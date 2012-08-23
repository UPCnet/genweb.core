from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from Products.CMFPlone.utils import _createObjectByType
from five import grok
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Acquisition import aq_inner

from upc.genwebupc.browser.plantilles import get_plantilles
from Products.CMFPlone.utils import normalizeString

from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from plone.cachepurging.interfaces import ICachePurgingSettings

from genweb.core.browser.helpers import getDorsal
from genweb.controlpanel.interface import IGenwebControlPanelSettings

import logging
import re


class migrateControlPanel(grok.View):
    """.."""
    grok.name('migrateControlPanel')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)

        logger = logging.getLogger('Genweb 4.2: Migration time!')
        logger.error('======================================================================')
        logger.error('%s' % context.id)
        logger.error('Running control panel and flavour settings migration from GW4 to GW4.2 ... ')

        genweb_props = getToolByName(context, 'portal_properties').genwebupc_properties
        registry = queryUtility(IRegistry)
        genweb_settings = registry.forInterface(IGenwebControlPanelSettings)

        # General section
        genweb_settings.html_title_ca = genweb_props.titolespai_ca
        genweb_settings.html_title_es = genweb_props.titolespai_es
        genweb_settings.html_title_en = genweb_props.titolespai_en

        genweb_settings.signatura_unitat_ca = genweb_props.firmaunitat_ca
        genweb_settings.signatura_unitat_es = genweb_props.firmaunitat_es
        genweb_settings.signatura_unitat_en = genweb_props.firmaunitat_en

        # Contact information section
        genweb_settings.contacte_id = unicode(genweb_props.contacteid)
        genweb_settings.contacte_no_upcmaps = genweb_props.boolmaps

        # Specific section
        genweb_settings.especific1 = unicode(genweb_props.especific1)
        genweb_settings.especific2 = unicode(genweb_props.especific3)

        if genweb_props.tipusintranet == 'Visible':
            genweb_settings.amaga_identificacio = False
        else:
            genweb_settings.amaga_identificacio = True

        # Master section
        genweb_settings.idestudi_master = unicode(genweb_props.idestudiMaster)

        # Translation flavour - GW4.2 settings
        legacy_skin = getToolByName(context, 'portal_skins').getDefaultSkin()

        # N3
        if legacy_skin == 'GenwebUPC_Neutre3':
            genweb_settings.contacte_BBBDD_or_page = False
            genweb_settings.contacte_al_peu = False
            genweb_settings.directori_upc = False
            genweb_settings.contrast_colors_bn = False
            genweb_settings.treu_imatge_capsalera = False
            genweb_settings.treu_menu_horitzontal = False
            genweb_settings.treu_icones_xarxes_socials = False

        # N2
        elif legacy_skin == 'GenwebUPC_Neutre2':
            genweb_settings.contacte_BBBDD_or_page = False
            genweb_settings.contacte_al_peu = False
            genweb_settings.directori_upc = False
            genweb_settings.contrast_colors_bn = False
            genweb_settings.treu_imatge_capsalera = False
            genweb_settings.treu_menu_horitzontal = True
            genweb_settings.treu_icones_xarxes_socials = False

        # Unitat
        elif legacy_skin == 'GenwebUPC_Unitat':
            genweb_settings.contacte_BBBDD_or_page = False
            genweb_settings.contacte_al_peu = False
            genweb_settings.directori_upc = False
            genweb_settings.contrast_colors_bn = False
            genweb_settings.treu_imatge_capsalera = False
            genweb_settings.treu_menu_horitzontal = False
            genweb_settings.treu_icones_xarxes_socials = False

        # Master
        elif legacy_skin == 'GenwebUPC_Master':
            genweb_settings.contacte_BBBDD_or_page = False
            genweb_settings.contacte_al_peu = False
            genweb_settings.directori_upc = False
            genweb_settings.contrast_colors_bn = False
            genweb_settings.treu_imatge_capsalera = False
            genweb_settings.treu_menu_horitzontal = True
            genweb_settings.treu_icones_xarxes_socials = False

        else:
            logger.error("OJO! skin del site no reconegut! %s" % legacy_skin)
            return "OJO! skin del site no reconegut!"

        return "Done!"


def migracio3(context):
    """Funcio que realitza la migracio de GW3 a GW4"""
    logger = logging.getLogger('Genweb 4: Migrator')
    logger.warn('======================================================================')
    logger.warn('%s' % context.id)
    logger.info('Running Migration')

    setup = getToolByName(context, 'portal_setup')
    ir = setup.getImportStepRegistry()
    ir.listSteps()
    logger.info('%s', ir.listSteps())

    try:
        ir.unregisterStep('upc.genweb.logosfooter.various')
        ir.unregisterStep('cachesettings')
        ir.unregisterStep('meetings-QI-dependencies')
        ir.unregisterStep('meetings-Update-RoleMappings')
        ir.unregisterStep('meetings-postInstall')
        ir.unregisterStep('meetings-GS-dependencies')
        ir.unregisterStep('upc.genweb.banners.various')
        ir.unregisterStep('upc.genweb.descriptorTIC-postInstall')
        logger.info("[Desregistrar steps de GS invalids] S'han desregistrat tots els steps correctament.")
    except:
        logger.info("[Desregistrar steps de GS invalids] Alguns dels steps no s'han trobat ja estaven esborrats o no existeixen")

    # Esborro el workflow que fa petar el migrador de Plone, despres ja es tornara a afegir
    pw = getToolByName(context, 'portal_workflow')
    try:
        pw.manage_delObjects('simpleTask_workflow')
        logger.info("[Esborrar workflow simpleTask] S'ha esborrat el simpleTask_workflow")
    except:
        logger.info('[Esborrar workflow simpleTask] El simpleTask_workflow ja estava esborrat')

    # Problema amb el SimpleAttachment, treure el 'Large Plone Folder' dels recursos 'linkables'
    kupuTool = getToolByName(context, 'kupu_library_tool', None)
    linkable = list(kupuTool.getPortalTypesForResourceType('linkable'))
    if 'Large Plone Folder' in linkable:
        linkable.remove('Large Plone Folder')
        kupuTool.updateResourceTypes(({'resource_type': 'linkable',
                                       'old_type': 'linkable',
                                       'portal_types': linkable},))

        logger.info("[Esborrar 'Large Plone Folder'] S'ha esborrat amb exit el tipus 'Large Plone Folder' dels recursos 'linkables' del Kupu")

    if 'Seccio' in linkable:
        linkable.remove('Seccio')
        kupuTool.updateResourceTypes(({'resource_type': 'linkable',
                                       'old_type': 'linkable',
                                       'portal_types': linkable},))

        logger.info("[Esborrar 'Seccio'] S'ha esborrat amb exit el tipus 'Seccio' dels recursos 'linkables' del Kupu")

    # Eliminem la transform del fck
    transformstool = getToolByName(context, 'portal_transforms', None)
    try:
        transformstool.manage_delObjects('fck_ruid_to_url')
        logger.info("Lesborrat de la transform de l'FCK ha estat satisfactoria")
    except:
        logger.info("Encara que s'ha intentat, l'esborrat de la transform de l'FCK ha fallat")

    # Canviem el rol per defecte dels usuaris autenticats via LDAP
    acl_users = getToolByName(context, 'acl_users')
    acl_users.ldapUPC.acl_users.manage_edit("ldapUPC", "cn", "cn", "ou=Users,dc=upc,dc=edu", 2, "Authenticated",
            "ou=Groups,dc=upc,dc=edu", 2, "cn=ldap.upc,ou=Users,dc=upc,dc=edu", "secret", 1, "cn",
            "top,person", 0, 0, "SSHA", 1, '')
    logger.info("S'ha canviat el rol dels usuaris autenticats via LDAP")

    return 'Purgat completat.'


def crearObjecte(context, id, type_name, title, description, exclude=True, constrains=None):
    pt = getToolByName(context, 'portal_types')
    if not getattr(context, id, False) and type_name in pt.listTypeTitles().keys():
        #creem l'objecte i el publiquem
        _createObjectByType(type_name, context, id)
    #populem l'objecte
    created = context[id]
    doWorkflowAction(created)
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


def doWorkflowAction(context):
    pw = getToolByName(context, "portal_workflow")
    object_workflow = pw.getWorkflowsFor(context)[0].id
    object_status = pw.getStatusOf(object_workflow, context)
    if object_status:
        try:
            pw.doActionFor(context, {'genweb_simple': 'publish', 'genweb_review': 'publicaalaintranet'}[object_workflow])
        except:
            pass


class migracioView(BrowserView):
    """Vista principal que s'ocupa de la migracio"""
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return migracio(self.context)


class afegirPlantillesTiny(grok.View):
    """Creacio dels objectes necessaris per a que funcioni el motor de templates de TinyMCE"""
    grok.name('afegirPlantillesTiny')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        pw = getToolByName(context, 'portal_workflow')
        templates = crearObjecte(context, 'templates', 'Folder', 'Templates', 'Plantilles per defecte administrades per l\'SCP.', constrains=(['Document']))
        plantilles = crearObjecte(context, 'plantilles', 'Folder', 'Plantilles', 'En aquesta carpeta podeu posar les plantilles per ser usades a l\'editor.', constrains = (['Document']))
        try:
            pw.doActionFor(templates, "restrict")
        except:
            pass

        for plt in get_plantilles():
            plantilla = crearObjecte(templates, normalizeString(plt['titol']), 'Document', plt['titol'], plt['resum'], '')
            plantilla.setText(plt['cos'], mimetype="text/html")

        return "OK"


class reaplicarDefaultWF(grok.View):
    """Reaplica el WF per defecte, donat un WF"""
    grok.name('reaplicarDefaultWF')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        wf = self.request.get('wf', None)
        if wf is not None:
            pw = getToolByName(context, 'portal_workflow')
            pw.setDefaultChain(wf)
            return wf
        else:
            return 'No workflow definit.'


class canviaFCKperTiny(grok.View):
    """Pues eso..."""
    grok.name('canviaFCKperTiny')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        logger = logging.getLogger('Genweb 4: Migrator')
        pm = getToolByName(context, 'portal_membership')
        pmd = getToolByName(context, 'portal_memberdata')
        for memberId in pmd._members:
            member = pm.getMemberById(memberId)
            if member is not None:
                editor = member.getProperty('wysiwyg_editor', None)
                if editor == 'TinyMCE':
                    logger.info('%s: TinyMCE already selected, leaving alone' % memberId)
                else:
                    member.setMemberProperties({'wysiwyg_editor': 'TinyMCE'})
                    logger.info('%s: TinyMCE has been set' % memberId)

        pmd.wysiwyg_editor = 'TinyMCE'
        return 'OK'


class canviaCachePurgeServer(grok.View):
    """.."""
    grok.name('canviaCachePurgeServer')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        registry = queryUtility(IRegistry)
        cachepurginsettings = registry.forInterface(ICachePurgingSettings)
        cacheserver = 'http://sylar.upc.es:90%02d' % int(getDorsal())
        cachepurginsettings.cachingProxies = (cacheserver,)


class canviaRestriccionsPlantilles(grok.View):
    """Canvia les restriccions de les plantilles per a que es puguin mostrar """
    grok.name('canviaRestriccionsPlantilles')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        templates = crearObjecte(context, 'templates', 'Folder', 'Templates', 'Plantilles per defecte administrades per l\'SCP.', constrains=(['Document'],['']))
        plantilles = crearObjecte(context, 'plantilles', 'Folder', 'Plantilles', 'En aquesta carpeta podeu posar les plantilles per ser usades a l\'editor.', constrains = (['Document'],['']))



class canviaPropietatsSurvey(grok.View):
    """ Canvia el portal_type dels objectes del PloneSurvey que tinguin espais en el nom del tipus"""

    grok.name('canviaPropietatsSurvey')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def update(self):
        # Busquem tots els objectes del PloneSurvey per canviar
        catalog = getToolByName(self.context, 'portal_catalog')
        search = catalog.searchResults({'portal_type': ['Sub Survey', 'Survey Date Question', 'Survey Matrix', 'Survey Matrix Question', 'Survey Select Question', 'Survey Text Question']})

        for item in search:
            objecte = item.getObject()
            # Eliminem tots els espais en blanc
            objecte.portal_type = re.sub(r'\s', '', objecte.Type())
            #Reindexem l'objecte
            objecte.reindexObject()

    def render(self):
        print "Objectes del PloneSurvey Actualitzats"
