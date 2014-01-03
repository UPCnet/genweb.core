from five import grok
from itertools import chain

from zope.interface import Interface
from zope.interface import implements
from zope.interface import alsoProvides
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.publisher.interfaces import IPublishTraverse, NotFound

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.ATContentTypes.interfaces.document import IATDocument

from plone.app.uuid.utils import uuidToObject
from plone.registry.interfaces import IRegistry

from genweb.core import ITranslatable
from genweb.core.interfaces import IHomePage
from genweb.core.interfaces import IGenwebLayer
from genweb.core.browser.viewlets import addQuery

import json
import pkg_resources

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_DXCT = False
else:
    HAS_DXCT = True
    from plone.dexterity.utils import createContentInContainer


NOT_TRANSLATED_YET_VIEW = 'not_translated_yet'


class setupDX(grok.View):
    """ Setup View that fixes p.a.ct front-page
    """
    grok.name('setupdxctsite')
    grok.context(Interface)
    grok.require('cmf.ManagePortal')

    def render(self):
        if HAS_DXCT:
            portal = getSite()
            pl = getToolByName(portal, 'portal_languages')
            if getattr(portal, 'front-page', False):
                portal.manage_delObjects('front-page')
                frontpage = createContentInContainer(portal, 'Document', title=u"front-page", checkConstraints=False)
                alsoProvides(frontpage, IHomePage)
                frontpage.exclude_from_nav = True
                frontpage.language = pl.getDefaultLanguage()
                frontpage.reindexObject()
            # Set the default page to the homepage view
            portal.setDefaultPage('homepage')
            return self.request.response.redirect(portal.absolute_url())
        else:
            return 'This site has no p.a.contenttypes installed.'


class universalLink(BrowserView):
    """ Redirects the user to the negotiated translated page
        based on the user preferences in the user's browser.
    """

    implements(IPublishTraverse)

    def __init__(self, context, request):
        super(universalLink, self).__init__(context, request)
        self.tg = None
        self.lang = None

    def publishTraverse(self, request, name):

        if self.tg is None:  # ../@@universal-link/translationgroup
            self.tg = name
        elif self.lang is None:  # ../@@universal-link/translationgroup/lang
            self.lang = name
        else:
            raise NotFound(self, name, request)

        return self

    def getDestination(self):
        # Look for the element
        translatable = ITranslatable(uuidToObject(self.tg), None)
        if translatable is not None:
            translations = translatable.getTranslations()
        else:
            translations = []

        if self.lang:
            destination = translations.get(self.lang, None)
        else:
            # The negotiated language
            ltool = getToolByName(self.context, 'portal_languages')
            if len(ltool.getRequestLanguages()) > 0:
                language = ltool.getRequestLanguages()[0]
                destination = translations.get(language, None)

        return destination

    def __call__(self):
        destination = self.getDestination()
        if not destination:
            destination = getSite()

        self.request.RESPONSE.redirect(destination.absolute_url())


class selectorView(universalLink):
    """ View that redirects to a concrete translation given an UUID and a
        destination language.
    """
    def getDialogDestination(self):
        """Get the "not translated yet" dialog URL.
        """
        dialog_view = '/' + NOT_TRANSLATED_YET_VIEW
        postpath = False
        # The dialog view shouldn't appear on the site root
        # because that is untraslatable by default.
        # And since we are mapping the root on itself,
        # we also do postpath insertion (@@search case)
        if ISiteRoot.providedBy(self.context):
            dialog_view = ''
            postpath = True

        url = self.context.absolute_url()

        return self.wrapDestination(url + dialog_view, postpath=postpath)

    def wrapDestination(self, url, postpath=True):
        """Fix the translation url appending the query
        and the eventual append path.
        """
        if postpath:
            url += self.request.form.get('post_path', '')
        return addQuery(
            self.request,
            url,
            exclude=('post_path')
        )

    def __call__(self):
        destination = self.getDestination()
        if destination:
            # We have a direct translation, full wrapping
            # Destination is a list
            url = self.wrapDestination(destination[0].absolute_url())
        else:
            url = self.getDialogDestination()

        self.request.RESPONSE.redirect(url)


class not_translated_yet(grok.View):
    """ View to inform user that the view requested is not translated yet,
        and shows the already translated related content.
    """
    grok.context(Interface)
    grok.require('zope2.View')
    grok.layer(IGenwebLayer)

    def already_translated(self):
        return self.context.getTranslations().items()

    def has_any_translation(self):
        return len(self.context.getTranslations().items()) > 1


class TemplateList(grok.View):
    """ Override of the default way of obtaining the TinyMCE template list """
    grok.context(Interface)
    grok.name('collective.tinymcetemplates.templatelist')
    grok.require('zope2.View')
    grok.layer(IGenwebLayer)

    def render(self):
        self.request.response.setHeader('Content-Type', 'text/javascript')
        registry = queryUtility(IRegistry)
        templates = []
        if registry is not None:
            templateDirectories = registry.get('collective.tinymcetemplates.templateLocations', None)
            if templateDirectories:

                portal_catalog = getToolByName(self.context, 'portal_catalog')
                portal_url = getToolByName(self.context, 'portal_url')

                portal_path = '/'.join(portal_url.getPortalObject().getPhysicalPath())
                paths = []
                for p in templateDirectories:
                    if p.startswith('/'):
                        p = p[1:]
                    paths.append("%s/%s" % (portal_path, p,))
                ats = portal_catalog(Language='all', path=paths, object_provides=IATDocument.__identifier__)
                dexts = portal_catalog(Language='all', path=paths, object_provides='Products.CMFCore.interfaces._content.IContentish')

                results = ats + dexts
                for r in results:
                    templates.append([r.Title, "%s/getText" % r.getURL(), r.Description])

        return u"var tinyMCETemplateList = %s;" % json.dumps(templates)


class AjaxUserSearch(grok.View):
    grok.context(Interface)
    grok.name('genweb.ajaxusersearch')
    grok.require('genweb.authenticated')
    grok.layer(IGenwebLayer)

    def render(self):
        self.request.response.setHeader("Content-type", "application/json")
        query = self.request.form.get('q', '')
        results = dict(more=False, results=[])
        if query:
            portal = getSite()
            hunter = getMultiAdapter((portal, self.request), name='pas_search')
            fulluserinfo = hunter.merge(chain(*[hunter.searchUsers(**{field: query}) for field in ['name', 'fullname']]), 'userid')
            values = [dict(id=userinfo.get('login'), text=userinfo.get('title')) for userinfo in fulluserinfo]
            results['results'] = values
            return json.dumps(results)
        else:
            return json.dumps({"error": "No query found"})
