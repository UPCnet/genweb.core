from plone.app.search.browser import quote_chars
from plone.app.search.browser import EVER

from Products.PlonePAS.utils import safe_unicode
from Products.LDAPUserFolder.utils import guid2string
from Products.LDAPUserFolder.LDAPDelegate import filter_format
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot

import unicodedata

import logging

logger = logging.getLogger('event.LDAPUserFolder')


def getToolbars(self, config):
    """ Patch the method for calculate number of toolbar rows from length of
        buttons replacing it with a hardcoded one for our convenience. Also,
        take advantage of the argument reference and add a missing value in
        TinyMCE configuration.
    """

    config['theme_advanced_blockformats'] = "p,div,h2,h3,h4"

    return ["fullscreen,|,code,|,save,newdocument,|,plonetemplates,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,|,cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor",
            "formatselect,style,|,cleanup,removeformat,|,image,media,|,tablecontrols,styleprops,|,visualaid,|,sub,sup,|,charmap",
            "", ""]


def isStringType(data):
    return isinstance(data, str) or isinstance(data, unicode)


def testMemberData(self, memberdata, criteria, exact_match=False):
    """Patch the method that test if a memberdata matches the search criteria
       for making it normalization of unicode strings aware.
    """
    for (key, value) in criteria.items():
        testvalue = memberdata.get(key, None)
        if testvalue is None:
            return False

        if isStringType(testvalue):
            testvalue = safe_unicode(testvalue.lower())
        if isStringType(value):
            value = safe_unicode(value.lower())

        if exact_match:
            if value != testvalue:
                return False
        else:
            try:
                if value not in testvalue and \
                   unicodedata.normalize('NFKD', value).encode('ASCII', 'ignore') not in unicodedata.normalize('NFKD', testvalue).encode('ASCII', 'ignore'):
                    return False
            except TypeError:
                # Fall back to exact match if we can check for
                # sub-component
                if value != testvalue:
                    return False

    return True


def searchUsers(self, attrs=(), exact_match=False, **kw):
    """ Look up matching user records based on one or mmore attributes

    This method takes any passed-in search parameters and values as
    keyword arguments and will sort out invalid keys automatically. It
    accepts all three forms an attribute can be known as, its real
    ldap name, the name an attribute is mapped to explicitly, and the
    friendly name it is known by.
    """
    users = []
    users_base = self.users_base
    search_scope = self.users_scope
    filt_list = []

    if not attrs:
        attrs = self.getSchemaConfig().keys()

    schema_translator = {}
    for ldap_key, info in self.getSchemaConfig().items():
        public_name = info.get('public_name', None)
        friendly_name = info.get('friendly_name', None)

        if friendly_name:
            schema_translator[friendly_name] = ldap_key

        if public_name:
            schema_translator[public_name] = ldap_key

        schema_translator[ldap_key] = ldap_key

    for (search_param, search_term) in kw.items():
        if search_param == 'dn':
            users_base = search_term
            search_scope = self._delegate.BASE

        elif search_param == 'objectGUID':
            # we can't escape the objectGUID query piece using filter_format
            # because it replaces backslashes, which we need as a result
            # of guid2string
            users_base = self.users_base
            guid = guid2string(search_term)

            if exact_match:
                filt_list.append('(objectGUID=%s)' % guid)
            else:
                filt_list.append('(objectGUID=*%s*)' % guid)

        else:
            # If the keyword arguments contain unknown items we will
            # simply ignore them and continue looking.
            ldap_param = schema_translator.get(search_param, None)
            if ldap_param is None:
                return []

            if search_term and exact_match:
                filt_list.append(filter_format('(%s=%s)'
                                               , (ldap_param, search_term)
                                               ))
            elif search_term:
                filt_list.append(filter_format('(%s=*%s*)'
                                               , (ldap_param, search_term)
                                               ))
            else:
                filt_list.append('(%s=*)' % ldap_param)

    if len(filt_list) == 0 and search_param != 'dn':
        # We have no useful filter criteria, bail now before bringing the
        # site down with a search that is overly broad.
        res = { 'exception' : 'No useful filter criteria given' }
        res['size'] = 0
        search_str = ''

    else:
        search_str = self._getUserFilterString(filters=filt_list)
        res = self._delegate.search( base=users_base
                                   , scope=search_scope
                                   , filter=search_str
                                   , attrs=attrs
                                   )

    if res['exception']:
        logger.debug('findUser Exception (%s)' % res['exception'])
        msg = 'findUser search filter "%s"' % search_str
        logger.debug(msg)
        users = [{ 'dn' : res['exception']
                 , 'cn' : 'n/a'
                 , 'sn' : 'Error'
                 }]

    elif res['size'] > 0:
        res_dicts = res['results']
        for i in range(res['size']):
            dn = res_dicts[i].get('dn')
            rec_dict = {}
            rec_dict['sn'] = rec_dict['cn'] = ''

            for key, val in res_dicts[i].items():
                rec_dict[key] = val[0]

            rec_dict['dn'] = dn

            users.append(rec_dict)

    return users


def generate_user_id(self, data):
    """Generate a user id from data.

    The data is the data passed in the form.  Note that when email
    is used as login, the data will not have a username.

    There are plans to add some more options and add a hook here
    so it is possible to use a different scheme here, for example
    creating a uuid or creating bob-jones-1 based on the fullname.

    This will update the 'username' key of the data that is passed.
    """
    default = data.get('username').lower() or data.get('email').lower() or ''
    data['username'] = default
    return default


def filter_query(self, query):
    request = self.request

    catalog = getToolByName(self.context, 'portal_catalog')
    valid_indexes = tuple(catalog.indexes())
    valid_keys = self.valid_keys + valid_indexes

    text = query.get('SearchableText', None)
    if text is None:
        text = request.form.get('SearchableText', '')
    if not text:
        # Without text, must provide a meaningful non-empty search
        valid = set(valid_indexes).intersection(request.form.keys()) or \
            set(valid_indexes).intersection(query.keys())
        if not valid:
            return

    for k, v in request.form.items():
        if v and ((k in valid_keys) or k.startswith('facet.')):
            query[k] = v
    if text:
        query['SearchableText'] = quote_chars(text) + '*'

    # don't filter on created at all if we want all results
    created = query.get('created')
    if created:
        if created.get('query'):
            if created['query'][0] <= EVER:
                del query['created']

    # respect `types_not_searched` setting
    types = query.get('portal_type', [])
    if 'query' in types:
        types = types['query']
    query['portal_type'] = self.filter_types(types)
    # respect effective/expiration date
    query['show_inactive'] = False
    # respect navigation root
    if 'path' not in query:
        query['path'] = getNavigationRoot(self.context)

    return query


# TOREMOVE as soon 4.3.4 goes live.
import transaction
from Acquisition import aq_inner
from Acquisition import aq_parent
from ZODB.POSException import ConflictError
from plone.app.linkintegrity.exceptions import LinkIntegrityNotificationException
from Products.CMFPlone.utils import log_exc
from Products.CMFPlone.utils import transaction_note


def deleteObjectsByPaths(self, paths, handle_errors=True, REQUEST=None):
    failure = {}
    success = []
    # use the portal for traversal in case we have relative paths
    portal = getToolByName(self, 'portal_url').getPortalObject()
    traverse = portal.restrictedTraverse
    for path in paths:
        # Skip and note any errors
        if handle_errors:
            sp = transaction.savepoint(optimistic=True)
        try:
            # To avoid issues with the check for acquisition,
            # relative paths should not be part of the API anymore.
            # Plone core itself does not use relative paths.
            if not path.startswith("/".join(portal.getPhysicalPath())):
                msg = (
                    'Path {} does not start '
                    'with path to portal'.format(path)
                )
                raise ValueError(msg)
            obj = traverse(path)
            if list(obj.getPhysicalPath()) != path.split('/'):
                msg = (
                    'Path {} does not match '
                    'traversed object physical path. '
                    'This is likely an acquisition issue.'.format(path)
                )
                raise ValueError(msg)
            obj_parent = aq_parent(aq_inner(obj))
            obj_parent.manage_delObjects([obj.getId()])
            success.append('%s (%s)' % (obj.getId(), path))
        except ConflictError:
            raise
        except LinkIntegrityNotificationException:
            raise
        except Exception, e:
            if handle_errors:
                sp.rollback()
                failure[path] = e
                log_exc()
            else:
                raise
    transaction_note('Deleted %s' % (', '.join(success)))
    return success, failure
