from five import grok
from AccessControl import Unauthorized
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from genweb.core.interfaces import IProtectedContent
from genweb.core.utils import havePermissionAtRoot


@grok.subscribe(IProtectedContent, IObjectRemovedEvent)
def preventDeletionOnProtectedContent(content, event):
    """ Community added handler
    """
    # Only administrators can delete packet content from root folder
    user_has_permission_at_root = havePermissionAtRoot()

    if not user_has_permission_at_root:
        raise(Unauthorized, u"Cannot delete protected content.")
