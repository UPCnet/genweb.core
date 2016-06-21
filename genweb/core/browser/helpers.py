# -*- coding: utf-8 -*-
from five import grok
from plone import api
from Acquisition import aq_inner
from OFS.interfaces import IFolder
from OFS.interfaces import IApplication
from zope.interface import Interface
from zope.component import queryUtility
from zope.interface import alsoProvides
import json
import os
import urllib
import pkg_resources

from plone.subrequest import subrequest
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IMutableUUID

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName

from genweb.core import HAS_PAM
from genweb.core.interfaces import IProtectedContent

try:
    pkg_resources.get_distribution('plone4.csrffixes')
except pkg_resources.DistributionNotFound:
    CSRF = False
else:
    from plone.protect.interfaces import IDisableCSRFProtection
    CSRF = True


def setupInstallProfile(profileid, steps=None):
    """Installs the generic setup profile identified by ``profileid``.
    If a list step names is passed with ``steps`` (e.g. ['actions']),
    only those steps are installed. All steps are installed by default.
    """
    setup = api.portal.get_tool('portal_setup')
    if steps is None:
        setup.runAllImportStepsFromProfile(profileid, purge_old=False)
    else:
        for step in steps:
            setup.runImportStepFromProfile(profileid,
                                           step,
                                           run_dependencies=False,
                                           purge_old=False)


class debug(grok.View):
    """ Convenience view for faster debugging. Needs to be manager. """
    grok.context(Interface)
    grok.require('cmf.ManagePortal')

    def render(self):
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)
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
        from plone.protect.interfaces import IDisableCSRFProtection
        alsoProvides(self.request, IDisableCSRFProtection)
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
    """ Returns Zeo dorsal """
    return os.environ.get('dorsal', False)


def listPloneSites(zope):
    """ List the available plonesites to be used by other function """
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
    """ [DEPRECATED] Redirect to getZOPE """
    grok.name('getZEO')
    grok.context(Interface)
    grok.require('zope2.View')

    def render(self):
        self.request.response.redirect('getZOPE')


class getZOPE(grok.View):
    """ This view is used to know the dorsal (the Genweb enviroment) assigned to
        this instance.
    """
    grok.name('getZOPE')
    grok.context(Interface)
    grok.require('zope2.View')
    grok.template('getzope')

    def dorsal(self):
        dorsal = os.environ.get('dorsal', False)
        if dorsal == '':
            return 'NaN'
        else:
            return dorsal


class listPloneSitesView(grok.View):
    """ Returns a list with the available plonesites in this Zope """
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
    """ Returns the last layer installed for each plonesite """
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
    """ Returns the last layer installed in this plonesite """
    grok.name('getFlavourSite')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')

    def render(self):
        context = aq_inner(self.context)
        portal_skins = getToolByName(context, 'portal_skins')
        return portal_skins.getDefaultSkin()


class getLanguagesSitesView(grok.View):
    """ Returns the last layer installed in this plonesite """
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
    """ Returns default language for each plonesite """
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
    """ Returns default workflow for each plonesite """
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


class mirrorUIDs(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('mirrorUIDs')
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


class mirrorStates(grok.View):
    grok.context(IPloneSiteRoot)
    grok.name('mirrorStates')
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


class bulkExecuteScriptView(grok.View):
    """ Execute one action view in all instances passed as a form parameter """
    grok.context(IApplication)
    grok.name('bulkAction')
    grok.require('cmf.ManagePortal')

    def render(self):
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)
        context = aq_inner(self.context)
        args = self.request.form
        view_name = self.request.form['view']
        exclude_sites = self.request.form.get('exclude_sites', '').split(',')
        plonesites = listPloneSites(context)
        output = []
        for plonesite in plonesites:
            if plonesite.id not in exclude_sites:
                print('======================')
                print('Executing view in {}'.format(plonesite.id))
                print('======================')
                quoted_args = urllib.urlencode(args)
                response = subrequest('/'.join(plonesite.getPhysicalPath()) + '/{}?{}'.format(view_name, quoted_args))
                output.append("""-- Executed view {} in site {} --<br/>""".format(view_name, plonesite.id))
                output.append(response.getBody())
        return '\n'.join(output)


class notSubProcessedBulkExecuteScriptView(grok.View):
    """
        Execute one action view in all instances passed as a form parameter used
        only in case that something does not work making a subrequest!
    """
    grok.context(IApplication)
    grok.name('nspBulkAction')
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


class fixRecord(grok.View):
    """ Fix KeyError problem when plonesite is moved from the original Zeo"""
    grok.context(IPloneSiteRoot)
    grok.name('fixRecord')
    grok.require('cmf.ManagePortal')

    def render(self, portal=None):
        from zope.component import getUtility
        if CSRF:
            alsoProvides(self.request, IDisableCSRFProtection)
        output = []
        site = self.context.portal_registry
        registry = getUtility(IRegistry)
        rec = registry.records
        keys = [a for a in rec.keys()]
        for k in keys:
            try:
                rec[k]
            except:
                output.append('{}, '.format(k))
                del site.portal_registry.records._values[k]
                del site.portal_registry.records._fields[k]
        return "S'han purgat les entrades del registre: {}".format(output)
