from StringIO import StringIO
from time import localtime
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter, getUtility
from Products.ATContentTypes.interface.folder import IATFolder
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from AccessControl import getSecurityManager

PLMF = MessageFactory('plonelocales')

def havePermissionAtRoot(self):
     """Funcio que retorna si es Editor a l'arrel"""
     
     pm= getToolByName(self, 'portal_membership')   
     tools = getMultiAdapter((self.context, self.request),
                                        name=u'plone_tools')       
     proot = tools.url().getPortalObject()
     #proot=pu.getPortalObject()
     sm = getSecurityManager()
     user = pm.getAuthenticatedMember()
     
     return sm.checkPermission('Modify portal content', proot) or ('WebMaster' in user.getRoles())    

def portal_url(self):
        """ Funcion a que retorna el path 
        """
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        return context_state.current_base_url()

class utilitats(BrowserView):

    def llistaEstats(self):
        """Retorna una llista dels estats dels workflows indicats
        """
        wtool = getToolByName(self,'portal_workflow')
        workflows = ['genweb_simple','genweb_review']
        estats = []
        for w in workflows:
            estats = estats + [s[0] for s in wtool.getWorkflowById(w).states.items()]
    
        return [w for w in wtool.listWFStatesByTitle() if w[0] in estats]

    def llistaContents(self):
        """Retorna tots els tipus de contingut, exclosos els de la llista types_to_exclude 
        """
        types_to_exclude = ['Banner', 'BannerContainer', 'CollageAlias', 'CollageColumn', 'CollageRow', 'Favorite', 'Large Plone Folder', 'Logos_Container', 'Logos_Footer', 'PoiPscTracker', 'SubSurvey', 'SurveyMatrix', 'SurveyMatrixQuestion', 'SurveySelectQuestion', 'SurveyTextQuestion',]
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        ptypes = portal_state.friendly_types()
        for typeEx in types_to_exclude:
            if typeEx in ptypes:
                ptypes.remove(typeEx)
        
        return ptypes
        
    def portal_url(self):
        """ Funcion a que retorna el path 
        """
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        return context_state.current_base_url()

    def dia_semana(self,day):
        """ Funcion a la que le pasas el dia y te lo devuelve en modo texto
        """
        _ts = getToolByName(self, 'translation_service')
        dia = day+1
        if dia == 7:
            dia = 0
        return PLMF(_ts. day_msgid(dia), default=_ts.weekday_english(dia, format='a'))
        
    def mes(self,month):
        """ Funcion a la que le pasas el mes y te lo devuelve en modo texto
        """
        _ts = getToolByName(self, 'translation_service')
        return PLMF(_ts.month_msgid(month), default=_ts.month_english(month, format='a'))
    
    def pref_lang(self):
        """Funcio que extreu idioma actiu
        """
        lt = getToolByName(self, 'portal_languages')
        return lt.getPreferredLanguage()

    def isFolder(self):
        """ Funcio que retorna si es carpeta per tal de mostrar o no el last modified
        """
        if  IATFolder.providedBy(self.context) or IPloneSiteRoot.providedBy(self.context):
            return True
   
    def getSectionFromURL(self):
        context=self.context
        #portal_url=getToolByName(context, 'portal_url')
        tools = getMultiAdapter((self.context, self.request),
                                        name=u'plone_tools')       
        
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        contentPath = tools.url().getRelativeContentPath(context)
        if not contentPath:
            return ''
        else:
            return portal_state.portal()[contentPath[0]].Title().replace('&nbsp;','')

    def getFlavour(self):
        portal_skins=getToolByName(self.context, 'portal_skins')
        return portal_skins.getDefaultSkin()

    
