from Products.PlonePAS.utils import safe_unicode
from Products.LDAPUserFolder.utils import guid2string
from Products.LDAPUserFolder.LDAPDelegate import filter_format

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
