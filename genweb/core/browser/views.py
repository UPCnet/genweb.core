# -*- coding: utf-8 -*-
from five import grok
from plone import api
from itertools import chain
from zExceptions import NotFound

from Acquisition import aq_inner

from zope.interface import Interface
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.component.hooks import getSite

from plone.app.contenttypes.interfaces import IDocument
from plone.dexterity.interfaces import IDexterityContent
from plone.registry.interfaces import IRegistry

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone.interfaces import IPloneSiteRoot

from genweb.core.interfaces import IGenwebLayer
from genweb.core.adapters import IImportant
from genweb.core.adapters import IFlash
from genweb.core.adapters import IOutOfList

from souper.soup import get_soup
from souper.soup import Record
from repoze.catalog.query import Eq

from genweb.core import GenwebMessageFactory as _

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
                    paths.append('%s/%s' % (portal_path, p,))

                # Primer les de SCP i després les custom (templates)
                templatesSCP = portal_catalog.searchResults(Language='',
                                                            path=paths[0],
                                                            object_provides=IDocument.__identifier__,
                                                            sort_on='getObjPositionInParent')

                # I després les custom (plantilles)
                templatesCustom = portal_catalog.searchResults(Language='',
                                                               path=paths[1],
                                                               object_provides=IDocument.__identifier__,
                                                               sort_on='getObjPositionInParent')

                results = templatesSCP + templatesCustom

                for r in results:
                    templates.append([r.Title, '%s/genweb.get.dxdocument.text' % r.getURL(), r.Description])

        return u'var tinyMCETemplateList = %s;' % json.dumps(templates)


class AjaxUserSearch(grok.View):
    grok.context(Interface)
    grok.name('genweb.ajaxusersearch')
    grok.require('genweb.authenticated')
    grok.layer(IGenwebLayer)

    def render(self):
        self.request.response.setHeader('Content-type', 'application/json')
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
            return json.dumps({'error': 'No query found'})


class SendToFormOverride(grok.View):
    grok.context(Interface)
    grok.name('sendto_form')
    grok.require('zope2.Public')
    grok.layer(IGenwebLayer)

    def render(self):
        raise NotFound


class gwToggleIsImportant(grok.View):
    grok.context(IDexterityContent)
    grok.name('toggle_important')
    grok.require('cmf.ModifyPortalContent')
    grok.layer(IGenwebLayer)

    def render(self):
        context = aq_inner(self.context)
        is_important = IImportant(context).is_important
        if is_important:
            IImportant(context).is_important = False
            confirm = _(u'L\'element s\'ha desmarcat com important')
        else:
            IImportant(context).is_important = True
            confirm = _(u'L\'element s\'ha marcat com important')

        IStatusMessage(self.request).addStatusMessage(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url())


class gwToggleIsFlash(grok.View):
    grok.context(IDexterityContent)
    grok.name('toggle_flash')
    grok.require('cmf.ModifyPortalContent')
    grok.layer(IGenwebLayer)

    def render(self):
        context = aq_inner(self.context)
        is_flash = IFlash(context).is_flash
        if is_flash:
            IFlash(context).is_flash = False
            confirm = _(u'L\'element s\'ha desmarcat com flash')
        else:
            IFlash(context).is_flash = True
            confirm = _(u'L\'element s\'ha marcat com flash')

        IStatusMessage(self.request).addStatusMessage(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url())


class gwToggleIsOutoflist(grok.View):
    grok.context(IDexterityContent)
    grok.name('toggle_outoflist')
    grok.require('cmf.ModifyPortalContent')
    grok.layer(IGenwebLayer)

    def render(self):
        context = aq_inner(self.context)
        is_outoflist = IOutOfList(context).is_outoflist
        if is_outoflist:
            IOutOfList(context).is_outoflist = False
            confirm = _(u'L\'element s\'ha desmarcat de la blacklist')
        else:
            IOutOfList(context).is_outoflist = True
            confirm = _(u'L\'element s\'ha marcat com a blacklist')

        IStatusMessage(self.request).addStatusMessage(confirm, type='info')
        self.request.response.redirect(self.context.absolute_url())


class gwToggleSubscribedTag(grok.View):
    grok.context(Interface)
    grok.name('toggle_subscriptiontag')
    grok.require('genweb.authenticated')
    grok.layer(IGenwebLayer)

    def render(self):
        portal = getSite()
        current_user = api.user.get_current()
        userid = current_user.id
        tag = self.request.form['tag']
        soup_tags = get_soup('user_subscribed_tags', portal)
        exist = [r for r in soup_tags.query(Eq('id', userid))]

        if not exist:
            record = Record()
            record.attrs['id'] = userid
            record.attrs['tags'] = [tag]
            soup_tags.add(record)
        else:
            subscribed = [True for utag in exist[0].attrs['tags'] if utag == tag]
            if subscribed:
                exist[0].attrs['tags'].remove(tag)
            else:
                exist[0].attrs['tags'].append(tag)
        soup_tags.reindex()

        if IPloneSiteRoot.providedBy(self.context):
            self.request.response.redirect(self.context.absolute_url()+'/alltags')
        else:
            self.request.response.redirect(self.context.absolute_url())
