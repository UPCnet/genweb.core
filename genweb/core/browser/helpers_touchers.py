# -*- coding: utf-8 -*-
from five import grok
from plone import api
from Acquisition import aq_inner
from OFS.interfaces import IApplication
from zope.interface import Interface
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from souper.soup import get_soup
import pkg_resources

from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin
from Products.PortalTransforms.transforms.pdf_to_text import pdf_to_text

from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.app.contenttypes.interfaces import IFolder
from plone.app.contenttypes.upgrades import use_new_view_names
from plone.dexterity.utils import createContentInContainer
from plone.dexterity.content import Container
from plone.subrequest import subrequest
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.constants import CONTEXT_CATEGORY

from genweb.core import HAS_DXCT
from genweb.core import HAS_PAM
from genweb.core.utils import json_response
from genweb.core.interfaces import IHomePage
from genweb.core.utils import add_user_to_catalog
from genweb.core.utils import reset_user_catalog
from genweb.core.browser.plantilles import get_plantilles
from genweb.core.browser.helpers import listPloneSites
from genweb.core.browser.helpers import setupInstallProfile

try:
    pkg_resources.get_distribution('plone4.csrffixes')
except pkg_resources.DistributionNotFound:
    CSRF = False
else:
    from plone.protect.interfaces import IDisableCSRFProtection
    CSRF = True

if HAS_PAM:
    from plone.app.multilingual.browser.setup import SetupMultilingualSite


class matagetHTTPCacheheaders(grok.View):
    """ Canvia el portal_type dels objectes del PloneSurvey que tinguin espais en el nom del tipus"""

    grok.name('mata_get_http_cache_headers')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        ps = getToolByName(context, 'portal_setup')
        toolset = ps.getToolsetRegistry()
        required = toolset._required.copy()
        existing = portal.keys()
        changed = False
        for name, info in required.items():
            if name not in existing:
                del required[name]
                changed = True
        if changed:
            toolset._required = required
            print 'Cleaned up the toolset registry.'

        return required


class removeBrokenCacheFu(grok.View):
    """ Canvia el portal_type dels objectes del PloneSurvey que tinguin espais en el nom del tipus"""

    grok.name('remove_broken_cachefu')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        from plone.app.upgrade.v40.alphas import removeBrokenCacheFu
        context = aq_inner(self.context)

        removeBrokenCacheFu(context)

        return 'done'


class makeMeaHomePage(grok.View):
    """ makeMeaHomePage """
    grok.name('make_me_a_homepage')
    grok.context(Interface)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        alsoProvides(self.context, IHomePage)
        if HAS_DXCT:
            from plone.app.contenttypes.interfaces import IFolder
            if IFolder.providedBy(self.context):
                self.context.setLayout('homepage')
        return self.request.response.redirect(self.context.absolute_url())


class makeMeaSubHomePage(grok.View):
    """ makeMeaSubHomePage """
    grok.name('make_me_a_subhome_page')
    grok.context(Interface)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        alsoProvides(self.context, IHomePage)
        if HAS_DXCT:
            from plone.app.contenttypes.interfaces import IFolder
            if IFolder.providedBy(self.context):
                self.context.setLayout('subhomepage')
        return self.request.response.redirect(self.context.absolute_url())


class bulkUserCreator(grok.View):
    """
        Convenience bulk user creator. It requires parametrization in code and
        eventually, run this over a debug instance in production.
    """
    grok.name('bulk_user_creator')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        users = ['joan.giralt',
                 'gemma.baldris',
                 'carme.jimenez',
                 'lluis.malvis',
                 'joaquim.fernandez',
                 'pau.cabanyol',
                 'sandra.franch',
                 'jose.alberola',
                 'pedro.alvarez',
                 'francesc.guasch',
                 'angel.aguilera',
                 'javier.trueba',
                 'jesus.galceran',
                 'merce.oller',
                 'jordi.aguilar',
                 'david.figueres',
                 'josep.maria.jordana',
                 'annibal.manyas',
                 'alfredo.soldevilla',
                 'alex.muntada',
                 'albert.obiols',
                 'boris.martinez',
                 'carles.espadas',
                 'pepe.martinez',
                 'roberto.molina',
                 'raul.pastor',
                 'belen.lalueza',
                 'tonyi.gomez',
                 'rosa.ma.martin',
                 'jordi.enric.martinez',
                 'sandra.marsa',
                 'antoni.mayans',
                 'yolanda.blanc',
                 'susy.tur',
                 'toni.font',
                 'anna.casas',
                 'manoli.cano',
                 'andres.arco',
                 'esther.nadal',
                 'jose.angel.fernandez',
                 'elena.lopez.romera',
                 'eulalia.formenti',
                 'ignasi.mallafre',
                 'amador.alvarez',
                 'josep.m.haro',
                 'jose.luis.roncero',
                 'katty.torla',
                 'cristina.dantart',
                 'sara.perez',
                 'antonio.fernandez',
                 'jesus.otero',
                 'eulalia.font',
                 'rosa.martin',
                 'ruben.menendez',
                 'francesc.bassas',
                 'jordi.bofill',
                 'alicia.ruiz',
                 'cesc.garcia',
                 'manel.campano',
                 'david.ortin',
                 'jose.lazaro',
                 'sofia.pascual',
                 'luisa.vicente',
                 'enric.ribot',
                 'jose.marcos.lopez']

        for user in users:
            # password = user[0].upper() + user.split('.')[1][0].upper() + user.split('.')[1][1:]

            if not api.user.get(username=user):
                api.user.create(email=user + '@upc.edu',
                                username=user,
                                password='1234')

        return 'Done.'


class bulkUserEraser(grok.View):
    """
        Convenience bulk user eraser. It requires parametrization in code and
        eventually, run this over a debug instance in production.
    """
    grok.name('bulk_user_eraser')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        users = ['joan.giralt',
                 'gemma.baldris',
                 'carme.jimenez',
                 'lluis.malvis',
                 'joaquim.fernandez',
                 'pau.cabanyol',
                 'sandra.franch',
                 'jose.alberola',
                 'pedro.alvarez',
                 'francesc.guasch',
                 'angel.aguilera',
                 'javier.trueba',
                 'jesus.galceran',
                 'merce.oller',
                 'jordi.aguilar',
                 'david.figueres',
                 'josep.maria.jordana',
                 'annibal.manyas',
                 'alfredo.soldevilla',
                 'alex.muntada',
                 'albert.obiols',
                 'boris.martinez',
                 'carles.espadas',
                 'pepe.martinez',
                 'roberto.molina',
                 'raul.pastor',
                 'belen.lalueza',
                 'tonyi.gomez',
                 'rosa.ma.martin',
                 'jordi.enric.martinez',
                 'sandra.marsa',
                 'antoni.mayans',
                 'yolanda.blanc',
                 'susy.tur',
                 'toni.font',
                 'anna.casas',
                 'manoli.cano',
                 'andres.arco',
                 'esther.nadal',
                 'jose.angel.fernandez',
                 'elena.lopez.romera',
                 'eulalia.formenti',
                 'ignasi.mallafre',
                 'amador.alvarez',
                 'josep.m.haro',
                 'jose.luis.roncero',
                 'katty.torla',
                 'cristina.dantart',
                 'sara.perez',
                 'antonio.fernandez',
                 'jesus.otero',
                 'eulalia.font',
                 'rosa.martin',
                 'ruben.menendez',
                 'francesc.bassas',
                 'jordi.bofill',
                 'alicia.ruiz',
                 'cesc.garcia',
                 'manel.campano',
                 'david.ortin',
                 'jose.lazaro',
                 'sofia.pascual',
                 'luisa.vicente',
                 'enric.ribot',
                 'jose.marcos.lopez']

        for user in users:

            if api.user.get(username=user):
                api.user.delete(username=user)
                print("Deleted user {}".format(user))

        return 'Done.'


class reinstallGWControlPanel(grok.View):
    """ Reinstalls genweb.controlpanel in the current Plone site. """
    grok.context(IPloneSiteRoot)
    grok.name('reinstall_gw_controlpanel')
    grok.require('cmf.ManagePortal')

    def render(self):
        context = aq_inner(self.context)
        output = []
        qi = getToolByName(context, 'portal_quickinstaller')

        if qi.isProductInstalled('genweb.controlpanel'):
            qi.uninstallProducts(['genweb.controlpanel'], reinstall=True)
            qi.installProducts(['genweb.controlpanel'], reinstall=True)
            output.append('{}: Successfully reinstalled control panel'.format(context))
        import transaction
        transaction.commit()
        return '\n'.join(output)


class bulkReinstallGWControlPanel(grok.View):
    """
        Reinstall genweb.controlpanel in all the Plone instance of this Zope.
        Useful when added some parameter to the control panel and you want to
        apply it at the same time in all the existing Plone sites in the Zope.
    """
    grok.context(IApplication)
    grok.name('bulk_reinstall_gw_controlpanel')
    grok.require('cmf.ManagePortal')

    def render(self):
        context = aq_inner(self.context)
        plonesites = listPloneSites(context)
        output = []
        for plonesite in plonesites:
            response = subrequest('/'.join(plonesite.getPhysicalPath()) + '/reinstall_gwcontrolpanel')
            output.append(response.getBody())
        return '\n'.join(output)


class resetLanguage(grok.View):
    """
        Re-set the language of each LRF according to its name. Execute in an LRF
    """
    grok.context(Interface)
    grok.name('reset_language')
    grok.require('cmf.ManagePortal')

    def render(self):
        from plone.app.multilingual.interfaces import ILanguage
        context = aq_inner(self.context)
        pc = api.portal.get_tool('portal_catalog')
        results = pc.unrestrictedSearchResults(path='/'.join(context.getPhysicalPath()))

        for brain in results:
            ob = brain._unrestrictedGetObject()
            language_aware = ILanguage(ob, None)
            if language_aware is not None:
                language_aware.set_language(self.context.id)
                ob.reindexObject(idxs=['Language', 'TranslationGroup'])


class oldMigrateRLF(grok.View):
    """ Used to migrate from old PAM sites to the current (Container based) one.
        This is the version as of February 2015
    """
    grok.context(IPloneSiteRoot)
    grok.name('old_migrate_rlf')
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        portal = api.portal.get()
        pc = api.portal.get_tool(name="portal_catalog")
        lrfs = pc.searchResults(portal_type="LRF")

        text = []
        for brain in lrfs:
            lrf = portal[brain.id]
            if lrf.__class__ != Container:
                portal._delOb(brain.id)

                lrf.__class__ = Container
                portal._setOb(lrf.id, lrf)

                text.append('Migrated lrf {}\n'.format(lrf.absolute_url()))
        return ''.join(text) + '\nDone!'


class migrateRLF2roundFIGHT(grok.View):
    """ Used to migrate from old PAM sites to the current (Container based) one.
        This is the version as of February 2015
    """
    grok.context(IPloneSiteRoot)
    grok.name('migrate_rlf')
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        portal = api.portal.get()
        pc = api.portal.get_tool(name="portal_catalog")

        lrfs = pc.searchResults(portal_type="LRF")
        original_lrfs_ids = [lang.id for lang in lrfs]

        # Disable constrains
        pt = api.portal.get_tool('portal_types')
        pt['Plone Site'].filter_content_types = False
        PS_ALLOWED = pt['Plone Site'].allowed_content_types
        pt['Plone Site'].allowed_content_types = PS_ALLOWED + ('LRF',)
        pt['LRF'].global_allow = True
        pt['LIF'].global_allow = True
        LRF_ALLOWED = pt['LRF'].allowed_content_types
        pt['LRF'].allowed_content_types = LRF_ALLOWED + ('LIF', 'BannerContainer', 'Logos_Container')

        for lrf in lrfs:
            api.content.rename(obj=lrf.getObject(), new_id='{}_old'.format(lrf.id))

        setupTool = SetupMultilingualSite()
        setupTool.setupSite(self.context, False)

        for old_lrf in original_lrfs_ids:
            # If a 'media' folder exists, delete it as we are going to put it
            # back later
            if portal[old_lrf + '_old'].get('media', False):
                api.content.delete(obj=portal[old_lrf + '_old']['media'])
            if portal[old_lrf].get('media', False):
                api.content.delete(obj=portal[old_lrf]['media'])

            for obj in portal[old_lrf + '_old'].objectIds():
                # Only to contentish objects as the original LRF is leaking root
                # objects
                if portal[old_lrf + '_old'].get(obj, False):
                    origin = portal[old_lrf + '_old'][obj].id
                    api.content.move(source=portal[old_lrf + '_old'][obj], target=portal[old_lrf])
                    print '{} ==> {}'.format(origin, portal[old_lrf])

        # Assert things are moved correctly and no object remains in old folders
        for old_lrf in original_lrfs_ids:
            assert not portal[old_lrf + '_old'].get(obj, False)

        # If so, delete original LRFs
        for old_lrf in original_lrfs_ids:
            api.content.delete(obj=portal[old_lrf + '_old'])

        # Rename original 'shared' folder
        if portal.get('shared', False):
            api.content.rename(obj=portal['shared'], new_id='shared_old')

        # Put back 'shared' folder
        # for lrf in lrfs:
        #     api.content.create(container=portal[lrf.id], type='LIF', id='shared')
        #     portal[lrf.id]['shared'].title = 'Fitxers compartits'
        #     if lrf == 'es':
        #         portal[lrf.id]['shared'].title = 'Ficheros compartidos'
        #     if lrf == 'en':
        #         portal[lrf.id]['shared'].title = 'Shared files'

        # Move shared folder content
        # if portal.get('shared', False):
        #     for obj_id in portal['shared']:
        #         api.content.move(source=portal['shared'][obj_id], target=portal['ca']['shared'])
        #         print '{} ==> {}'.format(obj_id, portal['ca']['shared'].id)

        # Put back constrains
        pt['Plone Site'].filter_content_types = True
        pt['Plone Site'].allowed_content_types = PS_ALLOWED
        pt['LRF'].global_allow = False
        pt['LIF'].global_allow = False
        pt['LRF'].allowed_content_types = LRF_ALLOWED

        # Finally, clear and rebuild catalog
        pc.clearFindAndRebuild()


class reBuildUserPropertiesCatalog(grok.View):
    """ Rebuild the OMEGA13 repoze.catalog for user properties data

        For default, we use the mutable_properties (users who have entered into communities)

        Path directo del plugin:
        acl_users/plugins/manage_plugins?plugin_type=IPropertiesPlugin

        En ACL_USERS / LDAP / Properties / Active Plugins ha de estar ordenado así:
          mutable_properties / auto_group / ldapaspb

        But really, we use the most preferent plugin
        If the most preferent plugin is:
           mutable_properties --> users who have entered into communities
           ldap --> users in LDAP
    """
    grok.context(IPloneSiteRoot)
    grok.name('rebuild_user_catalog')
    grok.require('cmf.ManagePortal')

    def render(self):
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)
        portal = api.portal.get()
        plugins = portal.acl_users.plugins.listPlugins(IPropertiesPlugin)

        # We use the most preferent plugin
        # If the most preferent plugin is:
        #    mutable_properties --> users who have entered into communities
        #    ldap --> users in LDAP
        pplugin = plugins[0][1]
        all_user_properties = pplugin.enumerateUsers()

        for user in all_user_properties:
            user.update(dict(username=user['id']))
            if 'title' in user:
                user.update(dict(fullname=user['title']))
            elif 'fullname' in user:
                user.update(dict(fullname=user['fullname']))
            elif 'sn' in user:
                user.update(dict(fullname=user['sn']))
            else:
                user.update(dict(fullname=user['cn']))

            user_obj = api.user.get(user['id'])

            if user_obj:
                add_user_to_catalog(user_obj, user)
            else:
                print('No user found in user repository (LDAP) {}'.format(user['id']))

            print('Updated properties catalog for {}'.format(user['id']))


class ResetUserPropertiesCatalog(grok.View):
    """ Reset the OMEGA13 repoze.catalog for user properties data """

    grok.context(IPloneSiteRoot)
    grok.name('reset_user_catalog')
    grok.require('cmf.ManagePortal')

    def render(self):
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)
        reset_user_catalog()


class userPropertiesCatalogViewer(grok.View):
    """ Rebuild the OMEGA13 repoze.catalog for user properties data """
    grok.context(IPloneSiteRoot)
    grok.name('view_user_catalog')
    grok.require('cmf.ManagePortal')

    @json_response
    def render(self):
        portal = api.portal.get()
        soup = get_soup('user_properties', portal)
        records = [r for r in soup.data.items()]

        result = {}
        for record in records:
            item = {}
            for key in record[1].attrs:
                item[key] = record[1].attrs[key]

            result[record[1].attrs['id']] = item

        return result

class DeleteUserPropertiesCatalog(grok.View):
    """ Delete users in catalog not in LDAP.

        Path directo del plugin:
        acl_users/plugins/manage_plugins?plugin_type=IPropertiesPlugin

        En ACL_USERS / LDAP / Properties / Active Plugins ha de estar ordenado así:
          mutable_properties / auto_group / ldapaspb

    """
    grok.context(IPloneSiteRoot)
    grok.name('delete_user_catalog')
    grok.require('cmf.ManagePortal')

    def render(self):
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)

        portal = api.portal.get()
        plugins = portal.acl_users.plugins.listPlugins(IPropertiesPlugin)
        # We use the ldap plugin
        pplugin = plugins[2][1]
        results = []
        try:
            acl = pplugin._getLDAPUserFolder()

            soup = get_soup('user_properties', portal)
            records = [r for r in soup.data.items()]

            for record in records:
                # For each user in catalog search user in ldap
                user_obj = acl.getUserById(record[1].attrs['id'])
                if not user_obj:
                    print('No user found in user repository (LDAP) {}'.format(record[1].attrs['id']))
                    soup.__delitem__(record[1])
                    print('User delete soup {}'.format(record[1].attrs['id']))
                    results.append('User delete soup: {}'.format(record[1].attrs['id']))

            print('Finish rebuild_user_catalog')
            results.append('Finish rebuild_user_catalog')
            return '\n'.join([str(item) for item in results])
        except:
            print('The order to the plugins in En ACL_USERS / LDAP / Properties / Active Plugins : mutable_properties / auto_group / ldapaspb')
            results.append('The order to the plugins in En ACL_USERS / LDAP / Properties / Active Plugins : mutable_properties / auto_group / ldapaspb')
            return '\n'.join([str(item) for item in results])

class enablePDFIndexing(grok.View):
    """ Enable PDF indexing """
    grok.context(IPloneSiteRoot)
    grok.name('enable_pdf_indexing')
    grok.require('cmf.ManagePortal')

    def render(self):
        pt = api.portal.get_tool('portal_transforms')
        pt.registerTransform(pdf_to_text())

        return 'Done'


class updateFolderViews(grok.View):
    """ Update view methods for folder type in the current Plone site. """
    grok.context(IPloneSiteRoot)
    grok.name('update_folder_views')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if not portal:
            portal = api.portal.get()

        output = []
        portal.portal_types['Folder'].view_methods = ('listing_view', 'folder_extended', 'album_view', 'summary_view', 'tabular_view', 'full_view', 'folder_index_view')
        import transaction
        transaction.commit()
        output.append('{}: Successfully reinstalled'.format(portal.id))
        return '\n'.join(output)


class reinstallPloneProduct(grok.View):
    """ Reinstalls a product passed by form parameter in the current Plone site. """
    grok.context(IPloneSiteRoot)
    grok.name('reinstall_product')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if not portal:
            portal = api.portal.get()

        product_name = self.request.form['product_name']
        output = []
        qi = getToolByName(portal, 'portal_quickinstaller')

        if qi.isProductInstalled(product_name):
            qi.uninstallProducts([product_name, ], reinstall=True)
            qi.installProducts([product_name], reinstall=True)
            output.append('{}: Successfully reinstalled {}'.format(portal.id, product_name))
        return '\n'.join(output)


class uninstallPloneProduct(grok.View):
    """ Uninstall a product passed by form parameter in the current Plone site. """
    grok.context(IPloneSiteRoot)
    grok.name('uninstall_product')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if not portal:
            portal = api.portal.get()

        product_name = self.request.form['product_name']
        output = []
        qi = getToolByName(portal, 'portal_quickinstaller')

        if qi.isProductInstalled(product_name):
            qi.uninstallProducts([product_name, ], reinstall=False)
            output.append('{}: Successfully uninstalled {}'.format(portal.id, product_name))
        return '\n'.join(output)


class upgradePloneVersion(grok.View):
    """ Upgrade to the latest Plone version in code """
    grok.context(IPloneSiteRoot)
    grok.name('upgrade_plone_version')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if not portal:
            portal = api.portal.get()
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)
        # pm = getattr(self.context, 'portal_migration')
        pm = api.portal.get_tool('portal_migration')
        self.request.method = 'POST'
        report = pm.upgrade(
            REQUEST=self.request,
            dry_run=False,
        )
        return report


class setupPAMAgain(grok.View):
    """ Reinstalls a product passed by form parameter in the current Plone site. """
    grok.context(IPloneSiteRoot)
    grok.name('setup_pam_again')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if not portal:
            portal = api.portal.get()

        from plone.app.multilingual.browser.setup import SetupMultilingualSite
        setupTool = SetupMultilingualSite()
        setupTool.setupSite(self.context, False)


class deleteNavPortletFromRoot(grok.View):
    """ Delete NavPortlet from Root """
    grok.context(IPloneSiteRoot)
    grok.name('delete_navportlet_from_root')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if not portal:
            portal = api.portal.get()

        # Delete default Navigation portlet on root
        target_manager_root = queryUtility(IPortletManager, name='plone.leftcolumn', context=portal)
        target_manager_root_assignments = getMultiAdapter((portal, target_manager_root), IPortletAssignmentMapping)
        if 'navigation' in target_manager_root_assignments:
            del target_manager_root_assignments['navigation']


class reinstallGWTinyTemplates(grok.View):
    """ Reinstalls all TinyMCE Templates """
    grok.context(IPloneSiteRoot)
    grok.name('reinstall_gw_tiny_templates')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)
        if not portal:
            portal = api.portal.get()

        templates = portal.get('templates', None)
        if templates:
            self.delete_templates(templates)
            for plt in get_plantilles():
                plantilla = self.create_content(templates, 'Document', normalizeString(plt['titol']), title=plt['titol'], description=plt['resum'])
                plantilla.text = IRichText['text'].fromUnicode(plt['cos'])
                plantilla.reindexObject()

    def delete_templates(self, templates):
        for template in templates.objectIds():
            api.content.delete(obj=templates[template])

    def create_content(self, container, portal_type, id, publish=True, **kwargs):
        if not getattr(container, id, False):
            obj = createContentInContainer(container, portal_type, checkConstraints=False, **kwargs)
            if publish:
                self.publish_content(obj)
        return getattr(container, id)

    def publish_content(self, context):
        """ Make the content visible either in both possible genweb.simple and
            genweb.review workflows.
        """
        pw = getToolByName(context, "portal_workflow")
        object_workflow = pw.getWorkflowsFor(context)[0].id
        object_status = pw.getStatusOf(object_workflow, context)
        if object_status:
            api.content.transition(obj=context, transition={'genweb_simple': 'publish', 'genweb_review': 'publicaalaintranet'}[object_workflow])


class removeDuplicatedGenwebSettings(grok.View):
    """ Remove duplicate (old) Genweb UPC settings in Control Panel """
    grok.context(Interface)
    grok.name('remove_duplicated_genweb_settings')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if not portal:
            portal = api.portal.get()

        portal_controlpanel = api.portal.get_tool('portal_controlpanel')
        portal_controlpanel.unregisterConfiglet('genweb')


class reapplyRegistryProfile(grok.View):
    """ ReapplyRegistryProfile """
    grok.context(Interface)
    grok.name('reapply_registry_profile')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if not portal:
            portal = api.portal.get()

        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)

        setupInstallProfile('profile-genweb.core:default', ['plone.app.registry'])

        # Should work this better
        # name = 'genweb.hidden_settings.languages_applied'
        # from plone.registry.field import Bool
        # value = True
        # registry = getUtility(IRegistry)
        # from plone.registry.record import Record as RegistryRecord
        # registry.records[name] = RegistryRecord(Bool(), value)
        # import transaction
        # transaction.commit()

        api.portal.set_registry_record('genweb.hidden_settings.languages_applied', True)
        return api.portal.get_registry_record(name='genweb.hidden_settings.languages_applied')


class PACUseNewViewNames(grok.View):
    """ Uninstall a product passed by form parameter in the current Plone site """
    grok.context(IPloneSiteRoot)
    grok.name('pac_use_new_view_names')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if not portal:
            portal = api.portal.get()

        output = []

        use_new_view_names(portal)

        return '\n'.join(output)


class importTypesTool(grok.View):
    """ ImportTypesTool """
    grok.context(IPloneSiteRoot)
    grok.name('import_types_tool')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        portal = api.portal.get()
        ps = getToolByName(portal, 'portal_setup')
        ps.runImportStepFromProfile('profile-genweb.upc:default', 'typeinfo')


class applyOldJS(grok.View):
    """ applyOldJS """
    grok.context(IPloneSiteRoot)
    grok.name('apply_old_js')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        output = []
        portal = api.portal.get()
        oldfiles = ['++resource++plone.app.jquery.js', 'jquery-integration.js',
                    'insert-after', 'event-registration.js', 'register_function.js',
                    'plone_javascript_variables.js',
                    '++resource++plone.app.jquerytools.js',
                    '++resource++plone.app.jquerytools.form.js',
                    'collapsibleformfields.js',
                    '++resource++plone.app.jquerytools.overlayhelpers.js',
                    '++resource++plone.app.jquerytools.dateinput.js',
                    '++resource++plone.app.jquerytools.rangeinput.js',
                    '++resource++plone.app.jquerytools.validator.js',
                    '++resource++plone.app.jquerytools.plugins.js',
                    '++resource++plone.app.jquerytools.tooltip.js',
                    '++resource++plone.app.jquerytools.tooltip.plugins.js',
                    'nodeutilities.js', 'cookie_functions.js', 'modernizr.js',
                    '++bootstrap++js/modernizr-2.6.1.min.js', 'livesearch.js',
                    '++resource++search.js', 'fullscreenmode.js', 'select_all.js',
                    'dragdropreorder.js', 'mark_special_links.js',
                    'collapsiblesections.js', 'form_tabbing.js', 'popupforms.js',
                    'jquery.highlightsearchterms.js', 'first_input_focus.js',
                    'accessibility.js', 'styleswitcher.js', 'toc.js',
                    '++resource++plone.app.discussion.javascripts/comments.js',
                    'dropdown.js', 'inline_validation.js', 'kss-bbb.js',
                    '++genwebupc++js/plone.formwidget.querystring.querywidget.js',
                    'collective.js.jqueryui.custom.min.js',
                    '++resource++collective.polls/js/jquery.flot.js',
                    '++resource++collective.polls/js/jquery.flot.pie.js',
                    '++resource++collective.polls/js/polls.js',
                    '++resource++collective.polls/js/collective.poll.js',
                    '++resource++plone.formwidget.recaptcha/recaptcha_ajax.js',
                    '++resource++plone.formwidget.recurrence/jquery.tmpl-beta1.js',
                    '++resource++plone.formwidget.recurrence/jquery.recurrenceinput.js',
                    '++resource++plone.app.event/event.js',
                    '++resource++plone.app.event.portlet_calendar.js',
                    '++resource++plone.formwidget.autocomplete/jquery.autocomplete.min.js',
                    '++resource++plone.formwidget.autocomplete/formwidget-autocomplete.js',
                    '++resource++plone.formwidget.contenttree/contenttree.js',
                    '++resource++jsi18n.js', 'table_sorter.js', 'calendar_formfield.js',
                    'formUnload.js', 'formsubmithelpers.js', 'unlockOnFormUnload.js',
                    'jquery.tinymce.js', 'tiny_mce_gzip.js',
                    '++resource++collective.polls/js/jquery.tasksplease.js',
                    '++resource++collage-resources/collage.js',
                    '++resource++collective.polls/js/excanvas.min.js',
                    '++resource++collective.z3cform.datagridfield/datagridfield.js',
                    '++bootstrap++js/bootstrap.min.js']
        js = api.portal.get_tool('portal_javascripts')
        for oldfile in oldfiles:
            if oldfile in js.getResourcesDict():
                jsfile = js.getResource(oldfile)
                if not jsfile.getEnabled():
                    jsfile.setEnabled(True)
        import transaction
        transaction.commit()
        output.append('{}: Applied old js files'.format(portal.id))
        return '\n'.join(output)


class importCSSRegistry(grok.View):
    """ importCSSRegistry """
    grok.context(IPloneSiteRoot)
    grok.name('import_css_registry')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        portal = api.portal.get()
        ps = getToolByName(portal, 'portal_setup')
        ps.runImportStepFromProfile('profile-genweb.upc:default', 'cssregistry')


class PortalSetupImport(grok.View):
    """
    Go to portal setup, select profile and import step.
    URL parameters:
      - step: id of the step to import, e.g. 'portlets'.
      - profile: id of the profile or snapshot to select, e.g. 'genweb.upc'.
      - profile_type: type of the selected profile, 'default' by default.
    """
    grok.context(IPloneSiteRoot)
    grok.name('portal_setup_import')
    grok.require('cmf.ManagePortal')

    DEFAULT_PROFILE_TYPE = 'default'

    def render(self):
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)
        portal = api.portal.get()
        ps = getToolByName(portal, 'portal_setup')
        params = self._parse_params()
        ps.runImportStepFromProfile(
            'profile-{profile}:{profile_type}'.format(**params),
            params['step'])
        return ('{step} from {profile}:{profile_type} '
                'successfully imported').format(**params)

    def _parse_params(self):
        if 'step' not in self.request.form:
            raise ValueError("Mandatory parameter 'step' was not specified")
        if 'profile' not in self.request.form:
            raise ValueError("Mandatory parameter 'profile' was not specified")
        step = self.request.form['step']
        profile = self.request.form['profile']
        profile_type = self.request.form.get(
            'profile_type', PortalSetupImport.DEFAULT_PROFILE_TYPE)
        return dict(step=step, profile=profile, profile_type=profile_type)


class changeNewsEventsPortlets(grok.View):
    """ Replace navigation portlet by categories portlet from news and events
    view methods in the current Plone site. """
    grok.context(IPloneSiteRoot)
    grok.name('replace_nav_portlet')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        output = []
        portal = api.portal.get()

        ps = getToolByName(portal, 'portal_setup')
        ps.runImportStepFromProfile('profile-genweb.theme:default', 'portlets')

        portal_ca = portal['ca']
        portal_es = portal['es']
        portal_en = portal['en']

        self.disinherit_from_parent(portal_ca, portal_es, portal_en)

        self.assign_news_events_listing_portlet(portal_ca['noticies'], 'News')
        self.assign_news_events_listing_portlet(portal_ca['esdeveniments'], 'Events')
        self.assign_news_events_listing_portlet(portal_es['noticias'], 'News')
        self.assign_news_events_listing_portlet(portal_es['eventos'], 'Events')
        self.assign_news_events_listing_portlet(portal_en['news'], 'News')
        self.assign_news_events_listing_portlet(portal_en['events'], 'Events')

        # Set layout for news folders
        portal_en['news'].setLayout('news_listing')
        portal_es['noticias'].setLayout('news_listing')
        portal_ca['noticies'].setLayout('news_listing')

        # Set layout for events folders
        portal_en['events'].setLayout('event_listing')
        portal_es['eventos'].setLayout('event_listing')
        portal_ca['esdeveniments'].setLayout('event_listing')

        import transaction
        transaction.commit()

        output.append('{}: Successfully replaced news_events_listing portlet'.format(portal.id))
        return '\n'.join(output)

    def disinherit_from_parent(self, portal_ca, portal_es, portal_en):
        # Blacklist the left column on portal_ca['noticies'] and portal_ca['esdeveniments'],
        # portal_es['noticias'] and portal_es['eventos'],
        # portal_en['news'] and portal_en['events']
        left_manager = queryUtility(IPortletManager, name=u'plone.leftcolumn')
        blacklist_ca = getMultiAdapter((portal_ca['noticies'], left_manager), ILocalPortletAssignmentManager)
        blacklist_ca.setBlacklistStatus(CONTEXT_CATEGORY, True)
        blacklist_ca = getMultiAdapter((portal_ca['esdeveniments'], left_manager), ILocalPortletAssignmentManager)
        blacklist_ca.setBlacklistStatus(CONTEXT_CATEGORY, True)
        blacklist_es = getMultiAdapter((portal_es['noticias'], left_manager), ILocalPortletAssignmentManager)
        blacklist_es.setBlacklistStatus(CONTEXT_CATEGORY, True)
        blacklist_es = getMultiAdapter((portal_es['eventos'], left_manager), ILocalPortletAssignmentManager)
        blacklist_es.setBlacklistStatus(CONTEXT_CATEGORY, True)
        blacklist_en = getMultiAdapter((portal_en['news'], left_manager), ILocalPortletAssignmentManager)
        blacklist_en.setBlacklistStatus(CONTEXT_CATEGORY, True)
        blacklist_en = getMultiAdapter((portal_en['events'], left_manager), ILocalPortletAssignmentManager)
        blacklist_en.setBlacklistStatus(CONTEXT_CATEGORY, True)

    def assign_news_events_listing_portlet(self, portal, obj_type):
        from genweb.theme.portlets.news_events_listing import Assignment as news_events_Assignment

        target_manager_left = queryUtility(IPortletManager, name='plone.leftcolumn', context=portal)
        target_manager_assignments_left = getMultiAdapter((portal, target_manager_left), IPortletAssignmentMapping)
        for portlet in target_manager_assignments_left:
            del target_manager_assignments_left[portlet]
        if 'news_events_listing' not in target_manager_assignments_left:
            target_manager_assignments_left['news_events_listing'] = news_events_Assignment([], obj_type)


class setSitemapDepth(grok.View):
    """ Set 3 levels of sitemap  """
    grok.context(IPloneSiteRoot)
    grok.name('set_sitemap_depth')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        output = []
        portal = api.portal.get()
        navtree_props = portal.portal_properties.navtree_properties
        navtree_props.sitemapDepth = 4
        import transaction
        transaction.commit()
        output.append('{}: Successfully setted 3 levels in sitemap'.format(portal.id))
        return '\n'.join(output)


class removeOldIconCollection(grok.View):
    """ Remove old icon collection """
    grok.context(IPloneSiteRoot)
    grok.name('remove_old_icon_collection')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        output = []
        portal = api.portal.get()
        file = '++resource++collection.css'
        css = api.portal.get_tool('portal_css')
        css.manage_removeStylesheet(file)
        import transaction
        transaction.commit()
        output.append('{}: Successfully css class removed'.format(portal.id))
        return '\n'.join(output)


class removeOldJSCollection(grok.View):
    """ Remove old js collection: ++resource++plone.formwidget.querystring.querywidget.js"""
    grok.context(IPloneSiteRoot)
    grok.name('remove_old_js_collection')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        output = []
        portal = api.portal.get()
        oldfile = '++resource++plone.formwidget.querystring.querywidget.js'
        js = api.portal.get_tool('portal_javascripts')
        js.manage_removeScript(oldfile)
        newfile = '++genwebupc++js/plone.formwidget.querystring.querywidget.js'
        if newfile in js.getResourcesDict():
            jsfile = js.getResource(newfile)
            if not jsfile.getEnabled():
                jsfile.setEnabled('True')
        else:
            js.manage_addScript(newfile)
            jsfile = js.getResource(newfile)
            jsfile.setEnabled('True')
        js.moveResourceAfter(newfile, "kss-bbb.js")
        import transaction
        transaction.commit()
        output.append('{}: Successfully oldjs file removed and newjs added'.format(portal.id))
        return '\n'.join(output)


class updateLIF_LRF(grok.View):
    """ Update view methods for LIf and LRF types in the current Plone site """
    grok.context(IPloneSiteRoot)
    grok.name('update_lif_lrf')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if not portal:
            portal = api.portal.get()

        output = []
        portal.portal_types['LIF'].view_methods = ('listing_view', 'summary_view', 'tabular_view', 'full_view', 'album_view')
        portal.portal_types['LIF'].default_view = 'tabular_view'
        portal.portal_types['LRF'].view_methods = ('listing_view', 'summary_view', 'tabular_view', 'full_view', 'album_view')
        portal.portal_types['LRF'].default_view = 'tabular_view'
        import transaction
        transaction.commit()
        output.append('{}: Successfully reinstalled'.format(portal.id))
        return '\n'.join(output)


class reinstallGenwebUPCWithLanguages(grok.View):
    """ Reinstalls genweb.upc keeping published languages in the current Plone site. """
    grok.context(IPloneSiteRoot)
    grok.name('reinstall_genweb_upc_with_languages')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)
        defaultLanguage = api.portal.get_default_language()
        languages = api.portal.get_registry_record(name='genweb.controlpanel.interface.IGenwebControlPanelSettings.idiomes_publicats')
        context = aq_inner(self.context)
        output = []
        qi = getToolByName(context, 'portal_quickinstaller')

        if qi.isProductInstalled('genweb.upc'):
            qi.uninstallProducts(['genweb.upc'], reinstall=True)
            qi.installProducts(['genweb.upc'], reinstall=True)
            pl = api.portal.get_tool('portal_languages')
            pl.setDefaultLanguage(defaultLanguage)
            pl.supported_langs = ['ca', 'es', 'en']
            api.portal.set_registry_record(name='genweb.controlpanel.interface.IGenwebControlPanelSettings.idiomes_publicats', value=languages)
            output.append('{}: Successfully reinstalled genweb upc'.format(context))
        return '\n'.join(output)


class importTinyMCE4GenwebUPC(grok.View):
    """ ImportTinyMCE4GenwebUPC """
    grok.context(IPloneSiteRoot)
    grok.name('import_tinymce')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)
        portal = api.portal.get()
        ps = getToolByName(portal, 'portal_setup')
        ps.runImportStepFromProfile('profile-genweb.upc:default', 'tinymce_settings')


class defaultHtmlConfig(grok.View):
    """ DefaultHtmlConfig """
    grok.context(IPloneSiteRoot)
    grok.name('default_html_config')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)

        from plone import api
        from Products.PortalTransforms.Transform import make_config_persistent

        tid = 'safe_html'

        pt = api.portal.get_tool(name='portal_transforms')
        if not tid in pt.objectIds():
            return

        trans = pt[tid]

        tconfig = trans._config
        tconfig['remove_javascript'] = 1
        tconfig['nasty_tags'] = {'meta': '1', 'style': '1'}
        tconfig['stripped_tags'] = ['fieldset', 'form', 'input', 'label',
                                    'legend', 'link', 'noscript', 'optgroup',
                                    'option', 'select', 'style', 'textarea']
        tconfig['custom_tags'] = ['applet', 'article', 'aside', 'audio',
                                  'canvas', 'command', 'datalist', 'details',
                                  'dialog', 'embed', 'figure', 'footer',
                                  'header', 'hgroup', 'iframe', 'keygen',
                                  'mark', 'meter', 'nav', 'output', 'progress',
                                  'rp', 'rt', 'ruby', 'section', 'source',
                                  'time', 'u', 'video']
        tconfig['stripped_attributes'] = ['lang', 'halign', 'border',
                                          'frame', 'rules', 'bgcolor']
        tconfig['stripped_combinations'] = {}
        tconfig['style_whitelist'] = ['text-align', 'list-style-type', 'float',
                                      'width', 'height', 'padding-left',
                                      'padding-right', 'text-decoration']
        tconfig['class_blacklist'] = []
        tconfig['valid_tags'] = {
            'code': '1', 'meter': '1', 'tbody': '1', 'style': '1', 'img': '0',
            'title': '1', 'tt': '1', 'tr': '1', 'param': '1', 'li': '1',
            'source': '1', 'tfoot': '1', 'th': '1', 'td': '1', 'dl': '1',
            'blockquote': '1', 'big': '1', 'dd': '1', 'kbd': '1', 'dt': '1',
            'p': '1', 'small': '1', 'output': '1', 'div': '1', 'em': '1',
            'datalist': '1', 'hgroup': '1', 'video': '1', 'rt': '1', 'canvas': '1',
            'rp': '1', 'sub': '1', 'bdo': '1', 'sup': '1', 'progress': '1',
            'body': '1', 'acronym': '1', 'base': '0', 'br': '0', 'address': '1',
            'article': '1', 'strong': '1', 'ol': '1', 'script': '1', 'caption': '1',
            'dialog': '1', 'col': '1', 'h2': '1', 'h3': '1', 'h1': '1', 'h6': '1',
            'h4': '1', 'h5': '1', 'header': '1', 'table': '1', 'span': '1',
            'area': '0', 'mark': '1', 'dfn': '1', 'var': '1', 'cite': '1',
            'thead': '1', 'head': '1', 'hr': '0', 'link': '1', 'ruby': '1',
            'b': '1', 'colgroup': '1', 'keygen': '1', 'ul': '1', 'del': '1',
            'iframe': '1', 'embed': '1', 'pre': '1', 'figure': '1', 'ins': '1',
            'aside': '1', 'html': '1', 'nav': '1', 'details': '1', 'u': '1',
            'samp': '1', 'map': '1', 'object': '1', 'a': '1', 'footer': '1',
            'i': '1', 'q': '1', 'command': '1', 'time': '1', 'audio': '1',
            'section': '1', 'abbr': '1', 'meta': '0', 'applet': '1', 'button': '1'}
        make_config_persistent(tconfig)
        trans._p_changed = True
        trans.reload()
        output = []
        output.append('Default HTML Configuration for safe_html applied')
        return '\n'.join(output)


class reindexAllPages(grok.View):
    """ reindexAllPages """
    grok.context(IPloneSiteRoot)
    grok.name('reindex_all_pages')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        output = []
        portal = api.portal.get()
        context = aq_inner(self.context)
        pc = getToolByName(context, 'portal_catalog')
        brains = pc.searchResults(portal_type='Document')
        for result in brains:
            obj = result.getObject()
            obj.reindexObject()
        import transaction
        transaction.commit()
        output.append('{}: Documents successfully reindexed'.format(portal.id))
        return '\n'.join(output)


class addPermissionsContributor(grok.View):
    """ add permission to folder contentes when rol is Contributor """
    grok.context(IPloneSiteRoot)
    grok.name('add_permissions_contributor')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)
        output = []
        portal = api.portal.get()
        roles_of_permission = portal.rolesOfPermission('List folder contents')
        portlets = portal.rolesOfPermission('Portlets: Manage portlets')
        output.append('PREVIOUS (List folder contents): name = {}, selected = {}'.format(roles_of_permission[2]['name'], roles_of_permission[2]['selected']))
        output.append('PREVIOUS (Portlets: Manage portlets): name = {}, selected = {}'.format(portlets[2]['name'], portlets[2]['selected']))
        ps = getToolByName(portal, 'portal_setup')
        ps.runImportStepFromProfile('profile-genweb.core:default', 'rolemap')
        roles_of_permission = portal.rolesOfPermission('List folder contents')
        portlets = portal.rolesOfPermission('Portlets: Manage portlets')
        output.append('AFTER (List folder contents): name = {}, selected = {}'.format(roles_of_permission[2]['name'], roles_of_permission[2]['selected']))
        output.append('AFTER (Portlets: Manage portlets): name = {}, selected = {}'.format(portlets[2]['name'], portlets[2]['selected']))
        output.append('{}: Permissions added'.format(portal.id))
        return '\n'.join(output)


class setFolderIndexViewasDefault(grok.View):
    """ Set all folders views of this site with the view passed by param """
    grok.context(IPloneSiteRoot)
    grok.name('set_folder_default_view')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        output = []
        context = aq_inner(self.context)
        view_method = self.request.form['view_method']
        pc = getToolByName(context, 'portal_catalog')
        brains = pc.searchResults(portal_type='Folder')
        for result in brains:
            obj = result.getObject()
            if obj.getDefaultPage() is None:
                obj.setLayout(view_method)
        import transaction
        transaction.commit()
        output.append('{}: Folder view successfully changed'.format(api.portal.get().id))
        return '\n'.join(output)


class addLinkIntoFolderNews(grok.View):
    """ addLinkIntoFolderNews """
    grok.context(IPloneSiteRoot)
    grok.name('add_link2news')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        output = []
        portal = api.portal.get()
        noticies = portal['ca']['noticies']
        noticias = portal['es']['noticias']
        news = portal['en']['news']
        from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
        behavior = ISelectableConstrainTypes(noticies)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(('News Item', 'Folder', 'Image', 'Link'))
        behavior.setImmediatelyAddableTypes(('News Item', 'Folder', 'Image', 'Link'))
        behavior = ISelectableConstrainTypes(noticias)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(('News Item', 'Folder', 'Image', 'Link'))
        behavior.setImmediatelyAddableTypes(('News Item', 'Folder', 'Image', 'Link'))
        behavior = ISelectableConstrainTypes(news)
        behavior.setConstrainTypesMode(1)
        behavior.setLocallyAllowedTypes(('News Item', 'Folder', 'Image', 'Link'))
        behavior.setImmediatelyAddableTypes(('News Item', 'Folder', 'Image', 'Link'))
        import transaction
        transaction.commit()
        output.append('{}: Link type added successfully to news folder in'.format(portal.id))
        return '\n'.join(output)


class refactorAggregatorNewsCollection(grok.View):
    """ refactorAggregatorNewsCollection """
    grok.context(IPloneSiteRoot)
    grok.name('refactor_news_collection')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        output = []
        NEWS_QUERY = [{'i': u'portal_type', 'o': u'plone.app.querystring.operation.selection.is', 'v': [u'News Item', u'Link']},
                      {'i': u'review_state', 'o': u'plone.app.querystring.operation.selection.is', 'v': [u'published']},
                      {'i': u'path', 'o': u'plone.app.querystring.operation.string.relativePath', 'v': u'..'}]
        portal = api.portal.get()
        noticies = portal['ca']['noticies']['aggregator']
        noticias = portal['es']['noticias']['aggregator']
        news = portal['en']['news']['aggregator']
        noticies.query = NEWS_QUERY
        noticias.query = NEWS_QUERY
        news.query = NEWS_QUERY
        import transaction
        transaction.commit()
        output.append('{}: Aggregator News collection successfully updated in'.format(portal.id))
        return '\n'.join(output)


class translateNews(grok.View):
    """ translate title and description spanish news"""
    grok.context(IPloneSiteRoot)
    grok.name('translate_news')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        output = []
        portal = api.portal.get()
        newsfolder = portal['es']['noticias']
        newsfolder.setTitle('Noticias')
        newsfolder.setDescription('Noticias del sitio')
        newsfolder.reindexObject()

        output.append('{}: Successfully translated news'.format(portal.id))
        return '\n'.join(output)


class bulkChangeCreator(grok.View):
    """ If the creator of the content is X, change it to Y """
    grok.context(IFolder)
    grok.name('bulk_change_creator')
    grok.require('cmf.ManagePortal')

    STATUS_oldcreators = u"You must select one old creator."
    STATUS_newcreators = u"You must select one new creator."
    STATUS_samecreator = u"You must select different creators."
    STATUS_updated = u"%s objects updated."
    status = []

    @property
    def catalog(self):
        return api.portal.get_tool(name='portal_catalog')

    @property
    def membership(self):
        return api.portal.get_tool(name='portal_membership')

    def old_creator(self):
        return self.request.form.get('old_creator', '')

    def new_creator(self):
        return self.request.form.get('new_creator', '')

    def change_modification_date(self):
        return self.request.form.get('change_modification_date', False)

    def get_sorted_list(self, user_list, user_old, user_id_lambda):
        ret_list = []
        for user in user_list:
            if not user:
                continue
            userid = user_id_lambda(user)
            info = self.membership.getMemberInfo(userid)
            if info and info['fullname']:
                d = dict(id=userid, name="%s (%s)" %
                         (info['fullname'], userid))
            else:
                d = dict(id=userid, name=userid)
            d['selected'] = 1 if userid in user_old else 0
            ret_list.append(d)
        ret_list.sort(lambda a, b:
                      cmp(str(a['id']).lower(), str(b['id']).lower()))
        return ret_list

    def list_creators(self):
        creator_list = []
        for brain in self.catalog(path=self.context.absolute_url_path()):
            creators = brain.getObject().listCreators()
            for creator in creators:
                if creator not in creator_list:
                    creator_list.append(creator)
        return self.get_sorted_list(
            creator_list,  # list of creators
            self.old_creator(),  # prev selected creators
            lambda element: element)

    def render(self):
        """ Main method """

        if 'submit' in self.request.form:

            old_creator = self.old_creator()
            new_creator = self.new_creator()
            change_modification_date = self.change_modification_date()
            self.status = []

            ok = True
            if old_creator == '':
                self.status.append(self.STATUS_oldcreators)
                ok = False
            if new_creator == '':
                self.status.append(self.STATUS_newcreators)
                ok = False
            if old_creator == new_creator:
                self.status.append(self.STATUS_samecreator)
                ok = False

            if ok:
                count = 0
                acl_users = getattr(self.context, 'acl_users')
                user = acl_users.getUserById(new_creator)

                valid_user = True
                if user is None:
                    user = self.membership.getMemberById(new_creator)
                    if user is None:
                        valid_user = False
                        self.status.append('WARNING: Could not find '
                                           'user %s !' % new_creator)

                header_index = len(self.status)
                self.status.append('')
                abspath = self.context.absolute_url_path()
                for brain in self.catalog(path=abspath):
                    obj = brain.getObject()
                    creators = list(obj.listCreators())
                    if old_creator in creators:
                        if valid_user:
                            obj.changeOwnership(user)
                        if new_creator in creators:
                            index1 = creators.index(old_creator)
                            index2 = creators.index(new_creator)
                            creators[min(index1, index2)] = new_creator
                            del creators[max(index1, index2)]
                        else:
                            creators[creators.index(old_creator)] = new_creator

                        obj.setCreators(creators)
                        if change_modification_date:
                            obj.reindexObject()
                        else:
                            old_modification_date = obj.ModificationDate()
                            obj.reindexObject()
                            obj.setModificationDate(old_modification_date)
                            obj.reindexObject(idxs=['modified'])

                        self.status.append(brain.getPath())
                        count += 1

                self.status[header_index] = self.STATUS_updated % count

        return ViewPageTemplateFile('helpers_touchers_templates'
                                    '/bulk_change_creator.pt')(self)
