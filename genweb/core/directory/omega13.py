# NOT USED
from AccessControl.Permissions import manage_users
from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from OFS.Cache import Cacheable
from plone import api
from five import grok
from zope.interface import Interface
from zope.interface import implements
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService import registerMultiPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IUserEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin

from Products.CMFPlone.interfaces import IPloneSiteRoot

from souper.interfaces import ICatalogFactory
from zope.component import getUtility

from repoze.catalog.query import Eq
from souper.soup import get_soup

import logging

logger = logging.getLogger('Omega13')


class IOmega13Helper(Interface):
    """Marker interface for Omega13Helper."""


# The Plugin
class Omega13Helper(BasePlugin, Cacheable):
    """ Omega13 PAS Plugin """

    meta_type = 'Omega13 Helper'
    security = ClassSecurityInfo()

    implements(IOmega13Helper, IUserEnumerationPlugin, IPropertiesPlugin)

    _properties = (
        {
            'id': 'oauth_server',
            'label': 'Oauth Server URL',
            'type': 'string',
            'mode': 'w'
        },
    )

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    security.declarePrivate('enumerateUsers')
    def enumerateUsers(self, id=None, login=None, exact_match=0, sort_by=None, max_results=None, **kw):
        """ Fullfill enumerateUsers requirements """
        # enumerateUsers Boilerplate
        plugin_id = self.getId()
        view_name = self.getId() + '_enumerateUsers'
        criteria = {'id': id, 'login': login, 'exact_match': exact_match,
                    'sort_by': sort_by, 'max_results': max_results}
        criteria.update(kw)

        cached_info = self.ZCacheable_get(view_name=view_name,
                                          keywords=criteria,
                                          default=None)

        if cached_info is not None:
            logger.warning('returning cached results from Omega13 enumerateUsers')
            return cached_info

        portal = api.portal.get()
        soup = get_soup('user_properties', portal)

        result = []
        if exact_match and (id or login):
            if id:
                records = [r for r in soup.query(Eq('username', id))]
            elif login:
                records = [r for r in soup.query(Eq('username', login))]

            if records:
                logger.warning('Omega13 found {} user: {}'.format(len(records), records))
                result.append({'id': records[0].attrs['username'],
                               'login': records[0].attrs['username'],
                               'pluginid': plugin_id,
                               })
        else:
            if id:
                records = [r for r in soup.query(Eq('username', id + '*'))]
            elif login:
                records = [r for r in soup.query(Eq('username', login + '*'))]

            if records:
                logger.warning('Omega13 found {} user: {}'.format(len(records), records))
                for record in records:
                    result.append({'id': record.attrs['username'],
                                   'login': record.attrs['username'],
                                   'pluginid': plugin_id,
                                   })

        result = tuple(result)
        self.ZCacheable_set(result, view_name=view_name, keywords=criteria)

        return result

    security.declarePrivate('getPropertiesForUser')
    def getPropertiesForUser(self, user, request=None):
        """ Fullfill PropertiesPlugin requirements """
        portal = api.portal.get()
        soup = get_soup('user_properties', portal)
        user_properties_utility = getUtility(ICatalogFactory, name='user_properties')
        indexed_attrs = user_properties_utility(portal).keys()
        properties = {}
        user.getId()
        records = [r for r in soup.query(Eq('username', user.getId()))]
        if records:
            for attr in indexed_attrs:
                if records[0].attrs.get(attr, False):
                    properties[attr] = records[0].attrs[attr]
            logger.warning('found properties for user: {}'.format(records[0].attrs['username']))

        return properties

InitializeClass(Omega13Helper)

# The Zope install part
manage_add_omega13_form = PageTemplateFile('browser/add_plugin', globals(), __name__='manage_add_omega13_form')


def manage_add_omega13_helper(dispatcher, id, title=None, REQUEST=None):
    """Add an omega13 Helper to the PluggableAuthentication Service."""

    sp = Omega13Helper(id, title)
    dispatcher._setObject(sp.getId(), sp)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_workspace'
                                     '?manage_tabs_message='
                                     'omega13Helper+added.'
                                     % dispatcher.absolute_url())


def register_omega13_plugin():
    try:
        registerMultiPlugin(Omega13Helper.meta_type)
    except RuntimeError:
        # make refresh users happy
        pass


def register_omega13_plugin_class(context):
    context.registerClass(Omega13Helper,
                          permission=manage_users,
                          constructors=(manage_add_omega13_form,
                                        manage_add_omega13_helper),
                          visibility = None,
                          icon='directory/icon.gif')


class ActivateOmega13(grok.View):
    grok.context(IPloneSiteRoot)

    def render(self):
        portal = self.context
        pas = portal.acl_users
        pluginid = 'omega13'

        installed = pas.objectIds()
        if pluginid in installed:
            return 'Omega 13 already installed.'

        plugin = Omega13Helper(pluginid, title='Omega13 plugin')
        pas._setObject(pluginid, plugin)
        plugin = pas[plugin.getId()]  # get plugin acquisition wrapped!
        for info in pas.plugins.listPluginTypeInfo():
            interface = info['interface']
            if not interface.providedBy(plugin):
                continue
            pas.plugins.activatePlugin(interface, plugin.getId())
            # In case we want to move it to the top
            pas.plugins.movePluginsDown(
                interface,
                [x[0] for x in pas.plugins.listPlugins(interface)[:-1]],
            )
        return 'Yes, captain.'
