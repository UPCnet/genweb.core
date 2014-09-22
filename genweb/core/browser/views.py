from five import grok
from plone import api
from itertools import chain

from zope.interface import Interface
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.component.hooks import getSite

from plone.app.contenttypes.interfaces import IDocument

from plone.registry.interfaces import IRegistry

from genweb.core.interfaces import IGenwebLayer

import json


class GetDXDocumentText(grok.View):
    grok.context(IDocument)
    grok.name('genweb.get.dxdocument.text')
    grok.require('zope2.View')

    def render(self):
        return self.context.text.output


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

                portal_catalog = api.portal.get_tool('portal_catalog')
                portal_path = '/'.join(api.portal.get().getPhysicalPath())
                paths = []

                for p in templateDirectories:
                    if p.startswith('/'):
                        p = p[1:]
                    paths.append("%s/%s" % (portal_path, p,))

                results = portal_catalog.searchResults(Language='', path=paths, object_provides=IDocument.__identifier__)

                for r in results:
                    templates.append([r.Title, "%s/genweb.get.dxdocument.text" % r.getURL(), r.Description])

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
            fulluserinfo = hunter.merge(chain(*[hunter.searchUsers(**{field: query}) for field in ['fullname', 'name']]), 'userid')
            values = [dict(id=userinfo.get('login'), text=userinfo.get('title')) for userinfo in fulluserinfo]
            results['results'] = values
            return json.dumps(results)
        else:
            return json.dumps({"error": "No query found"})
