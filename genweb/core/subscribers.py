from five import grok
from plone import api
from AccessControl import Unauthorized
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from genweb.core.interfaces import IProtectedContent


@grok.subscribe(IProtectedContent, IObjectRemovedEvent)
def preventDeletionOnProtectedContent(content, event):
    """ Community added handler
    """
    try:
        api.portal.get()
    except:
        # Most probably we are on Zope root and trying to delete an entire Plone
        # Site so grant it unconditionally
        return

    # Only (global) site managers can delete packet content from root folder

    if 'Manager' not in api.user.get_roles():
        raise(Unauthorized, u'Cannot delete protected content.')
    else:
        return
