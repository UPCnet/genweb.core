# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from App.config import getConfiguration
from Products.CMFPlone.interfaces import IPloneSiteRoot
from OFS.interfaces import IFolder
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from five import grok
from OFS.interfaces import IApplication
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
import json


DORSALS = {"1": "Víctor Valdés", "2": "Dani Alves", "3": "Piqué",
           "4": "Cesc", "5": "Puyol", "6": "Xavi", "7": "David Villa",
           "8": "A. Iniesta", "9": "Alexis", "10": "Messi", "11": "Thiago",
           "12": "Unknown", "13": "Pinto", "14": "Mascherano", "15": "Keita",
           "16": "Sergio", "17": "Pedro"}


def getDorsal():
    config = getConfiguration()
    configuration = config.product_config.get('genwebconfig', dict())
    zeo = configuration.get('zeo')
    return zeo


def listPloneSites(zope):
    out = []
    for item in zope.values():
        if IFolder.providedBy(item):
            for site in item.values():
                if IPloneSiteRoot.providedBy(site):
                    out.append(site)
    return out


class getZEO(BrowserView):
    """ Funció que agafa el numero de zeo al que esta assignat la instancia de genweb.
        Per aixo, el buildout s'ha d'afegir una linea a la zope-conf-additional:
        zope-conf-additional =
           <product-config genweb>
               zeo 9
           </product-config>
    """

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
