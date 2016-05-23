from five import grok

from zope import schema
from zope.interface import Interface
from zope.annotation.interfaces import IAnnotations

from plone.indexer import indexer

from Products.Archetypes.interfaces import IBaseObject
from plone.dexterity.interfaces import IDexterityContent

from genweb.core import GenwebMessageFactory as _

OUTOFLIST_KEY = 'genweb.core.outoflist'


class IOutOfList(Interface):
    """ An object which can be marked as outoflist
    """

    is_outoflist = schema.Bool(
        title=_(u"Tells if an object is marked as outoflist"),
        default=False
    )


class OutOfListMarker(grok.Adapter):
    """ Adapts all non folderish AT objects (IBaseContent) to have
        the outoflist attribute (Boolean) as an annotation.
        It is available through IOutOfList adapter.
    """
    grok.provides(IOutOfList)
    grok.context(Interface)

    def __init__(self, context):
        self.context = context

        annotations = IAnnotations(context)
        self._is_outoflist = annotations.setdefault(OUTOFLIST_KEY, False)

    def get_outoflist(self):
        annotations = IAnnotations(self.context)
        self._is_outoflist = annotations.setdefault(OUTOFLIST_KEY, '')
        return self._is_outoflist

    def set_outoflist(self, value):
        annotations = IAnnotations(self.context)
        annotations[OUTOFLIST_KEY] = value
        self.context.reindexObject(idxs=["is_outoflist"])

    is_outoflist = property(get_outoflist, set_outoflist)


@indexer(IDexterityContent)
def outoflistIndexer(context):
    """Create a catalogue indexer, registered as an adapter for DX content. """
    return IOutOfList(context).is_outoflist
grok.global_adapter(outoflistIndexer, name='is_outoflist')


@indexer(IBaseObject)
def outoflistIndexerAT(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``is_outoflist`` index.
    """
    return IOutOfList(context).is_outoflist
grok.global_adapter(outoflistIndexerAT, name='is_outoflist')
