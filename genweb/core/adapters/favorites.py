from five import grok
from zope.interface import Interface

from plone.indexer import indexer
from plone.dexterity.interfaces import IDexterityContent

from Products.Archetypes.interfaces import IBaseContent

ATTRIBUTE_NAME = '_favoritedBy'


class IFavorite(Interface):
    """ Adapt an object to this interface to manage the favorites of an object """

    def get():
        """ Return the usernames who favorited the object. """

    def add(username):
        """ Set the username that favorites the object. """


class Favorite(grok.Adapter):
    grok.provides(IFavorite)
    grok.context(Interface)

    def __init__(self, context):
        self.context = context

    def get(self):
        return getattr(self.context, ATTRIBUTE_NAME, None)

    def add(self, username):
        username = str(username)
        fans = self.get()
        if fans:
            fans.append(username)
        else:
            fans = []
            fans.append(username)
        setattr(self.context, ATTRIBUTE_NAME, fans)
        self.context.reindexObject()


@indexer(IDexterityContent)
def favoriteIndexer(context):
    """Create a catalogue indexer, registered as an adapter for AT content. """
    return IFavorite(context).get()
grok.global_adapter(favoriteIndexer, name='favoritedBy')
