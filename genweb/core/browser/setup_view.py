# -*- coding: utf-8 -*-
from five import grok
from cgi import parse_qs
from Acquisition import aq_parent
from zope.interface import alsoProvides
from zope.component import getMultiAdapter

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import _createObjectByType

from plone.app.controlpanel.mail import IMailSchema

from genweb.core.interfaces import IHomePage
from genweb.core.browser.plantilles import get_plantilles

grok.templatedir('views_templates')


class setup(grok.View):
    grok.name('setup-view')
    grok.template('setup_view')
    grok.context(IPloneSiteRoot)
    grok.require('cmf.ManagePortal')

    # index = ViewPageTemplateFile('setup_view.pt')

    def update(self):
        base_url = "%s/@@setup-view" % str(
                       getMultiAdapter((self.context, self.request),
                       name='absolute_url')
                   )
        qs = self.request.get('QUERY_STRING', None)
        if qs is not None:
            query = parse_qs(qs)
            if 'create' in query:
                for name in query['create']:
                    if name == 'all':
                        self.createContent()
                        self.request.response.redirect(base_url)

    def contentStatus(self):
        objects = [('Notícies', ['noticies', 'noticias', 'news']),
                   ('Esdeveniments', ['esdeveniments', 'eventos', 'events']),
                   ('Banners', ['banners-ca', 'banners-es', 'banners-en']),
                   ('LogosFooter', ['logosfooter-ca', 'logosfooter-es', 'logosfooter-en']),
                   ('Homepage', ['benvingut', 'bienvenido', 'welcome']),
                   ('Templates', ['templates', ]),
                   ('Plantilles', ['plantilles', ]),
                   ]
        result = []
        portal = getToolByName(self, 'portal_url').getPortalObject()
        for o in objects:
            tr = [o[0]]
            for td in o[1]:
                tr.append(getattr(portal, td, False) and 'Creat' or 'No existeix')
            result.append(tr)
        return result

    def createContent(self):
        """ Method that creates all the default content """

        # Let's configure mail
        portal = getToolByName(self, 'portal_url').getPortalObject()
        mail = IMailSchema(portal)
        mail.smtp_host = u'localhost'
        mail.email_from_name = "Administrador del Genweb"
        mail.email_from_address = "noreply@upc.edu"

        if getattr(portal, 'front-page', False):
            portal.manage_delObjects('front-page')
        if getattr(portal, 'news', False):
            if not self.getObjectStatus(portal.news):
                portal.manage_delObjects('news')
        if getattr(portal, 'events', False):
            if not self.getObjectStatus(portal.events):
                portal.manage_delObjects('events')
        if getattr(portal, 'Members', False):
            portal['Members'].setExcludeFromNav(True)
            portal['Members'].reindexObject()
            portal['Members'].setLanguage('en')

        # Let's create folders and collections, linked by language, the first language is the canonical one

        news = self.crearObjecte(portal, 'news', 'Folder', 'News', 'Site News', constrains=(['News Item'], ['Image']))
        noticias = self.crearObjecte(portal, 'noticias', 'Folder', 'Notícias', 'Notícias del sitio', constrains=(['News Item'], ['Image']))
        noticies = self.crearObjecte(portal, 'noticies', 'Folder', 'Notícies', 'Notícies del lloc', constrains=(['News Item'], ['Image']))
        self.setLanguageAndLink([(noticies, 'ca'), (noticias, 'es'), (news, 'en')])

        self.addCollection(news, 'aggregator', 'News', 'Site News', 'News Item')
        self.addCollection(noticias, 'aggregator', 'Notícias', 'Notícias del sitio', 'News Item')
        self.addCollection(noticies, 'aggregator', 'Notícies', 'Notícies del lloc', 'News Item')
        self.setLanguageAndLink([(noticies.aggregator, 'ca'), (noticias.aggregator, 'es'), (news.aggregator, 'en')])

        noticies.aggregator.manage_permission(permissions.DeleteObjects, roles=["Manager"], acquire=False)
        noticias.aggregator.manage_permission(permissions.DeleteObjects, roles=["Manager"], acquire=False)
        news.aggregator.manage_permission(permissions.DeleteObjects, roles=["Manager"], acquire=False)

        events = self.crearObjecte(portal, 'events', 'Folder', 'Events', 'Site Events', constrains=(['Event', 'Meeting'], ['Image']))
        eventos = self.crearObjecte(portal, 'eventos', 'Folder', 'Eventos', 'Eventos del sitio', constrains=(['Event', 'Meeting'], ['Image']))
        esdeveniments = self.crearObjecte(portal, 'esdeveniments', 'Folder', 'Esdeveniments', 'Esdeveniments del lloc', constrains=(['Event', 'Meeting'], ['Image']))
        self.setLanguageAndLink([(esdeveniments, 'ca'), (eventos, 'es'), (events, 'en')])

        self.addCollection(events, 'aggregator', 'Events', 'Site Events', ('Event', 'Meeting'), date_filter=True)
        self.addCollection(eventos, 'aggregator', 'Eventos', 'Eventos del sitio', ('Event', 'Meeting'), date_filter=True)
        self.addCollection(esdeveniments, 'aggregator', 'Esdeveniments', 'Esdeveniments del lloc', ('Event', 'Meeting'), date_filter=True)
        self.setLanguageAndLink([(esdeveniments.aggregator, 'ca'), (eventos.aggregator, 'es'), (events.aggregator, 'en')])

        esdeveniments.aggregator.manage_permission(permissions.DeleteObjects, roles=["Manager"], acquire=False)
        eventos.aggregator.manage_permission(permissions.DeleteObjects, roles=["Manager"], acquire=False)
        events.aggregator.manage_permission(permissions.DeleteObjects, roles=["Manager"], acquire=False)

        self.addCollection(events.aggregator, 'previous', 'Past Events', 'Events which have already happened. ', 'Event', dateRange=u'-', operation=u'less', setDefault=False, path='grandfather', date_filter=True)
        self.addCollection(eventos.aggregator, 'anteriores', 'Eventos pasados', 'Eventos del sitio que ya han sucedido', 'Event', dateRange=u'-', operation=u'less', setDefault=False, path='grandfather', date_filter=True)
        self.addCollection(esdeveniments.aggregator, 'anteriors', 'Esdeveniments passats', 'Esdeveniments del lloc que ja han passat', 'Event', dateRange=u'-', operation=u'less', setDefault=False, path='grandfather', date_filter=True)
        self.setLanguageAndLink([(esdeveniments.aggregator.anteriors, 'ca'), (eventos.aggregator.anteriores, 'es'), (events.aggregator.previous, 'en')])

        banners_en = self.crearObjecte(portal, 'banners-en', 'BannerContainer', 'Banners', 'English Banners')
        banners_es = self.crearObjecte(portal, 'banners-es', 'BannerContainer', 'Banners', 'Banners en Español')
        banners_ca = self.crearObjecte(portal, 'banners-ca', 'BannerContainer', 'Banners', 'Banners en Català')
        self.setLanguageAndLink([(banners_ca, 'ca'), (banners_es, 'es'), (banners_en, 'en')])

        logosfooter_en = self.crearObjecte(portal, 'logosfooter-en', 'Logos_Container', 'Footer Logos', 'English footer logos')
        logosfooter_es = self.crearObjecte(portal, 'logosfooter-es', 'Logos_Container', 'Logos pie', 'Logos en español del pie de página')
        logosfooter_ca = self.crearObjecte(portal, 'logosfooter-ca', 'Logos_Container', 'Logos peu', 'Logos en català del peu de pàgina')
        self.setLanguageAndLink([(logosfooter_ca, 'ca'), (logosfooter_es, 'es'), (logosfooter_en, 'en')])

        # welcome pages

        welcome_string = """<h1>Us donem la benvinguda a Genweb UPC v3</h1>
<div id="content-core">
<p> </p>
<p><a href="http://www.upc.edu/comunicacio/www/genweb-upc"><img alt="Genweb UPC" class="image-right" src="logogw.gif" /></a></p>
<p>A partir d'aquest moment, ja podeu introduir continguts al vostre espai <a href="http://www.upc.edu/comunicacio/www/genweb-upc" target="_blank">Genweb</a>. A més, us oferim l'allotjament del vostre espai, <a href="http://www.upc.edu/comunicacio/www/dominis-upc" target="_blank">un domini upc.edu</a>, estadístiques, formació i suport tècnic.</p>
<h2>Abans d'utilitzar Genweb...</h2>
<p>Consulteu el <a href="http://www.upc.edu/comunicacio/www/genweb-upc/formacio/genweb3_manualUsuari.pdf" target="_blank">manual d'usuari</a> i els <a href="http://www.upc.edu/comunicacio/www/genweb-upc/formacio" target="_blank">videotutorials de formació</a>.<br /> Sempre tindreu accés a la formació i al suport tècnic a través de l'enllaç d'<a href="http://www.upc.edu/comunicacio/www/genweb-upc/formacio" target="_blank">ajuda</a> que apareix a les opcions d'usuari.</p>
<h2>Les novetats...</h2>
<p>El Genweb està a la última, més potent i adaptat<br /><br /></p>
<ul>
<li>Una <strong>imatge actualitzada </strong>al nou programari</li>
<li><strong>TinyMCE</strong> és el nou editor del Genweb</li>
<li>Edició més flexible:<strong> crea les teves pròpies </strong><strong>plantilles</strong></li>
<li><strong>Genweb UPC v3 </strong>està desenvolupat amb el gestor de continguts de programari lliure <a href="http://www.plone.org" target="_blank">Plone 4.0</a>, basat en el servidor d'aplicacions Zope.</li>
</ul>
<h2>Participació...</h2>
<p>Si teniu idees, necessitats o suggeriments per millorar el Genweb, ens ho podeu explicar a la nostra <a href="mailto:servei.comunicacio.promocio@upc.edu">bústia</a>.</p>
<p> </p>
<p> </p>
</div>"""
        benvingut = self.crearObjecte(portal, 'benvingut', 'Document', 'Benvingut', '')
        bienvenido = self.crearObjecte(portal, 'bienvenido', 'Document', 'Bienvenido', '')
        welcome = self.crearObjecte(portal, 'welcome', 'Document', 'Welcome', '')

        benvingut.setText(welcome_string, mimetype='text/html')
        bienvenido.setText(welcome_string, mimetype='text/html')
        welcome.setText(welcome_string, mimetype='text/html')

        benvingut.manage_permission(permissions.DeleteObjects, roles=["Manager"], acquire=False)
        bienvenido.manage_permission(permissions.DeleteObjects, roles=["Manager"], acquire=False)
        welcome.manage_permission(permissions.DeleteObjects, roles=["Manager"], acquire=False)

        self.setLanguageAndLink([(benvingut, 'ca'), (bienvenido, 'es'), (welcome, 'en')])

        # Mark all homes with IHomePage marker interface
        alsoProvides(benvingut, IHomePage)
        alsoProvides(bienvenido, IHomePage)
        alsoProvides(welcome, IHomePage)

        # Reindex them to update object_provides index
        benvingut.reindexObject()
        bienvenido.reindexObject()
        welcome.reindexObject()

        # Set the default page to the homepage view
        portal.setDefaultPage('homepage')

        # Templates TinyMCE
        templates = self.crearObjecte(portal, 'templates', 'Folder', 'Templates', 'Plantilles per defecte administrades per l\'SCP.', constrains=(['Document'], ['']))
        plantilles = self.crearObjecte(portal, 'plantilles', 'Folder', 'Plantilles', 'En aquesta carpeta podeu posar les plantilles per ser usades a l\'editor.', constrains=(['Document'], ['']))
        pw = getToolByName(portal, "portal_workflow")
        pw.doActionFor(templates, "restrict")

        for plt in get_plantilles():
            plantilla = self.crearObjecte(templates, normalizeString(plt['titol']), 'Document', plt['titol'], plt['resum'], '')
            plantilla.setText(plt['cos'], mimetype="text/html")

        return True

    def setLanguageAndLink(self, items):
        canonical, canonical_lang = items[0]
        for item, language in items:
            item.setLanguage(language)
            if item != canonical and canonical_lang not in item.getTranslations().keys():
                item.addTranslationReference(canonical)

    def getObjectStatus(self, context):
        pw = getToolByName(context, "portal_workflow")
        object_workflow = pw.getWorkflowsFor(context)[0].id
        object_status = pw.getStatusOf(object_workflow, context)
        return object_status

    def doWorkflowAction(self, context):
        pw = getToolByName(context, "portal_workflow")
        object_workflow = pw.getWorkflowsFor(context)[0].id
        object_status = pw.getStatusOf(object_workflow, context)
        if object_status:
            try:
                pw.doActionFor(context, {'genweb_simple': 'publish', 'genweb_review': 'publicaalaintranet'}[object_workflow])
            except:
                pass

    def crearObjecte(self, context, id, type_name, title, description, exclude=True, constrains=None):
        pt = getToolByName(context, 'portal_types')
        if not getattr(context, id, False) and type_name in pt.listTypeTitles().keys():
            #creem l'objecte i el publiquem
            _createObjectByType(type_name, context, id)
        #populem l'objecte
        created = context[id]
        self.doWorkflowAction(created)
        created.setTitle(title)
        created.setDescription(description)
        created._at_creation_flag = False
        created.setExcludeFromNav(exclude)
        if constrains:
            created.setConstrainTypesMode(1)
            if len(constrains) > 1:
                created.setLocallyAllowedTypes(tuple(constrains[0] + constrains[1]))
            else:
                created.setLocallyAllowedTypes(tuple(constrains[0]))
            created.setImmediatelyAddableTypes(tuple(constrains[0]))

        created.reindexObject()
        return created

    def addCollection(self, context, id, title, description, type_filter, state_filter=None, day=0, dateRange=u'+', operation=u'more', setDefault=True, path='father', date_filter=False):

        topic = self.crearObjecte(context, id, 'Topic', title, description, False)

        # Activem el limit i el posem a 10 notícies
        topic.setLimitNumber(True)
        topic.setItemCount(10)

        #Ara afegim els criteris, si no hi son
        criteris = [('Type', 'ATPortalTypeCriterion'),
            ('path', 'ATPathCriterion'),
            ('modified', 'ATSortCriterion')]
        if date_filter:
            criteris.append(('start', 'ATFriendlyDateCriteria'))
        if state_filter:
            criteris.append(('review_state', 'ATSimpleStringCriterion'))

        for crit in criteris:
            if not 'crit__%s_%s' % (crit[0], crit[1]) in topic.keys():
                topic.addCriterion(crit[0], crit[1])

        # Criteri tipus
        criteri_tipus = topic['crit__Type_ATPortalTypeCriterion']
        criteri_tipus.setValue((type_filter))

        #TOREVIEW
        #criteri_tipus.setOperator('and')

        # criteri estat
        if state_filter:
            criteri_estat = topic['crit__review_state_ATSimpleStringCriterion']
            criteri_estat.setValue((state_filter))

        # criteri ruta = carpeta pare

        criteri_ruta = topic['crit__path_ATPathCriterion']
        ruta = path == 'father' and context or aq_parent(context)
        criteri_ruta.setValue([ruta])
        criteri_ruta.setRecurse(True)

        # criteri data

        if date_filter:
            criteri_estat = topic['crit__start_ATFriendlyDateCriteria']
            criteri_estat.setValue(day)
            criteri_estat.setDateRange(dateRange)
            criteri_estat.setOperation(operation)

        # Criteri d'ordenació

        criteri_ordenacio = topic['crit__modified_ATSortCriterion']
        criteri_ordenacio.setReversed(True)

        # Posar la vista per defecte de la pàgina principal a la collection que acavem de crear

        if setDefault:
            context.setDefaultPage(id)
        return
