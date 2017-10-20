from five import grok

from zope import schema
from zope.interface import Interface
from zope.annotation.interfaces import IAnnotations

from plone.indexer import indexer

from Products.Archetypes.interfaces import IBaseObject
from plone.dexterity.interfaces import IDexterityContent

from genweb.core import GenwebMessageFactory as _

FLASH_KEY = 'genweb.core.flash'


class IFlash(Interface):
    """ An object which can be marked as flash
    """

    is_flash = schema.Bool(
        title=_(u"Tells if an object is marked as flash"),
        default=False
    )


class FlashMarker(grok.Adapter):
    """ Adapts all non folderish AT objects (IBaseContent) to have
        the flash attribute (Boolean) as an annotation.
        It is available through IFlash adapter.
    """
    grok.provides(IFlash)
    grok.context(Interface)

    def __init__(self, context):
        self.context = context

        annotations = IAnnotations(context)
        self._is_flash = annotations.setdefault(FLASH_KEY, False)

    def get_flash(self):
        annotations = IAnnotations(self.context)
        self._is_flash = annotations.setdefault(FLASH_KEY, '')
        return self._is_flash

    def set_flash(self, value):
        annotations = IAnnotations(self.context)
        annotations[FLASH_KEY] = value
        self.context.reindexObject(idxs=["is_flash"])

    is_flash = property(get_flash, set_flash)


@indexer(IDexterityContent)
def flashIndexer(context):
    """Create a catalogue indexer, registered as an adapter for DX content. """
    return IFlash(context).is_flash


grok.global_adapter(flashIndexer, name='is_flash')


@indexer(IBaseObject)
def flashIndexerAT(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``is_flash`` index.
    """
    return IFlash(context).is_flash


grok.global_adapter(flashIndexerAT, name='is_flash')
