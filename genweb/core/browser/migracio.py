from five import grok
from Acquisition import aq_inner
from zope.component import queryUtility

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import normalizeString

from plone.app.folder.utils import findObjects
from plone.locking.interfaces import ILockable
from plone.registry.interfaces import IRegistry
from plone.cachepurging.interfaces import ICachePurgingSettings

from Products.LinguaPlone.interfaces import ITranslatable

from genweb.core.browser.plantilles import get_plantilles
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
            return "OJO! skin del site no reconegut!" % legacy_skin

        return "Done!"


class migrateSeccioType(grok.View):
    """.."""
    grok.name('migrateSeccioType')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        self.logger = logging.getLogger('Genweb 4.2: Migration time!')
        pc = getToolByName(context, 'portal_catalog')
        pw = getToolByName(context, 'portal_workflow')
        default_wf = pw.getDefaultChain()
        ptypes = getToolByName(context, 'portal_types')
        ptypes['Plone Site'].allowed_content_types = ['Document', 'File', 'Folder', 'Image', 'Seccio']
        traverse = context.unrestrictedTraverse

        all_seccions = pc.searchResults(portal_type='Seccio', Language="all")

        if all_seccions is None:
            self.logger.error("El site %s no te seccions." % self.context.id)
            return "El site %s no te seccions." % self.context.id

        for seccio_brain in all_seccions:
            seccio = seccio_brain.getObject()
            seccio_id = seccio.id

            # Create the new folder, append '_new', set Language and state
            context.invokeFactory('Folder', seccio.id + '_new')
            new_folder = context[seccio_id + '_new']
            new_folder.setTitle(seccio.Title())
            new_folder.setDescription(seccio.Description())
            new_folder.setLanguage(seccio.getLanguage())
            new_folder.setExcludeFromNav(seccio.getExcludeFromNav())

            try:
                state = pw.getInfoFor(seccio, 'review_state')
                if state == 'published':
                    pw.doActionFor(new_folder, 'publish')
                elif state == 'private':
                    pw.doActionFor(new_folder, 'hide')
                elif state == 'intranet':
                    pw.doActionFor(new_folder, 'publishtointranet')
            except:
                pass

            # Look for some possible locked objects inside section
            self.stealLocks(seccio)

            # Move all objects to the new location
            ids_to_move = [childrenId for childrenId in seccio.objectIds()]

            # Statistics
            path = '/'.join(seccio.getPhysicalPath())
            seccio_objs = pc.searchResults(object_provides=ITranslatable.__identifier__, path={'query': path}, Language="all")
            self.logger.error("Migrant %s objectes a la nova carpeta dins de %s." % (len(seccio_objs), ids_to_move))

            for childrenId in ids_to_move:
                cp = seccio.manage_cutObjects(childrenId)
                new_folder.manage_pasteObjects(cp)

            # Rename objects
            context.manage_renameObjects([seccio.id], [seccio.id + '_old'])
            import transaction
            transaction.commit()
            context.manage_renameObjects([new_folder.id], [seccio_id])

        # Clone the link to translations of the new objects by id
        all_seccions = pc.searchResults(portal_type='Seccio', Language="all")
        base = '/'.join(context.getPhysicalPath())
        for seccio_brain in all_seccions:
            seccio = seccio_brain.getObject()
            if seccio.isCanonical:
                translations = seccio.getTranslations(include_canonical=False)
                if translations:
                    for language in translations.keys():
                        try:
                            traverse(translations[language][0].id.replace('_old', '')).addTranslationReference(traverse(base + '/' + seccio.id.replace('_old', '')))
                        except:
                            pass

        return 'Done!'

    def stealLocks(self, seccio):
        for path, obj in findObjects(seccio):
            lockable = ILockable(obj)
            if lockable.locked():
                lockable.unlock()
                self.logger.error("Unlocking object %s." % obj)


class killBrokenTransforms(grok.View):
    """.."""
    grok.name('killBrokenTransforms')
    grok.context(IPloneSiteRoot)
    grok.require('zope2.ViewManagementScreens')

    def render(self):
        context = aq_inner(self.context)
        pt = getToolByName(context, 'portal_transforms')

        return 'Done!'


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
            "ou=Groups,dc=upc,dc=edu", 2, "cn=ldap.upc,ou=Users,dc=upc,dc=edu", "conldapnexio", 1, "cn",
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
