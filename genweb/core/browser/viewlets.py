from five import grok
from plone.app.layout.viewlets.interfaces import IAboveContentTitle
from Products.ATContentTypes.interface.document import IATDocument

# grok.templatedir("templates")


class notConfiguredViewlet(grok.Viewlet):
    grok.viewletmanager(IAboveContentTitle)
    grok.context(IATDocument)
