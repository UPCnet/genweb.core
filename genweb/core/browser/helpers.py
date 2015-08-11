# -*- coding: utf-8 -*-
from five import grok
from plone import api
from Acquisition import aq_inner
from App.config import getConfiguration
from OFS.interfaces import IFolder
from OFS.interfaces import IApplication
from zope.interface import Interface
from zope.component import queryUtility
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.event import notify

from Products.PluggableAuthService.interfaces.plugins import IPropertiesPlugin

from plone.dexterity.interfaces import IDexterityContent
from Products.Archetypes.interfaces import IBaseObject
from plone.dexterity.utils import createContentInContainer
from Products.CMFPlone.utils import normalizeString
from plone.app.contenttypes.behaviors.richtext import IRichText

from plone.dexterity.content import Container
from plone.subrequest import subrequest
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IMutableUUID
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from Products.PluggableAuthService.events import PropertiesUpdated
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.transforms.pdf_to_text import pdf_to_text
from Products.PythonScripts.standard import url_quote

from repoze.catalog.query import Eq
from souper.interfaces import ICatalogFactory
from souper.soup import get_soup
from souper.soup import Record

from genweb.core import HAS_DXCT
from genweb.core import HAS_PAM
from genweb.core.utils import json_response
from genweb.core.interfaces import IHomePage
from genweb.core.interfaces import IProtectedContent
from genweb.core.utils import add_user_to_catalog
from genweb.core.utils import reset_user_catalog
from genweb.core.browser.plantilles import get_plantilles

import json
import os
import urllib


if HAS_PAM:
    from plone.app.multilingual.browser.setup import SetupMultilingualSite


DORSALS = {"1": "Ter Stegen", "2": "Montoya", "3": "Piqué",
           "4": "Rakitic", "5": "Busquets", "6": "Xavi", "7": "Pedro",
           "8": "Iniesta", "9": "Suárez", "10": "Messi", "11": "Neymar JR",
           "12": "Rafinha", "13": "Bravo", "14": "Mascherano", "15": "Bartra"}


class debug(grok.View):
    """ Convenience view for faster degugging. Needs to be manager. """
    grok.context(Interface)
    grok.require('cmf.ManagePortal')

    def render(self):
        context = aq_inner(self.context)
        # Magic Victor debug view do not delete!
        import ipdb; ipdb.set_trace()  # Magic! Do not delete!!! :)


class monitoringView(grok.View):
    """ Convenience view for monitoring software """
    grok.name('ping')
    grok.context(IApplication)
    grok.require('zope2.View')

    def render(self):
        return '1'


class protectContent(grok.View):
    """ Makes the context a content protected. It could only be deleted by
        managers.
    """
    grok.context(Interface)
    grok.require('cmf.ManagePortal')

    def render(self):
        context = aq_inner(self.context)
        alsoProvides(context, IProtectedContent)


class instanceindevelmode(grok.View):
    """ This instance is in development mode """
    grok.context(Interface)
    grok.require('zope2.View')

    __allow_access_to_unprotected_subobjects__ = True

    def render(self):
        return api.env.debug_mode()


def getDorsal():
    return os.environ.get('dorsal', False)


def listPloneSites(zope):
    out = []
    for item in zope.values():
        if IFolder.providedBy(item) and not IPloneSiteRoot.providedBy(item):
            for site in item.values():
                if IPloneSiteRoot.providedBy(site):
                    out.append(site)
        elif IPloneSiteRoot.providedBy(item):
            out.append(item)
    return out


class getZEO(grok.View):
    """ This view is used to know the dorsal (the Genweb enviroment) assigned to
        this instance.
    """
    grok.name('getZEO')
    grok.context(Interface)
    grok.require('zope2.View')

    def dorsal(self):
        return os.environ.get('dorsal', False)

    def nomDorsal(self):
        dorsal = self.dorsal()
        if dorsal:
            return DORSALS[self.dorsal()]
        else:
            return 'N/A'


class listPloneSitesView(grok.View):
    grok.name('listPloneSites')
    grok.context(IApplication)
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        out = []
        for item in context.values():
            #if IPloneSiteRoot.providedBy(item):
            #    out.append(item)
            if IFolder.providedBy(item):
                for site in item.values():
                    if IPloneSiteRoot.providedBy(site):
                        out.append(item.id + '/' + site.id)
        return json.dumps(out)


class getFlavourSitesView(grok.View):
    grok.name('getFlavourSites')
    grok.context(IApplication)
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        plonesites = listPloneSites(context)
        out = {}
        for plonesite in plonesites:
            portal_skins = getToolByName(plonesite, 'portal_skins')
            out[plonesite.id] = portal_skins.getDefaultSkin()
        return json.dumps(out)


class getFlavourSiteView(grok.View):
    grok.name('getFlavourSite')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        portal_skins = getToolByName(context, 'portal_skins')
        return portal_skins.getDefaultSkin()


class getLanguagesSitesView(grok.View):
    grok.name('getLanguagesSites')
    grok.context(IApplication)
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        plonesites = listPloneSites(context)
        out = {}
        for plonesite in plonesites:
            portal_languages = getToolByName(plonesite, 'portal_languages')
            out[plonesite.id] = portal_languages.getSupportedLanguages()
        return json.dumps(out)


class getDefaultLanguageSitesView(grok.View):
    grok.name('getDefaultLanguageSites')
    grok.context(IApplication)
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        plonesites = listPloneSites(context)
        out = {}
        for plonesite in plonesites:
            portal_languages = getToolByName(plonesite, 'portal_languages')
            out[plonesite.id] = portal_languages.getDefaultLanguage()
        return json.dumps(out)


class getDefaultWFSitesView(grok.View):
    grok.name('getDefaultWFSites')
    grok.context(IApplication)
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        plonesites = listPloneSites(context)
        out = {}
        for plonesite in plonesites:
            portal_workflow = getToolByName(plonesite, 'portal_workflow')
            out[plonesite.id] = portal_workflow.getDefaultChain()
        return json.dumps(out)


class configuraSiteCache(grok.View):
    """ Vista que configura la caché del site corresponent. """
    grok.name('configuraSiteCache')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        from Products.GenericSetup.tests.common import DummyImportContext
        from plone.app.registry.exportimport.handler import RegistryImporter
        from genweb.core.browser.cachesettings import cacheprofile
        from plone.cachepurging.interfaces import ICachePurgingSettings
        contextImport = DummyImportContext(context, purge=False)
        registry = queryUtility(IRegistry)
        importer = RegistryImporter(registry, contextImport)
        importer.importDocument(cacheprofile)

        cachepurginsettings = registry.forInterface(ICachePurgingSettings)

        varnish_url = os.environ.get('varnish_url', False)
        if varnish_url:
            cachepurginsettings.cachingProxies = (varnish_url,)
            return 'Successfully set caching for this site.'
        else:
            return 'There aren\'t any varnish_url in the environment, no caching proxy could be configured.'


class listLDAPInfo(grok.View):
    grok.name('listLDAPInfo')
    grok.context(IApplication)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        plonesites = listPloneSites(context)
        out = {}
        for plonesite in plonesites:
            acl_users = getToolByName(plonesite, 'acl_users')
            try:
                out[plonesite.id] = acl_users.ldapUPC.acl_users.getServers()
            except:
                print "Plonesite %s doesn't have a valid ldapUPC instance." % plonesite.id
        return json.dumps(out)


class matagetHTTPCacheheaders(grok.View):
    """ Canvia el portal_type dels objectes del PloneSurvey que tinguin espais en el nom del tipus"""

    grok.name('matagetHTTPCacheheaders')
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

    grok.name('removeBrokenCacheFu')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        from plone.app.upgrade.v40.alphas import removeBrokenCacheFu
        context = aq_inner(self.context)

        removeBrokenCacheFu(context)

        return 'done'


class MakeMeaHomePage(grok.View):
    grok.name('makemeahomepage')
    grok.context(Interface)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        alsoProvides(self.context, IHomePage)
        if HAS_DXCT:
            from plone.app.contenttypes.interfaces import IFolder
            if IFolder.providedBy(self.context):
                self.context.setLayout('homepage')
        return self.request.response.redirect(self.context.absolute_url())


class MakeMeaSubHomePage(grok.View):
    grok.name('makemeasubhomepage')
    grok.context(Interface)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        alsoProvides(self.context, IHomePage)
        if HAS_DXCT:
            from plone.app.contenttypes.interfaces import IFolder
            if IFolder.providedBy(self.context):
                self.context.setLayout('subhomepage')
        return self.request.response.redirect(self.context.absolute_url())


class BulkUserCreator(grok.View):
    """
        Convenience bulk user creator. It requires parametrization in code and
        eventually, run this over a debug instance in production.
    """
    grok.name('bulkusercreator')
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
                'jose.marcos.lopez',]

        for user in users:
            # password = user[0].upper() + user.split('.')[1][0].upper() + user.split('.')[1][1:]

            if not api.user.get(username=user):
                api.user.create(email=user+'@upc.edu',
                                username=user,
                                password='1234')

        return 'Done.'


class BulkUserEraser(grok.View):
    """
        Convenience bulk user eraser. It requires parametrization in code and
        eventually, run this over a debug instance in production.
    """
    grok.name('bulkusereraser')
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
                'jose.marcos.lopez',]

        for user in users:

            if api.user.get(username=user):
                api.user.delete(username=user)
                print("Deleted user {}".format(user))

        return 'Done.'


class ListLastLogin(grok.View):
    """ List the last_login information for all the users in this site. """
    grok.context(IPloneSiteRoot)
    grok.require('genweb.webmaster')

    def render(self):
        pmd = api.portal.get_tool(name='portal_memberdata')
        pm = api.portal.get_tool(name='portal_membership')

        output = []
        for user in pmd._members.items():
            wrapped_user = pm.getMemberById(user[0])
            if wrapped_user:
                fullname = wrapped_user.getProperty('fullname')
                if not fullname:
                    fullname = wrapped_user.getProperty('id')
                last_login = wrapped_user.getProperty('last_login_time')
                output.append('{}; {}'.format(fullname, last_login))
        return '\n'.join(output)


class ReinstallGWControlPanel(grok.View):
    """ Reinstalls genweb.controlpanel in the current Plone site. """
    grok.context(IPloneSiteRoot)
    grok.name('reinstall_gwcontrolpanel')
    grok.require('cmf.ManagePortal')

    def render(self):
        context = aq_inner(self.context)
        output = []
        qi = getToolByName(context, 'portal_quickinstaller')

        if qi.isProductInstalled('genweb.controlpanel'):
            qi.uninstallProducts(['genweb.controlpanel'], reinstall=True)
            qi.installProducts(['genweb.controlpanel'], reinstall=True)
            output.append('{}: Successfully reinstalled control panel'.format(context))
        return '\n'.join(output)


class BulkReinstallGWControlPanel(grok.View):
    """
        Reinstall genweb.controlpanel in all the Plone instance of this Zope.
        Useful when added some parameter to the control panel and you want to
        apply it at the same time in all the existing Plone sites in the Zope.
    """
    grok.context(IApplication)
    grok.name('bulk_reinstall_gwcontrolpanel')
    grok.require('cmf.ManagePortal')

    def render(self):
        context = aq_inner(self.context)
        plonesites = listPloneSites(context)
        output = []
        for plonesite in plonesites:
            response = subrequest('/'.join(plonesite.getPhysicalPath()) + '/reinstall_gwcontrolpanel')
            output.append(response.getBody())
        return '\n'.join(output)


class ResetLanguage(grok.View):
    """
        Re-set the language of each LRF according to its name. Execute in an LRF.
    """
    grok.context(Interface)
    grok.name('resetlanguage')
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


class MirrorUIDs(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('mirroruids')
    grok.require('cmf.ManagePortal')

    def update(self):
        portal = self.context
        form = self.request.form
        self.output = []
        if self.request['method'] == 'POST' and form.get('origin_root_path', False):
            origin_root_path = form.get('origin_root_path')
            destination_root_path = '/'.join(portal.getPhysicalPath())
            origin_portal = portal.restrictedTraverse(origin_root_path)
            # Get all eligible objects
            if HAS_PAM:
                all_objects = origin_portal.portal_catalog.searchResults(path=origin_root_path)
            else:
                all_objects = origin_portal.portal_catalog.searchResults(path=origin_root_path, Language='all')
            for obj in all_objects:
                # Check if exist a match object by path in destination
                destination_obj = portal.unrestrictedTraverse(obj.getPath().replace(origin_root_path, destination_root_path), False)
                if destination_obj:
                    origin_uuid = obj.UID
                    IMutableUUID(destination_obj).set(str(origin_uuid))
                    destination_obj.reindexObject()
                    self.output.append('{0} -> {1}'.format(destination_obj.absolute_url(), origin_uuid))
                    print '{0} -> {1}'.format(destination_obj.absolute_url(), origin_uuid)
            self.output = '<br/>'.join(self.output)


class MirrorStates(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('mirrorstates')
    grok.require('cmf.ManagePortal')
    grok.template('mirroruids')

    def update(self):
        portal = self.context
        form = self.request.form
        self.output = []
        if self.request['method'] == 'POST' and form.get('origin_root_path', False):
            origin_root_path = form.get('origin_root_path')
            destination_root_path = '/'.join(portal.getPhysicalPath())
            origin_portal = portal.restrictedTraverse(origin_root_path)

            # States translation table from genweb_review to genweb_simple
            states = {'esborrany': 'visible', 'intranet': 'intranet', 'pending': 'pending', 'private': 'private', 'published': 'published', 'restricted-to-managers': 'restricted-to-managers'}

            # Get all eligible objects
            if HAS_PAM:
                all_objects = origin_portal.portal_catalog.searchResults(path=origin_root_path)
            else:
                all_objects = origin_portal.portal_catalog.searchResults(path=origin_root_path, Language='all')
            for obj in all_objects:
                # Check if exist a match object by path in destination
                destination_obj = portal.unrestrictedTraverse(obj.getPath().replace(origin_root_path, destination_root_path), False)
                if destination_obj:
                    origin_state = obj.review_state
                    if origin_state and origin_state != 'Missing.Value' and origin_state in states.keys():
                        api.content.transition(obj=destination_obj, to_state=states[origin_state])

                    try:
                        destination_obj.reindexObject()
                    except:
                        print "##### Not able to reindex %s" % obj.getURL()

                    self.output.append('{0} -> {1}'.format(destination_obj.absolute_url(), origin_state))
                    print '{0} -> {1}'.format(destination_obj.absolute_url(), origin_state)
            self.output = '<br/>'.join(self.output)


    def __call__(self):
        portal = self.context
        form = self.request.form
        self.output = []
        HAS_PAM = False
        states = {'esborrany': 'visible', 'intranet': 'intranet', 'pending': 'pending', 'private': 'private', 'published': 'published', 'restricted-to-managers': 'restricted-to-managers'}
        if self.request['method'] == 'POST' and form.get('origin_root_path', False):
            origin_root_path = form.get('origin_root_path')
            destination_root_path = '/'.join(portal.getPhysicalPath())
            origin_portal = portal.restrictedTraverse(origin_root_path)
            # Get all eligible objects
            if HAS_PAM:
                all_objects = origin_portal.portal_catalog.searchResults(path=origin_root_path)
            else:
                all_objects = origin_portal.portal_catalog.searchResults(path=origin_root_path, Language='all')
            for obj in all_objects:
                # Check if exist a match object by path in destination
                destination_obj = portal.unrestrictedTraverse(obj.getPath().replace(origin_root_path, destination_root_path), False)
                if destination_obj:
                    origin_state = obj.review_state
                    if origin_state and origin_state != 'Missing.Value' and origin_state in states.keys():
                        api.content.transition(obj=destination_obj, to_state=states[origin_state])

                    try:
                        destination_obj.reindexObject()
                    except:
                        print "##### Not able to reindex %s" % obj.getURL()
                    self.output.append('{0} -> {1}'.format(destination_obj.absolute_url(), origin_state))
                    print '{0} -> {1}'.format(destination_obj.absolute_url(), origin_state)
            self.output = '<br/>'.join(self.output)


class MigrateRLF(grok.View):
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


class MigrateRLF2roundFIGHT(grok.View):
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


class ReBuildUserPropertiesCatalog(grok.View):
    """
        Rebuild the OMEGA13 repoze.catalog for user properties data.
    """
    grok.context(IPloneSiteRoot)
    grok.name('rebuild_user_catalog')
    grok.require('cmf.ManagePortal')

    def render(self):
        context = aq_inner(self.context)
        portal = api.portal.get()
        plugins = portal.acl_users.plugins.listPlugins(IPropertiesPlugin)
        # We use the most preferent plugin
        pplugin = plugins[0][1]
        all_user_properties = pplugin.enumerateUsers()

        for user in all_user_properties:
            user.update(dict(username=user['id']))
            if 'title' in user:
                user.update(dict(fullname=user['title']))
            else:
                user.update(dict(fullname=user['fullname']))

            user_obj = api.user.get(user['id'])

            if user_obj:
                add_user_to_catalog(user_obj, user)
            else:
                print('No user found in user repository (LDAP) {}'.format(user['id']))

            print('Updated properties catalog for {}'.format(user['id']))


class ResetUserPropertiesCatalog(grok.View):
    """
        Reset the OMEGA13 repoze.catalog for user properties data.
    """
    grok.context(IPloneSiteRoot)
    grok.name('reset_user_catalog')
    grok.require('cmf.ManagePortal')

    def render(self):
        reset_user_catalog()


class UserPropertiesCatalogViewer(grok.View):
    """
        Rebuild the OMEGA13 repoze.catalog for user properties data.
    """
    grok.context(IPloneSiteRoot)
    grok.name('view_user_catalog')
    grok.require('cmf.ManagePortal')

    @json_response
    def render(self):
        context = aq_inner(self.context)
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


class enablePDFIndexing(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('enable_pdf_transform')
    grok.require('cmf.ManagePortal')

    def render(self):
        pt = api.portal.get_tool('portal_transforms')
        pt.registerTransform(pdf_to_text())

        return 'Done'


class GetRenderedStylesheets(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('get_rendered_stylesheets')
    grok.require('cmf.ManagePortal')

    @json_response
    def render(self):
        registry = self.context.portal_css
        registry_url = registry.absolute_url()
        context = aq_inner(self.context)

        styles = registry.getEvaluatedResources(context)
        skinname = url_quote(self.skinname())
        result = []
        for style in styles:
            rendering = style.getRendering()
            if style.isExternalResource():
                src = "%s" % style.getId()
            else:
                src = "%s/%s/%s" % (registry_url, skinname, style.getId())
            if rendering == 'link':
                data = {'rendering': rendering,
                        'media': style.getMedia(),
                        'rel': style.getRel(),
                        'title': style.getTitle(),
                        'conditionalcomment': style.getConditionalcomment(),
                        'src': src}
            elif rendering == 'import':
                data = {'rendering': rendering,
                        'media': style.getMedia(),
                        'conditionalcomment': style.getConditionalcomment(),
                        'src': src}
            elif rendering == 'inline':
                content = registry.getInlineResource(style.getId(), context)
                data = {'rendering': rendering,
                        'media': style.getMedia(),
                        'conditionalcomment': style.getConditionalcomment(),
                        'content': content}
            else:
                raise ValueError("Unkown rendering method '%s' for style '%s'" % (rendering, style.getId()))
            result.append(data['src'])
        return result

    def skinname(self):
        return aq_inner(self.context).getCurrentSkinName()


class BulkExecuteScriptView(grok.View):
    """
        Execute one action view in all instances passed as a form parameter
    """
    grok.context(IApplication)
    grok.name('bulk_action')
    grok.require('cmf.ManagePortal')

    def render(self):
        context = aq_inner(self.context)
        args = self.request.form
        view_name = self.request.form['view']
        plonesites = listPloneSites(context)
        output = []
        for plonesite in plonesites:
            print('======================')
            print('Executed view in {}'.format(plonesite.id))
            print('======================')
            quoted_args = urllib.urlencode(args)
            response = subrequest('/'.join(plonesite.getPhysicalPath()) + '/{}?{}'.format(view_name, quoted_args))
            output.append(response.getBody())

            output.append('Executed view {} in site {}'.format(view_name, plonesite.id))
            output.append('-----------------------------------------------')
        return '\n'.join(output)


class ReinstallPloneProduct(grok.View):
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


class NotSubProcessedBulkExecuteScriptView(grok.View):
    """
        Execute one action view in all instances passed as a form parameter used
        only in case that something does not work making a subrequest!
    """
    grok.context(IApplication)
    grok.name('nsp_bulk_action')
    grok.require('cmf.ManagePortal')

    def render(self):
        context = aq_inner(self.context)
        args = self.request.form
        view_name = self.request.form['view']
        plonesites = listPloneSites(context)
        output = []
        for plonesite in plonesites:
            view = plonesite.restrictedTraverse(view_name)
            view.render(plonesite, **args)
            output.append('Executed view {} in site {}'.format(view_name, plonesite.id))
        return '\n'.join(output)


class SetupPAMAgain(grok.View):
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


class DeleteNavPortletFromRoot(grok.View):
    """ Reinstalls a product passed by form parameter in the current Plone site. """
    grok.context(IPloneSiteRoot)
    grok.name('delete_nav_portlet_from_root')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        if not portal:
            portal = api.portal.get()

        # Delete default Navigation portlet on root
        target_manager_root = queryUtility(IPortletManager, name='plone.leftcolumn', context=portal)
        target_manager_root_assignments = getMultiAdapter((portal, target_manager_root), IPortletAssignmentMapping)
        if 'navigation' in target_manager_root_assignments:
            del target_manager_root_assignments['navigation']


class ReinstallGWTinyTemplates(grok.View):
    """
        Reinstalls all TinyMCE Templates
    """
    grok.context(IPloneSiteRoot)
    grok.name('reinstall_tiny_templates')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
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
