from five import grok

from zope.interface import Interface
from zope.interface import implements
from zope.component import queryUtility
from zope.app.component.hooks import getSite
from zope.publisher.interfaces import IPublishTraverse, NotFound

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.LinguaPlone.interfaces import ITranslatable
from Products.ATContentTypes.interfaces.document import IATDocument

from plone.app.uuid.utils import uuidToObject
from plone.registry.interfaces import IRegistry

from genweb.core.browser.viewlets import addQuery
from genweb.core.interfaces import IGenwebLayer

try:
    import json
except ImportError:
    from simplejson import json

NOT_TRANSLATED_YET_VIEW = 'not_translated_yet'


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
            url = self.wrapDestination(destination.absolute_url())
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

                for r in portal_catalog(Language='all', path=paths, object_provides=IATDocument.__identifier__):
                    templates.append([r.Title, "%s/getText" % r.getURL(), r.Description])

        return u"var tinyMCETemplateList = %s;" % json.dumps(templates)
