from five import grok
from zope.interface import Interface
from plone import api
from elasticsearch import Elasticsearch
from zope.component import getUtility


class IElasticSearch(Interface):
    """ Marker for ElasticSearch global utility """


class ElasticSearch(object):
    grok.implements(IElasticSearch)

    def __init__(self):
        self._conn = None

    def __call__(self):
        return self.connection

    def create_new_connection(self):
        self.es_url = api.portal.get_registry_record('genweb.controlpanel.core.IGenwebCoreControlPanelSettings.elasticsearch')
        self._conn = Elasticsearch(self.es_url)

    @property
    def connection(self):
        if self._conn is None:
            self.create_new_connection()
        return self._conn

grok.global_utility(ElasticSearch)


class ReloadESConfig(grok.View):
    """ Convenience view for faster debugging. Needs to be manager. """
    grok.context(Interface)
    grok.require('cmf.ManagePortal')
    grok.name('reload_es_config')

    def render(self):
        es = getUtility(IElasticSearch)
        es.reload = True
