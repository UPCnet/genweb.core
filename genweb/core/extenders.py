from zope.component import adapts
from zope.interface import implements

from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import BooleanWidget

from Products.ATContentTypes.interface.link import IATLink

from Products.ATContentTypes.interface.news import IATNewsItem

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender

from five import grok
from plone.indexer import indexer


# TODO: Deprecate all this
# Any field you tack on must have ExtensionField as its first subclass:
class _StringExtensionField(ExtensionField, BooleanField):
    pass


class ATLinkSchemaModifier(object):
    """Afegeix un check nou al contingut enllas"""
    adapts(IATLink)
    implements(IOrderableSchemaExtender)

    _fields = [
        _StringExtensionField('obrirfinestra',
            required=False,
            searchable=True,
            widget=BooleanWidget(
                label='Open in a new window',
                label_msgid='upc.genweb.banners_label_Obrirennovafinestra',
                i18n_domain='upc.genweb.banners',
            )
        )
    ]

    def __init__(self, newsItem):
        pass

    def getFields(self):
        return self._fields

    def getOrder(self, original):
        new = original.copy()  # contract requires us to make a new one
        defaultSchemaFields = new['default']  # fields from the "default" schemata
        defaultSchemaFields.remove('obrirfinestra')
        defaultSchemaFields.insert(defaultSchemaFields.index('remoteUrl') + 1,
                                   'obrirfinestra')  # stick "obrirfinestra" after "remoteUrl"
        return new


@indexer(IATLink)
def obrirEnFinestraNova(obj):
    return obj.obrirfinestra
grok.global_adapter(obrirEnFinestraNova, name="obrirEnFinestraNova")


@indexer(IATNewsItem)
def newsImageFile(obj):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``context.filename`` value and index it.
    """
    return obj.getField('image').getFilename(obj)
grok.global_adapter(newsImageFile, name='news_image_filename')
