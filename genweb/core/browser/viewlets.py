from five import grok
from Acquisition import aq_inner

from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.layout.viewlets.interfaces import IAboveContent

from genweb.core.interfaces import IGenwebLayer
from genweb.core.interfaces import IHomePage
from genweb.core.utils import portal_url


class notConfiguredForHomes(grok.Viewlet):
    grok.viewletmanager(IAboveContent)
    grok.context(IHomePage)
    grok.layer(IGenwebLayer)

    def existObjectsNeeded(self):
        """Funcio que mira si existeixen els objectes que son necessaris pel bon funcionament del espai
           TODO: Fer que comprovi mes objectes, per ara nomes comprova la pagina principal en catala
        """
        context = aq_inner(self.context)
        return getattr(context, 'benvingut', False)

    def getSetupLink(self):
        """Funcio que dona l'enllas al formulari de creacio dels elements per defecte
        """
        return portal_url(self) + "/setup-view"


class notConfiguredForRoots(grok.Viewlet):
    grok.viewletmanager(IAboveContent)
    grok.context(IPloneSiteRoot)
    grok.layer(IGenwebLayer)

    def existObjectsNeeded(self):
        """Funcio que mira si existeixen els objectes que son necessaris pel bon funcionament del espai
           TODO: Fer que comprovi mes objectes, per ara nomes comprova la pagina principal en catala
        """
        context = aq_inner(self.context)
        return getattr(context, 'benvingut', False)

    def getSetupLink(self):
        """Funcio que dona l'enllas al formulari de creacio dels elements per defecte
        """
        return portal_url(self) + "/setup-view"
