from five import grok

from zope import schema
from zope.interface import Interface
from zope.annotation.interfaces import IAnnotations

from plone.indexer import indexer

from Products.Archetypes.interfaces import IBaseObject
from plone.dexterity.interfaces import IDexterityContent

from genweb.core import GenwebMessageFactory as _

SHOW_NEW_IN_APP_KEY = 'genweb.core.show_new_in_app'


class IShowInApp(Interface):
    """ An object which can be marked as inapp
    """

    in_app = schema.Bool(
        title=_(u"Tells if an object is shown in App"),
        default=False
    )


class inappMarker(grok.Adapter):
    """ Adapts all non folderish AT objects (IBaseContent) to have
        the inapp attribute (Boolean) as an annotation.
        It is available through Iinapp adapter.
    """
    grok.provides(IShowInApp)
    grok.context(Interface)

    def __init__(self, context):
        self.context = context

        annotations = IAnnotations(context)
        self._show_new_in_app = annotations.setdefault(SHOW_NEW_IN_APP_KEY, False)

    def get_inapp(self):
        annotations = IAnnotations(self.context)
        self._show_new_in_app = annotations.setdefault(SHOW_NEW_IN_APP_KEY, '')
        return self._show_new_in_app

    def set_inapp(self, value):
        annotations = IAnnotations(self.context)
        annotations[SHOW_NEW_IN_APP_KEY] = value
        self.context.reindexObject(idxs=["in_app"])

    in_app = property(get_inapp, set_inapp)


@indexer(IDexterityContent)
def showinappIndexer(context):
    """Create a catalogue indexer, registered as an adapter for DX content. """
    return IShowInApp(context).in_app


grok.global_adapter(showinappIndexer, name='in_app')


@indexer(IBaseObject)
def showinappIndexer(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``in_app`` index.
    """
    return IShowInApp(context).in_app


grok.global_adapter(showinappIndexer, name='in_app')
