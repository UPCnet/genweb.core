from zope.interface import implementer
from zope.component import provideUtility
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from souper.interfaces import ICatalogFactory
from souper.soup import NodeAttributeIndexer


@implementer(ICatalogFactory)
class UserPropertiesSoupCatalogFactory(object):
    def __call__(self, context):
        catalog = Catalog()
        idindexer = NodeAttributeIndexer('id')
        catalog['id'] = CatalogFieldIndex(idindexer)
        userindexer = NodeAttributeIndexer('username')
        catalog['username'] = CatalogTextIndex(userindexer)
        fullname = NodeAttributeIndexer('fullname')
        catalog['fullname'] = CatalogTextIndex(fullname)
        email = NodeAttributeIndexer('email')
        catalog['email'] = CatalogTextIndex(email)
        location = NodeAttributeIndexer('location')
        catalog['location'] = CatalogTextIndex(location)
        ubicacio = NodeAttributeIndexer('ubicacio')
        catalog['ubicacio'] = CatalogTextIndex(ubicacio)
        telefon = NodeAttributeIndexer('telefon')
        catalog['telefon'] = CatalogTextIndex(telefon)
        twitter_username = NodeAttributeIndexer('twitter_username')
        catalog['twitter_username'] = CatalogTextIndex(twitter_username)
        return catalog
provideUtility(UserPropertiesSoupCatalogFactory(), name="user_properties")


@implementer(ICatalogFactory)
class GroupsSoupCatalogFactory(object):
    def __call__(self, context):
        catalog = Catalog()
        groupindexer = NodeAttributeIndexer('id')
        catalog['id'] = CatalogFieldIndex(groupindexer)
        idsearchableindexer = NodeAttributeIndexer('searchable_id')
        catalog['searchable_id'] = CatalogTextIndex(idsearchableindexer)
        return catalog
provideUtility(GroupsSoupCatalogFactory(), name="ldap_groups")
