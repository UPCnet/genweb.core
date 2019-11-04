# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.statusmessages.interfaces import IStatusMessage

from five import grok
from itertools import chain
from plone import api
from plone.app.contenttypes.interfaces import IDocument
from plone.dexterity.interfaces import IDexterityContent
from plone.registry.interfaces import IRegistry
from repoze.catalog.query import Eq
from souper.soup import Record
from souper.soup import get_soup
from zExceptions import NotFound
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.interface import Interface

from genweb.core import GenwebMessageFactory as _
from genweb.core.adapters import IFlash
from genweb.core.adapters import IImportant
from genweb.core.adapters import IOutOfList
from genweb.core.adapters import IShowInApp
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
        templates = {}

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

                templates['1. Destacats'] = [['Destacat', 'http://localhost:8080/170/etsab/templates/destacat/genweb.get.dxdocument.text', 'Text destacat.'],
                                             ['Destacat color', 'http://localhost:8080/170/etsab/templates/destacat-color/genweb.get.dxdocument.text', 'Destacat amb text m\xc3\xa9s gran i color.'],
                                             ['Destacat contorn', 'http://localhost:8080/170/etsab/templates/destacat-contorn/genweb.get.dxdocument.text', 'Destacat amb text petit.'],
                                             ['Pou', 'http://localhost:8080/170/etsab/templates/pou/genweb.get.dxdocument.text', 'Contenidor de pou per encabir elements i limitar-los visualment.'],
                                             ['Pou degradat', 'http://localhost:8080/170/etsab/templates/pou-degradat/genweb.get.dxdocument.text', 'Contenidor de pou per encabir elements i limitar-los visualment amb fons degradat.'],
                                             ['Caixa', 'http://localhost:8080/170/etsab/templates/caixa/genweb.get.dxdocument.text', 'Contenidor de caixa per encabir elements i limitar-los visualment.'],
                                             ['Caixa degradat', 'http://localhost:8080/170/etsab/templates/caixa-degradat/genweb.get.dxdocument.text', 'Contenidor de caixa per encabir elements i limitar-los visualment amb fons degradat.']]

                templates['2. Columnes'] = [['Dues columnes de text', 'http://localhost:8080/170/etsab/templates/dues-columnes-de-text/genweb.get.dxdocument.text', "A cada columna s'hi poden afegir altres plantilles."],
                                            ['Combinacions de columnes', 'http://localhost:8080/170/etsab/templates/combinacions-de-columnes/genweb.get.dxdocument.text', "Podeu fer d'1 a 4 columnes i fusionar-les entre elles. Elimineu les combinacions que no us interessin i treballeu amb el columnat que us agradi m\xc3\xa9s."]]

                templates['3. Continguts (Text, botons, bàners, Llistats)'] = [['Llistat \xc3\xadndex', 'http://localhost:8080/170/etsab/templates/llistat-index/genweb.get.dxdocument.text', '\xc3\x8dndex de continguts.'],
                                                                               ['Llistat enlla\xc3\xa7os', 'http://localhost:8080/170/etsab/templates/llistat-enllacos/genweb.get.dxdocument.text', "Per afegir un llistat d'enlla\xc3\xa7os relacionats."],
                                                                               ['Llistat destacat', 'http://localhost:8080/170/etsab/templates/llistat-destacat/genweb.get.dxdocument.text', "Per afegir un llistat d'enlla\xc3\xa7os destacats."],
                                                                               ['Text amb tots els titulars', 'http://localhost:8080/170/etsab/templates/text-amb-tots-els-titulars/genweb.get.dxdocument.text', 'Com utilitzar la jerarquia de t\xc3\xadtols. \xc3\x89s important respectar aquesta jerarquia si volem ser accessibles i millorar el nostre posicionament a Internet.'],
                                                                               ['Text amb video', 'http://localhost:8080/170/etsab/templates/text-amb-video/genweb.get.dxdocument.text', "Per inserir-hi el vostre v\xc3\xaddeo heu d'accedir al codi html de la p\xc3\xa0gina i substituir l'enlla\xc3\xa7 al v\xc3\xaddeo."],
                                                                               ['Assenyalar enlla\xc3\xa7os', 'http://localhost:8080/170/etsab/templates/assenyalar-enllacos/genweb.get.dxdocument.text', "Classes que es poden afegir als enlla\xc3\xa7os per indicar el tipus d'element enlla\xc3\xa7at."],
                                                                               ['Bot\xc3\xb3 ample blau', 'http://localhost:8080/170/etsab/templates/boto-ample-blau/genweb.get.dxdocument.text', "Bot\xc3\xb3 standard blau que ocupa el 100% de l'ample del contenidor"],
                                                                               ['Bot\xc3\xb3 ample gris', 'http://localhost:8080/170/etsab/templates/boto-ample-gris/genweb.get.dxdocument.text', "Bot\xc3\xb3 standard gris que ocupa el 100% de l'ample del contenidor"],
                                                                               ['Bot\xc3\xb3 blau', 'http://localhost:8080/170/etsab/templates/boto-blau/genweb.get.dxdocument.text', 'Bot\xc3\xb3 standard blau'],
                                                                               ['Bot\xc3\xb3', 'http://localhost:8080/170/etsab/templates/boto/genweb.get.dxdocument.text', 'Bot\xc3\xb3 standard gris']]

                templates['4. Taules'] = [['Taula', 'http://localhost:8080/170/etsab/templates/taula/genweb.get.dxdocument.text', 'Taula sense estils.'],
                                          ['Taula colors destacats', 'http://localhost:8080/170/etsab/templates/taula-colors-destacats/genweb.get.dxdocument.text', 'Taula amb colors destacats.'],
                                          ['Taula de registres per files', 'http://localhost:8080/170/etsab/templates/taula-de-registres-per-files/genweb.get.dxdocument.text', 'Per definir una taula de registres estructurada per columnes. Es pot ampliar en files i columnes.'],
                                          ['Taula amb estils', 'http://localhost:8080/170/etsab/templates/taula-amb-estils/genweb.get.dxdocument.text', 'Una taula amb vora, destacat ombrejat en passar per sobre amb el ratol\xc3\xad i diferenciaci\xc3\xb3 de columnes en diferents colors.'],
                                          ['Taula amb files destacades', 'http://localhost:8080/170/etsab/templates/taula-amb-files-destacades/genweb.get.dxdocument.text', 'Una taula amb vora, diferenciaci\xc3\xb3 de primera fila i columna.']]

                templates['5. Composicions'] = [['Columna de suport', 'http://localhost:8080/170/etsab/templates/columna-de-suport/genweb.get.dxdocument.text', 'Afegiu enlla\xc3\xa7os i contingut de suport a la columna de la dreta.'],
                                                ['Calendari', 'http://localhost:8080/170/etsab/templates/calendari/genweb.get.dxdocument.text', "Per representar gr\xc3\xa0ficament els esdeveniments o activitats d'un mes determinat. Es pot representar tot un any afegint successivament un mes darrera l'altre."],
                                                ['Fitxa', 'http://localhost:8080/170/etsab/templates/fitxa/genweb.get.dxdocument.text', 'Contenidor de fitxa.'],
                                                ['\xc3\x80lbum de fotografies', 'http://localhost:8080/170/etsab/templates/album-de-fotografies/genweb.get.dxdocument.text', 'Crea un \xc3\xa0lbum amb les miniatures de fotografies.'],
                                                ["Imatge alineada a l'esquerra amb text ", 'http://localhost:8080/170/etsab/templates/imatge-alineada-a-lesquerra-amb-text/genweb.get.dxdocument.text', "Imatge alineada a l'esquerra amb text."],
                                                ['Imatge alineada a la dreta amb text ', 'http://localhost:8080/170/etsab/templates/imatge-alineada-a-la-dreta-amb-text/genweb.get.dxdocument.text', 'Imatge alineada a la dreta amb text.'],
                                                ['Imatge amb text lateral superposat', 'http://localhost:8080/170/etsab/templates/imatge-amb-text-lateral-superposat/genweb.get.dxdocument.text', 'Imatge damunt la qual hi apareix un text superposat.'],
                                                ['Imatge amb text superposat clar', 'http://localhost:8080/170/etsab/templates/imatge-amb-text-superposat-clar/genweb.get.dxdocument.text', 'Imatge amb text superposat en un bloc inferior clar amb text fosc'],
                                                ['Imatge amb text superposat fosc', 'http://localhost:8080/170/etsab/templates/imatge-amb-text-superposat-fosc/genweb.get.dxdocument.text', 'Imatge amb text superposat en un bloc inferior fosc amb text blanc']]

                templates['6. Avançades'] = [["Carousel d'imatges", 'http://localhost:8080/170/etsab/templates/carousel-dimatges/genweb.get.dxdocument.text', "Carousel d'imatges navegables."],
                                             ['Zoom imatge', 'http://localhost:8080/170/etsab/templates/zoom-imatge/genweb.get.dxdocument.text', "Imatge que s'amplia."],
                                             ['Pestanyes', 'http://localhost:8080/170/etsab/templates/pestanyes/genweb.get.dxdocument.text', 'Contingut segmentat per pestanyes amb un altre estil.'],
                                             ['Pestanyes caixa', 'http://localhost:8080/170/etsab/templates/pestanyes-caixa/genweb.get.dxdocument.text', 'Contingut segmentat per pestanyes.'],
                                             ['Acordi\xc3\xb3', 'http://localhost:8080/170/etsab/templates/acordio/genweb.get.dxdocument.text', "Acordi\xc3\xb3 d'opcions."]]

                results = portal_catalog.searchResults(Language='',
                                                       path=paths[1],
                                                       object_provides=IDocument.__identifier__,
                                                       sort_on='getObjPositionInParent')

                templates['7. Pròpies'] = []
                for r in results:
                    templates['7. Pròpies'].append([r.Title, '%s/genweb.get.dxdocument.text' % r.getURL(), r.Description])

                qi = getToolByName(self.context, 'portal_quickinstaller')
                if qi.isProductInstalled('genweb.robtheme'):
                    templates['1. Destacats'] += [['Rob Theme - Caixa amb llista - UPC GRIS', 'http://localhost:8080/170/etsab/templates/rob-theme-caixa-amb-llista-upc-gris/genweb.get.dxdocument.text', ''],
                                                  ['Rob Theme - Caixa amb llista - VERD', 'http://localhost:8080/170/etsab/templates/rob-theme-caixa-amb-llista-verd/genweb.get.dxdocument.text', ''],
                                                  ['Rob Theme - Frase destacada', 'http://localhost:8080/170/etsab/templates/rob-theme-frase-destacada/genweb.get.dxdocument.text', ''],
                                                  ['Rob Theme - Destacat amb imatge', 'http://localhost:8080/170/etsab/templates/rob-theme-destacat-amb-imatge/genweb.get.dxdocument.text', '']]

                    templates['3. Continguts (Text, botons, bàners, Llistats)'] += [['Rob Theme - Banner Text Link - Icona Info - GRIS', 'http://localhost:8080/170/etsab/templates/rob-theme-banner-text-link-icona-info-gris/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Banner Text Link - Icona Arxiu - GRIS', 'http://localhost:8080/170/etsab/templates/rob-theme-banner-text-link-icona-arxiu-gris/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Banner Text Link - Icona Info - BLAU', 'http://localhost:8080/170/etsab/templates/rob-theme-banner-text-link-icona-info-blau/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Banner Text Link - Icona Arxiu - BLAU', 'http://localhost:8080/170/etsab/templates/rob-theme-banner-text-link-icona-arxiu-blau/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Banner Text No Link - Icona Info - GRIS', 'http://localhost:8080/170/etsab/templates/rob-theme-banner-text-no-link-icona-info-gris/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Banner Text No Link - Icona Arxiu - GRIS', 'http://localhost:8080/170/etsab/templates/rob-theme-banner-text-no-link-icona-arxiu-gris/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Banner Text No Link - Icona Info - BLAU', 'http://localhost:8080/170/etsab/templates/rob-theme-banner-text-no-link-icona-info-blau/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Banner Text No Link - Icona Arxiu - BLAU', 'http://localhost:8080/170/etsab/templates/rob-theme-banner-text-no-link-icona-arxiu-blau/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Banner Text Link - Imatge', 'http://localhost:8080/170/etsab/templates/rob-theme-banner-text-link-imatge/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Banner Text No Link - Imatge', 'http://localhost:8080/170/etsab/templates/rob-theme-banner-text-no-link-imatge/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Bot\xc3\xb3 Destacat BLAU', 'http://localhost:8080/170/etsab/templates/rob-theme-boto-destacat-blau/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Bot\xc3\xb3 Destacat GRIS', 'http://localhost:8080/170/etsab/templates/rob-theme-boto-destacat-gris/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Bot\xc3\xb3 Destacat DANGER', 'http://localhost:8080/170/etsab/templates/rob-theme-boto-destacat-danger/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Bot\xc3\xb3 Destacat WARNING', 'http://localhost:8080/170/etsab/templates/rob-theme-boto-destacat-warning/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Bot\xc3\xb3 Destacat SUCCESS', 'http://localhost:8080/170/etsab/templates/rob-theme-boto-destacat-success/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Llista amb subllista UPC', 'http://localhost:8080/170/etsab/templates/rob-theme-llista-amb-subllista-upc/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Listat opcions - icones lletres - 2 cols', 'http://localhost:8080/170/etsab/templates/rob-theme-llistat-opcions-icones-lletres-2-cols/genweb.get.dxdocument.text', ''],
                                                                                    ['Rob Theme - Conjunt Imatge amb llista opcions - 3 cols', 'http://localhost:8080/170/etsab/templates/rob-theme-conjunt-imatge-amb-llista-opcions-3-cols/genweb.get.dxdocument.text', '']]

                    templates['5. Composicions'] += [['Rob Theme - Dades num\xc3\xa8riques', 'http://localhost:8080/170/etsab/templates/rob-theme-dades-numeriques/genweb.get.dxdocument.text', ''],
                                                     ['Rob Theme - Graella imatges', 'http://localhost:8080/170/etsab/templates/rob-theme-graella-imatges/genweb.get.dxdocument.text', '']]

                    templates['6. Avançades'] += [['Rob Theme - Acordi\xc3\xb3', 'http://localhost:8080/170/etsab/templates/rob-theme-acordio/genweb.get.dxdocument.text', '']]

        return u'var tinyMCETemplateList = %s;' % templates


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


class gwToggleNewsInApp(grok.View):
    grok.context(IDexterityContent)
    grok.name('toggle_news_in_app')
    grok.require('cmf.ModifyPortalContent')
    grok.layer(IGenwebLayer)

    def render(self):
        context = aq_inner(self.context)
        is_inapp = IShowInApp(context).is_inapp
        if is_inapp:
            IShowInApp(context).is_inapp = False
            confirm = _(u'L\'element no es mostra a la App')
        else:
            IShowInApp(context).is_inapp = True
            confirm = _(u'L\'element es mostra a la App')

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
            self.request.response.redirect(self.context.absolute_url() + '/alltags')
        else:
            self.request.response.redirect(self.context.absolute_url())
