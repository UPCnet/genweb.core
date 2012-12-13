from five import grok

from zope import schema
from zope.interface import Interface
from zope.annotation.interfaces import IAnnotations

from plone.indexer import indexer

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
    """ Adapts all non folderish AT objects (IBaseContent) to have
        the important attribute (Boolean) as an annotation.
        It is available through IImportant adapter.
    """
    grok.provides(IImportant)
    grok.context(IBaseContent)

    def __init__(self, context):
        self.context = context

        annotations = IAnnotations(context)
        self._is_important = annotations.setdefault(IMPORTANT_KEY, False)

    def get_important(self):
        return self._is_important

    def set_important(self, value):
        self._is_important = value
        self.context.reindexObject()

    is_important = property(get_important, set_important)


@grok.adapter(IBaseContent, name='is_important')
@indexer(IBaseContent)
def importantIndexer(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``is_important`` index.
    """
    return IImportant(context).is_important
