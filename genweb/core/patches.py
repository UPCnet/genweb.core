# -*- coding: utf-8 -*-
try:
    from hashlib import sha1 as sha_new
except ImportError:
    from sha import new as sha_new
from urllib import quote_plus
from Acquisition import aq_inner
from pyquery import PyQuery as pq
from plone import api
from plone.app.content.browser.folderfactories import _allowedTypes
from plone.app.search.browser import quote_chars
from plone.app.search.browser import EVER
from plone.memoize.instance import memoize
from wildcard.foldercontents import wcfcMessageFactory as _WF
from wildcard.foldercontents.interfaces import IATCTFileFactory
from wildcard.foldercontents.interfaces import IDXFileFactory
from zope.i18n import translate
from zope.event import notify

from Products.PlonePAS.utils import safe_unicode
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.CMFPlone.browser.navtree import getNavigationRoot
from Products.PluggableAuthService.PropertiedUser import PropertiedUser
from Products.LDAPUserFolder.LDAPUser import NonexistingUser
from Products.LDAPUserFolder.LDAPUser import LDAPUser
from Products.PluggableAuthService.events import PropertiesUpdated
from Products.CMFCore.MemberDataTool import MemberData as BaseMemberData
from Products.PluggableAuthService.interfaces.authservice import IPluggableAuthService
from Products.PlonePAS.interfaces.propertysheets import IMutablePropertySheet
from StringIO import StringIO

from genweb.core.utils import get_safe_member_by_id, portal_url

from plone.app.content.interfaces import INameFromTitle
from Acquisition import aq_base
from plone.i18n.normalizer.interfaces import IUserPreferredURLNormalizer
from plone.i18n.normalizer.interfaces import IURLNormalizer
from zope.component import getUtility

import json
import mimetypes
import pkg_resources
import unicodedata
import inspect
import logging
import requests


logger = logging.getLogger('event.LDAPUserFolder')
genweb_log = logging.getLogger('genweb.core')


def getToolbars(self, config):
    """ Patch the method for calculate number of toolbar rows from length of
        buttons replacing it with a hardcoded one for our convenience. Also,
        take advantage of the argument reference and add a missing value in
        TinyMCE configuration.
    """

    config['theme_advanced_blockformats'] = 'p,div,h2,h3,h4'

    try:
        custom_icons = api.portal.get_registry_record('genweb.controlpanel.core.IGenwebCoreControlPanelSettings.custom_editor_icons')
    except:
        custom_icons = []

    if custom_icons:
        return custom_icons
    else:
        return ['fullscreen,|,code,|,save,newdocument,|,plonetemplates,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,|,cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor',
                'formatselect,style,|,cleanup,removeformat,|,image,media,|,tablecontrols,styleprops,|,visualaid,|,sub,sup,|,charmap',
                '', '']


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


def generate_user_id(self, data):
    """Generate a user id from data.

    The data is the data passed in the form.  Note that when email
    is used as login, the data will not have a username.

    There are plans to add some more options and add a hook here
    so it is possible to use a different scheme here, for example
    creating a uuid or creating bob-jones-1 based on the fullname.

    This will update the 'username' key of the data that is passed.
    """
    if data.get('username'):
        default = data.get('username').lower()
    elif data.get('email'):
        default = data.get('email').lower()
    else:
        default = ''
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


# TO REMOVE AS SOON AS THIS GOT PROPERLY FIXED
# This fixes CMFEditions to work with Dexterity combined with five.pt that
# doesn't exposes "macros" property, also fix bug in retrieving the correct
# version

def get_macros(self, vdata):
    context = aq_inner(self.context)
    # We need to get the view appropriate for the object in the
    # history, not the current object, which may differ due to
    # some migration.
    type_info = context.portal_types.getTypeInfo(vdata.object)

    # build the name of special versions views
    if getattr(type_info, 'getViewMethod', None) is not None:
        # Should use IBrowserDefault.getLayout ?
        def_method_name = type_info.getViewMethod(context)
    else:
        def_method_name = type_info.getActionInfo(
            'object/view')['url'].split('/')[-1] or \
            getattr(type_info, 'default_view', 'view')
    versionPreviewMethodName = 'version_%s' % def_method_name
    versionPreviewTemplate = getattr(
        context, versionPreviewMethodName, None)

    # check if a special version view exists
    if getattr(versionPreviewTemplate, 'macros', None) is None:
        # Use the Plone's default view template
        versionPreviewTemplate = vdata.object.restrictedTraverse(
            def_method_name)

    if getattr(versionPreviewTemplate, 'macros', None) is None:
        # We assume we are using Dexterity Content Types along with five.pt
        content = pq(versionPreviewTemplate.index())
        return content('#content-core').html()

    macro_names = ['content-core', 'main']

    try:
        return versionPreviewTemplate.macros['content-core']
    except KeyError:
        pass  # No content-core macro could mean that we are in plone3 land
    try:
        return versionPreviewTemplate.macros['main']
    except KeyError:
        context.plone_log(
            '(CMFEditions: @@get_macros) Internal error: Missing TAL '
            'macros %s in template "%s".' % (', '.join(macro_names), versionPreviewMethodName))
        return None


# TO REMOVE AS SOON AS THIS GOT PROPERLY FIXED
# This fixes the save button on TinyMCE for dexterity content types with
# Richtext fields. This should be solved on Plone 5 or with the new version of
# TinyMCE

from zope.interface import implements
from Products.TinyMCE.adapters.interfaces.Save import ISave
from plone.app.contenttypes.behaviors.richtext import IRichText


class Save(object):
    """Saves the richedit field"""

    implements(ISave)

    def __init__(self, context):
        """Constructor"""

        self.context = context

    def save(self, text, fieldname):
        """Saves the specified richedit field"""
        fieldname = fieldname.split('.')[-1]
        setattr(self.context, fieldname, IRichText['text'].fromUnicode(text))

        return 'saved'


def setMemberProperties(self, mapping, force_local=0):
    """ PAS-specific method to set the properties of a
        member. Ignores 'force_local', which is not reliably present.
    """
    sheets = None

    # We could pay attention to force_local here...
    if not IPluggableAuthService.providedBy(self.acl_users):
        # Defer to base impl in absence of PAS, a PAS user, or
        # property sheets
        return BaseMemberData.setMemberProperties(self, mapping)
    else:
        # It's a PAS! Whee!
        user = self.getUser()
        sheets = getattr(user, 'getOrderedPropertySheets', lambda: None)()

        # We won't always have PlonePAS users, due to acquisition,
        # nor are guaranteed property sheets
        if not sheets:
            # Defer to base impl if we have a PAS but no property
            # sheets.
            return BaseMemberData.setMemberProperties(self, mapping)

    # If we got this far, we have a PAS and some property sheets.
    # XXX track values set to defer to default impl
    # property routing?
    modified = False
    for k, v in mapping.items():
        if v is None:
            continue
        for sheet in sheets:
            if not sheet.hasProperty(k):
                continue
            if IMutablePropertySheet.providedBy(sheet):
                sheet.setProperty(user, k, v)
                modified = True
            else:
                break
                # raise RuntimeError, ("Mutable property provider "
                #                     "shadowed by read only provider")
    if modified:
        self.notifyModified()

        # Genweb: Updated by patch
        notify(PropertiesUpdated(user, mapping))


WHITELISTED_CALLERS = ['getMemberById/getMemberInfo/author/authorname/__call__/render/render/render/render/__call__/pt_render/__call__/__call__/render/render/render/render_content_provider/render_content/render_master/render/render/render/render/__call__/pt_render/__call__/__call__/__call__/call_object/mapply/publish/publish_module_standard/publish_module/__init__',
                       'getMemberById/getMemberInfo/author/render/render/render/render/__call__/pt_render/__call__/__call__/render/render/render/render_content_provider/render_content/render_master/render/render/render/render/__call__/pt_render/__call__/__call__/__call__/call_object/mapply/publish/publish_module_standard/publish_module/__init__',
                       'getMemberById/getMemberInfo/info/memogetter/render_listitem/render_entries/render_listing/render_content_core/__fill_content_core/render_content/render_master/render/render/render/render/__call__/pt_render/__call__/__call__/__call__/call_object/mapply/publish/publish_module_standard/publish_module/__init__',
                       'getMemberById/getMemberInfo/info/memogetter/render_listitem/__fill_entry/render_entries/__fill_entries/render_listing/render_content_core/render_listing/__fill_content_core/render_content/render_master/render/render/render/render/__call__/pt_render/__call__/__call__/__call__/call_object/mapply/publish/publish_module_standard/wrapper/publish_module/__init__',
                       'getMemberById/getMemberInfo/author/render/render/render/render/__call__/pt_render/__call__/__call__/render/render/render/render_content_provider/render_content/render_master/render/render/render/render/__call__/pt_render/__call__/__call__/__call__/call_object/mapply/publish/publish_module_standard/wrapper/publish_module/__init__',
                       'getMemberById/getMemberInfo/author/authorname/__call__/render/render/render/render/__call__/pt_render/__call__/__call__/render/render/render/render_content_provider/render_content/render_master/render/render/render/render/__call__/pt_render/__call__/__call__/__call__/call_object/mapply/publish/publish_module_standard/wrapper/publish_module/__init__',
                       'getMemberById/getMemberInfo/author/authorname/__call__/render/render/render/render/__call__/pt_render/__call__/__call__/render/render/render/render_content_provider/render_content/render_master/render/render/render/render/__call__/pt_render/__call__/__call__/__call__/__call__/__call__/call_object/mapply/publish/publish_module_standard/wrapper/publish_module/__init__',
                       'getMemberById/getMemberInfo/update/_updateViewlets/update/render_content_provider/render_master/render/render/render/render/__call__/pt_render/render/_render_template/__call__/call_object/mapply/publish/publish_module_standard/publish_module/__init__'
                       ]


# from profilehooks import timecall
# Patch for shout the evidence of using a getMemberById!
# @timecall
def getMemberById(self, id):
    '''
    Returns the given member.
    '''
    stack = inspect.stack()
    upstream_callers = '/'.join([a[3] for a in stack])

    # If the requested callers is in the whitelist
    if upstream_callers in WHITELISTED_CALLERS:
        user = get_safe_member_by_id(id)
        if user is not None:
            user_towrap = PropertiedUser(id)
            # As we added the key 'id' into the local user catalog, we need to
            # get rid of the get_safe_member_by_id result to make
            # addPropertyShit (pun intended) happy
            user.pop('id', None)
            user_towrap.addPropertysheet('omega13', user)
            user = self.wrapUser(user_towrap)
            return user

    # If the user is not on the new catalog, then fallback anyway
    if api.env.debug_mode():
        genweb_log.warning('')
        genweb_log.warning('Warning! Using getMemberById')
        genweb_log.warning('from: {}'.format(upstream_callers))
        genweb_log.warning('')

    user = self._huntUser(id, self)
    if user is not None:
        user = self.wrapUser(user)

    return user


# TinyMCE install. To remove default values in styles and tablestyles
def _importNode(self, node):
    """Import the object from the DOM node"""
    if self.environ.shouldPurge() or node.getAttribute('purge').lower() == 'true':
        self._purgeAttributes()

    for categorynode in node.childNodes:
        if categorynode.nodeName != '#text' and categorynode.nodeName != '#comment':
            for fieldnode in categorynode.childNodes:
                if fieldnode.nodeName != '#text' and fieldnode.nodeName != '#comment':
                    if self.attributes[categorynode.nodeName][fieldnode.nodeName]['type'] == 'Bool':
                        if fieldnode.hasAttribute('value'):
                            setattr(self.context, fieldnode.nodeName, self._convertToBoolean(fieldnode.getAttribute('value')))
                    elif self.attributes[categorynode.nodeName][fieldnode.nodeName]['type'] == 'Text':
                        if fieldnode.hasAttribute('value'):
                            setattr(self.context, fieldnode.nodeName, fieldnode.getAttribute('value'))
                    elif self.attributes[categorynode.nodeName][fieldnode.nodeName]['type'] == 'List':
                        field = getattr(self.context, fieldnode.nodeName)
                        if field is None or fieldnode.getAttribute('purge').lower() == 'true':
                            items = {}
                        else:
                            if fieldnode.nodeName == 'styles' or fieldnode.nodeName == 'tablestyles':
                                items = {}
                            else:
                                items = dict.fromkeys(field.split('\n'))
                        for element in fieldnode.childNodes:
                            if element.nodeName != '#text' and element.nodeName != '#comment':
                                if element.getAttribute('remove').lower() == 'true' and \
                                        element.getAttribute('value') in items:
                                    del(items[element.getAttribute('value')])
                                elif element.getAttribute('remove').lower() != 'true' and \
                                        element.getAttribute('value') not in items:
                                    items[element.getAttribute('value')] = None
                        string = '\n'.join(sorted(items.keys()))

                        # Don't break on international characters or otherwise
                        # funky data -
                        if type(string) == str:
                            # On Plone 4.1 this should not be reached
                            # as string is unicode in any case
                            string = string.decode('utf-8', 'ignore')

                        setattr(self.context, fieldnode.nodeName, string)

    self._logger.info('TinyMCE Settings imported.')


# Patching the custom pas_member view that is called from some templates of p.a.c.
@memoize
def info(self, userid=None):
    user = get_safe_member_by_id(userid)
    if user is None:
        # No such member: removed?  We return something useful anyway.
        return {'username': userid, 'description': '', 'language': '',
                'home_page': '', 'name_or_id': userid, 'location': '',
                'fullname': ''}
    user['name_or_id'] = user.get('fullname') or \
        user.get('username') or userid
    return user


# Patching the method that calls getMemberById in DocumentByLine
def author(self):
    return get_safe_member_by_id(self.creator())


# Add subjects and creators to searchableText Dexterity objects
def SearchableText(obj, text=False):
    subjList = []
    creatorList = []

    for sub in obj.subject:
        subjList.append(sub)
    subjects = ','.join(subjList)

    for creator in obj.creators:
        creatorList.append(creator)
    creators = ','.join(creatorList)

    return u' '.join((
        safe_unicode(obj.id),
        safe_unicode(obj.title) or u'',
        safe_unicode(obj.description) or u'',
        safe_unicode(subjects) or u'',
        safe_unicode(creators) or u'',
    ))


def getThreads(self, start=0, size=None, root=0, depth=None):
        """Get threaded comments
        """

        def recurse(comment_id, d=0):
            # Yield the current comment before we look for its children
            yield {'id': comment_id, 'comment': self[comment_id], 'depth': d}

            # Recurse if there are children and we are not out of our depth
            if depth is None or d + 1 < depth:
                children = self._children.get(comment_id, None)
                if children is not None:
                    for child_id in children:
                        for value in recurse(child_id, d + 1):
                            yield value

        # Find top level threads
        comments = self._children.get(root, None)
        if comments is not None:
            count = 0l
            for comment_id in reversed(comments.keys(min=start)):

                # Abort if we have found all the threads we want
                count += 1
                if size and count > size:
                    return

                # Let the closure recurse
                for value in recurse(comment_id):
                    yield value


def getUserByAttr(self, name, value, pwd=None, cache=0):
    """
        Get a user based on a name/value pair representing an
        LDAP attribute provided to the user.  If cache is True,
        try to cache the result using 'value' as the key
    """
    if not value:
        return None

    cache_type = pwd and 'authenticated' or 'anonymous'
    negative_cache_key = '%s:%s:%s' % (name,
                                       value,
                                       sha_new(pwd or '').hexdigest())
    if cache:
        if self._cache('negative').get(negative_cache_key) is not None:
            return None

        cached_user = self._cache(cache_type).get(value, pwd)

        if cached_user:
            msg = 'getUserByAttr: "%s" cached in %s cache' % (value, cache_type)
            logger.debug(msg)
            return cached_user

    user_roles, user_dn, user_attrs, ldap_groups = self._lookupuserbyattr(name=name, value=value, pwd=pwd)

    if user_dn is None:
        logger.debug('getUserByAttr: "%s=%s" not found' % (name, value))
        self._cache('negative').set(negative_cache_key, NonexistingUser())
        return None

    if user_attrs is None:
        msg = 'getUserByAttr: "%s=%s" has no properties, bailing' % (name, value)
        logger.debug(msg)
        self._cache('negative').set(negative_cache_key, NonexistingUser())
        return None

    if user_roles is None or user_roles == self._roles:
        msg = 'getUserByAttr: "%s=%s" only has roles %s' % (name, value, str(user_roles))
        logger.debug(msg)

    login_name = user_attrs.get(self._login_attr, '')
    uid = user_attrs.get(self._uid_attr, '')

    if self._login_attr != 'dn' and len(login_name) > 0:
        try:
            if name == self._login_attr:
                logins = [x for x in login_name
                          if value.strip().lower() == x.lower()]
                login_name = logins[0]
            else:
                login_name = login_name[0]
        except:
            msg = ('****getUserByAttr: logins %s and login_name %s' % (logins, login_name))
            logger.error(msg)
            pass

    elif len(login_name) == 0:
        msg = 'getUserByAttr: "%s" has no "%s" (Login) value!' % (user_dn, self._login_attr)
        logger.debug(msg)
        self._cache('negative').set(negative_cache_key, NonexistingUser())
        return None

    if self._uid_attr != 'dn' and len(uid) > 0:
        uid = uid[0]
    elif len(uid) == 0:
        msg = 'getUserByAttr: "%s" has no "%s" (UID Attribute) value!' % (user_dn, self._uid_attr)
        logger.debug(msg)
        self._cache('negative').set(negative_cache_key, NonexistingUser())
        return None

    # BEGIN PATCH
    login_name = login_name.lower()
    uid = uid.lower()
    # END PATCH

    user_obj = LDAPUser(uid,
                        login_name,
                        pwd or 'undef',
                        user_roles or [],
                        [],
                        user_dn,
                        user_attrs,
                        self.getMappedUserAttrs(),
                        self.getMultivaluedUserAttrs(),
                        ldap_groups=ldap_groups)

    if cache:
        self._cache(cache_type).set(value, user_obj)

    return user_obj


def enumerateUsers(self,
                   id=None,
                   login=None,
                   exact_match=0,
                   sort_by=None,
                   max_results=None,
                   **kw):
    """ Fulfill the UserEnumerationPlugin requirements """
    view_name = self.getId() + '_enumerateUsers'
    criteria = {'id': id, 'login': login, 'exact_match': exact_match,
                'sort_by': sort_by, 'max_results': max_results}
    criteria.update(kw)

    cached_info = self.ZCacheable_get(view_name=view_name,
                                      keywords=criteria,
                                      default=None)

    if cached_info is not None:
        logger.debug('returning cached results from enumerateUsers')
        return cached_info

    result = []
    acl = self._getLDAPUserFolder()
    login_attr = acl.getProperty('_login_attr')
    uid_attr = acl.getProperty('_uid_attr')
    rdn_attr = acl.getProperty('_rdnattr')
    plugin_id = self.getId()
    edit_url = '%s/%s/manage_userrecords' % (plugin_id, acl.getId())

    if acl is None:
        return ()

    if exact_match and (id or login):
        if id:
            ldap_user = acl.getUserById(id)
            if ldap_user is not None and ldap_user.getId() != id:
                ldap_user = None
        elif login:
            ldap_user = acl.getUser(login)
            if ldap_user is not None and ldap_user.getUserName() != login:
                ldap_user = None

        if ldap_user is not None:
            qs = 'user_dn=%s' % quote_plus(ldap_user.getUserDN())
            result.append({'id': ldap_user.getId(),
                           'login': ldap_user.getProperty(login_attr),
                           'pluginid': plugin_id,
                           'editurl': '%s?%s' % (edit_url, qs)})
    else:
        l_results = []
        seen = []
        ldap_criteria = {}

        if id:
            if uid_attr == 'dn':
                # Workaround: Due to the way findUser reacts when a DN
                # is searched for I need to hack around it... This
                # limits the usefulness of searching by ID if the user
                # folder uses the full DN aas user ID.
                ldap_criteria[rdn_attr] = id
            else:
                ldap_criteria[uid_attr] = id

        if login:
            ldap_criteria[login_attr] = login

        for key, val in kw.items():
            if key not in (login_attr, uid_attr):
                ldap_criteria[key] = val

        # If no criteria are given create a criteria set that will
        # return all users
        if not login and not id:
            ldap_criteria[login_attr] = ''

        l_results = acl.searchUsers(exact_match=exact_match, **ldap_criteria)

        for l_res in l_results:
            try:
                # If the LDAPUserFolder returns an error, bail
                if (l_res.get('sn', '') == 'Error' and l_res.get('cn', '') == 'n/a'):
                    return ()

                if l_res['dn'] not in seen:
                    # BEGIN PATCH
                    l_res['id'] = l_res[uid_attr].lower()
                    l_res['login'] = l_res[login_attr].lower()
                    # END PATCH
                    l_res['pluginid'] = plugin_id
                    quoted_dn = quote_plus(l_res['dn'])
                    l_res['editurl'] = '%s?user_dn=%s' % (edit_url, quoted_dn)
                    result.append(l_res)
                    seen.append(l_res['dn'])
            except:
                msg = ('****Result ldap error: l_res %s' % (l_res))
                logger.error(msg)
                pass

        if sort_by is not None:
            result.sort(lambda a, b: cmp(a.get(sort_by, '').lower(),
                                         b.get(sort_by, '').lower()))

        if isinstance(max_results, int) and len(result) > max_results:
            result = result[:max_results - 1]

    result = tuple(result)
    self.ZCacheable_set(result, view_name=view_name, keywords=criteria)

    return result


from AccessControl import Unauthorized
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.permissions import ManageUsers
from zope.component import getMultiAdapter
from genweb.core.adapters.portrait import IPortraitUploadAdapter


# Extensible member portrait management
def changeMemberPortrait(self, portrait, id=None):
    """update the portait of a member.

    We URL-quote the member id if needed.

    Note that this method might be called by an anonymous user who
    is getting registered.  This method will then be called from
    plone.app.users and this is fine.  When called from restricted
    python code or with a curl command by a hacker, the
    declareProtected line will kick in and prevent use of this
    method.
    """
    authenticated_id = self.getAuthenticatedMember().getId()
    if not id:
        id = authenticated_id
    safe_id = self._getSafeMemberId(id)

    # Our LDAP improvements hand the current user id in unicode, but BTree can't
    # handle unicode keys in inner objects... *sigh*
    if isinstance(safe_id, unicode):
        safe_id = str(safe_id)

    if authenticated_id and id != authenticated_id:
        # Only Managers can change portraits of others.
        if not _checkPermission(ManageUsers, self):
            raise Unauthorized

    # The plugable actions for how to handle the portrait.
    adapter = getMultiAdapter((self, self.REQUEST), IPortraitUploadAdapter)
    adapter(portrait, safe_id)


def deletePersonalPortrait(self, id=None):
    """deletes the Portait of a member.
    """
    authenticated_id = self.getAuthenticatedMember().getId()
    if not id:
        id = authenticated_id
    safe_id = self._getSafeMemberId(id)
    if id != authenticated_id and not _checkPermission(
            ManageUsers, self):
        raise Unauthorized

    # The plugable actions for how to handle the portrait.
    portrait_url = portal_url() + '/defaultUser.png'
    imgData = requests.get(portrait_url).content
    image = StringIO(imgData)
    image.filename = 'defaultUser'
    adapter = getMultiAdapter((self, self.REQUEST), IPortraitUploadAdapter)
    adapter(image, safe_id)
    # membertool = getToolByName(self, 'portal_memberdata')
    # return membertool._deletePortrait(safe_id)


try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    from plone.dexterity.interfaces import IDexterityFTI
    HAS_DEXTERITY = True


def jupload__call__(self):
    authenticator = getMultiAdapter((self.context, self.request),
                                    name=u"authenticator")
    if not authenticator.verify() or \
            self.request['REQUEST_METHOD'] != 'POST':
        raise Unauthorized
    filedata = self.request.form.get("files[]", None)
    if filedata is None:
        return
    filename = filedata.filename
    content_type = mimetypes.guess_type(filename)[0] or ""

    if not filedata:
        return

    ctr = getToolByName(self.context, 'content_type_registry')
    type_ = ctr.findTypeName(filename.lower(), '', '') or 'File'

    # Determine if the default file/image types are DX or AT based
    DX_BASED = False
    context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
    if HAS_DEXTERITY:
        pt = getToolByName(self.context, 'portal_types')
        if IDexterityFTI.providedBy(getattr(pt, type_)):
            factory = IDXFileFactory(self.context)
            DX_BASED = True
        else:
            factory = IATCTFileFactory(self.context)
        # if the container is a DX type, get the available types from the behavior
        if IDexterityFTI.providedBy(getattr(pt, self.context.portal_type)):
            addable_types = ISelectableConstrainTypes(
                self.context).getLocallyAllowedTypes()
        elif context_state.is_portal_root():
            allowed_types = _allowedTypes(self.request, self.context)
            addable_types = [fti.getId() for fti in allowed_types]
        else:
            addable_types = self.context.getLocallyAllowedTypes()
    else:
        factory = IATCTFileFactory(self.context)
        if context_state.is_portal_root():
            allowed_types = _allowedTypes(self.request, self.context)
            addable_types = [fti.getId() for fti in allowed_types]
        else:
            addable_types = self.context.getLocallyAllowedTypes()

    # if the type_ is disallowed in this folder, return an error
    if type_ not in addable_types:
        msg = translate(
            _WF('disallowed_type_error',
                default='${filename}: adding of "${type}" \
                         type is disabled in this folder',
                mapping={'filename': filename, 'type': type_}),
            context=self.request
        )
        return json.dumps({'files': [{'error': msg}]})

    obj = factory(filename, content_type, filedata)

    if DX_BASED:
        if 'File' in obj.portal_type:
            size = obj.file.getSize()
            content_type = obj.file.contentType
        elif 'Image' in obj.portal_type:
            size = obj.image.getSize()
            content_type = obj.image.contentType

        result = {
            "url": obj.absolute_url(),
            "name": obj.getId(),
            "type": content_type,
            "size": size
        }
    else:
        try:
            size = obj.getSize()
        except AttributeError:
            size = obj.getObjSize()

        result = {
            "url": obj.absolute_url(),
            "name": obj.getId(),
            "type": obj.getContentType(),
            "size": size
        }

    if 'Image' in obj.portal_type:
        result['thumbnail_url'] = result['url'] + '/@@images/image/tile'

    return json.dumps({
        'files': [result]
    })


def chooseName(self, name, object):
    container = aq_inner(self.context)
    if not name:
        nameFromTitle = INameFromTitle(object, None)
        if nameFromTitle is not None:
            name = nameFromTitle.title
        if not name:
            name = getattr(aq_base(object), 'id', None)
        if not name:
            name = getattr(aq_base(object), 'portal_type', None)
        if not name:
            name = object.__class__.__name__

    if not isinstance(name, unicode):
        name = unicode(name, 'utf-8')

    request = getattr(object.__of__(container), 'REQUEST', None)
    if request is not None:
        name = IUserPreferredURLNormalizer(request).normalize(name)
    else:
        name = getUtility(IURLNormalizer).normalize(name)

    if name[:1] == '_':
        name = name[1:]

    return self._findUniqueName(name, object)
