# -*- coding: utf-8 -*-
from five import grok
from plone import api
from Acquisition import aq_inner
from App.config import getConfiguration
from OFS.interfaces import IFolder
from OFS.interfaces import IApplication
from zope.interface import Interface
from zope.component import queryUtility
from zope.interface import alsoProvides

from plone.subrequest import subrequest
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IMutableUUID

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from genweb.core import HAS_DXCT
from genweb.core import HAS_PAM
from genweb.core.interfaces import IHomePage
from genweb.core.interfaces import IProtectedContent

import json


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
        import ipdb; ipdb.set_trace() # Magic! Do not delete!!! :)


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
    config = getConfiguration()
    configuration = config.product_config.get('genwebconfig', dict())
    zeo = configuration.get('zeo')
    return zeo


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
    """ Funció que agafa el numero de zeo al que esta assignat la instancia de
        genweb. Per aixo, el buildout s'ha d'afegir una linea a la zope-conf-
        additional:
        zope-conf-additional =
                <product-config genweb>
                    zeo 9
                </product-config>
    """
    grok.name('getZEO')
    grok.context(Interface)
    grok.require('zope2.View')

    def dorsal(self):
        config = getConfiguration()
        configuration = config.product_config.get('genwebconfig', dict())
        zeo = configuration.get('zeo')
        return zeo

    def nomDorsal(self):
        return DORSALS[self.dorsal()]


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
        cacheserver = 'http://sylar.upc.es:90%02d' % int(getDorsal())
        cachepurginsettings.cachingProxies = (cacheserver,)

        return 'Configuracio de cache importada correctament.'


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
