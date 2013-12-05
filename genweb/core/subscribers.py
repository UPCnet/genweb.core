from five import grok
from AccessControl import Unauthorized
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from genweb.core.interfaces import IProtectedContent


@grok.subscribe(IProtectedContent, IObjectRemovedEvent)
def preventDeletionOnProtectedContent(content, event):
    """ Community added handler
    """
    raise(Unauthorized, u"Cannot delete protected content.")
