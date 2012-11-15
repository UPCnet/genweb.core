from five import grok

from zope import schema
from zope.interface import Interface
from zope.annotation.interfaces import IAnnotations

from Products.Archetypes.interfaces import IBaseContent

from genweb.core import GenwebMessageFactory as _

IMPORTANT_KEY = 'genweb.core.important'


class IImportant(Interface):
    """ An object which can be marked as important
    """

    is_important = schema.Bool(
            title=_(u"Tells if an object is marked as important"),
            default=False
        )


class ImportantMarker(grok.Adapter):
    grok.provides(IImportant)
    grok.context(IBaseContent)

    def __init__(self, context):
        self.context = context

        annotations = IAnnotations(context)
        self.is_important = annotations.setdefault(IMPORTANT_KEY, False)
