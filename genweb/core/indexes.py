from five import grok
from plone.indexer import indexer
from plone.app.contenttypes.interfaces import INewsItem


@indexer(INewsItem)
def newsImageFile(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``context.filename`` value and index it.
    """
    return context.image.filename
grok.global_adapter(newsImageFile, name='news_image_filename')
