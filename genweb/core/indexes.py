from five import grok
from plone.indexer import indexer
from plone.app.contenttypes.interfaces import INewsItem

from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
from souper.interfaces import ICatalogFactory
from souper.soup import NodeAttributeIndexer
from zope.interface import implementer


@indexer(INewsItem)
def newsImageFile(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``context.filename`` value and index it.
    """
    return context.image.filename
grok.global_adapter(newsImageFile, name='news_image_filename')


@implementer(ICatalogFactory)
class UserSubscribedTagsSoupCatalog(object):
    def __call__(self, context):
        catalog = Catalog()
        idindexer = NodeAttributeIndexer('id')
        catalog['id'] = CatalogFieldIndex(idindexer)
        hashindex = NodeAttributeIndexer('tags')
        catalog['tags'] = CatalogKeywordIndex(hashindex)

        return catalog
grok.global_utility(UserSubscribedTagsSoupCatalog, name='user_subscribed_tags')
