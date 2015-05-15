from Acquisition import aq_inner
from pyquery import PyQuery as pq
from plone import api
from plone.app.search.browser import quote_chars
from plone.app.search.browser import EVER
from plone.memoize.instance import memoize

from Products.PlonePAS.utils import safe_unicode
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot
from Products.PluggableAuthService.PropertiedUser import PropertiedUser

from zope.event import notify
from Products.PluggableAuthService.events import PropertiesUpdated

from Products.CMFCore.MemberDataTool import MemberData as BaseMemberData
from Products.PluggableAuthService.interfaces.authservice import IPluggableAuthService
from Products.PlonePAS.interfaces.propertysheets import IMutablePropertySheet

from genweb.core.utils import get_safe_member_by_id


import unicodedata
import inspect
import logging


logger = logging.getLogger('event.LDAPUserFolder')
genweb_log = logging.getLogger('genweb.core')


def getToolbars(self, config):
    """ Patch the method for calculate number of toolbar rows from length of
        buttons replacing it with a hardcoded one for our convenience. Also,
        take advantage of the argument reference and add a missing value in
        TinyMCE configuration.
    """

    config['theme_advanced_blockformats'] = 'p,div,h2,h3,h4'

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


# TOREMOVE AS SOON AS THIS GOT PROPERLY FIXED
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


# TOREMOVE AS SOON AS THIS GOT PROPERLY FIXED
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
