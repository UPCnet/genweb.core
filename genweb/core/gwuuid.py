from five import grok
from zope.interface import Interface
from zope.component import queryUtility
from zope import interface
from zope import component

from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectCopiedEvent

from plone.indexer import indexer
from plone.uuid.interfaces import IUUIDGenerator
from plone.uuid.interfaces import IAttributeUUID
from plone.uuid.interfaces import IUUIDAware

try:
    from Acquisition import aq_base
except ImportError:
    aq_base = lambda v: v  # soft-dependency on Zope2, fallback

ATTRIBUTE_NAME = '_gw.uuid'


class IGWUUID(Interface):
    """ The interface of the adapter for getting and setting the gwuuid """

    def get():
        """Return the UUID of the context"""

    def set(uuid):
        """Set the unique id of the context with the uuid value.
        """


@grok.subscribe(IAttributeUUID, IObjectCreatedEvent)
def addAttributeUUID(obj, event):

    if not IObjectCopiedEvent.providedBy(event):
        if getattr(aq_base(obj), ATTRIBUTE_NAME, None):
            return  # defensive: keep existing UUID on non-copy create

    generator = queryUtility(IUUIDGenerator)
    if generator is None:
        return

    uuid = generator()
    if not uuid:
        return

    setattr(obj, ATTRIBUTE_NAME, uuid)


@grok.implementer(IGWUUID)
@grok.adapter(IAttributeUUID)
class MutableAttributeUUID(object):

    def __init__(self, context):
        self.context = context

    def get(self):
        return getattr(self.context, ATTRIBUTE_NAME, None)

    def set(self, uuid):
        uuid = str(uuid)
        setattr(self.context, ATTRIBUTE_NAME, uuid)


@indexer(IUUIDAware)
def gwUUID(context):
    return IGWUUID(context, None).get()
grok.global_adapter(gwUUID, name='gwuuid')


class GWUUIDView(grok.View):
    grok.context(Interface)

    def render(self):
        return IGWUUID(self.context).get()
