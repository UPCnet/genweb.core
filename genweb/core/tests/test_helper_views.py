import unittest2 as unittest
from genweb.core.testing import GENWEBUPC_INTEGRATION_TESTING
from AccessControl import Unauthorized
from zope.component import getMultiAdapter
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import login, logout
from plone.app.testing import setRoles

from plone.app.testing import applyProfile

from genweb.core.browser.helpers import getDorsal
from plone.cachepurging.interfaces import ICachePurgingSettings


class HelperViewsIntegrationTest(unittest.TestCase):

    layer = GENWEBUPC_INTEGRATION_TESTING

    def setconfig(self, **kw):
        import App.config
        config = App.config.getConfiguration()
        for key, value in kw.items():
            setattr(config, key, value)
        App.config.setConfiguration(config)

    def testHelperViewsAvailable(self):
        portal = self.layer['portal']
        self.failUnless(portal.unrestrictedTraverse('@@configuraSiteCache'))

    def testHelperViewsNotAvailableForAnonymous(self):
        logout()
        portal = self.layer['portal']
        self.assertRaises(Unauthorized, portal.restrictedTraverse, '@@configuraSiteCache')

    def test_getDorsal(self):
        self.setconfig(product_config={"genwebconfig": {"zeo": "1"}})
        self.assertEqual(getDorsal(), "1")

    def test_configuraSiteCache(self):
        self.setconfig(product_config={"genwebconfig": {"zeo": "1"}})
        portal = self.layer['portal']
        request = self.layer['request']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        cachesetup = getMultiAdapter((portal, request), name='configuraSiteCache')
        cachesetup.render()
        registry = queryUtility(IRegistry)
        cachepurginsettings = registry.forInterface(ICachePurgingSettings)
        self.assertEqual(cachepurginsettings.cachingProxies, ('http://sylar.upc.es:9001', ))

    def test_configuraSiteCache_with_2_digits(self):
        self.setconfig(product_config={"genwebconfig": {"zeo": "11"}})
        portal = self.layer['portal']
        request = self.layer['request']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        cachesetup = getMultiAdapter((portal, request), name='configuraSiteCache')
        cachesetup.render()
        registry = queryUtility(IRegistry)
        cachepurginsettings = registry.forInterface(ICachePurgingSettings)
        self.assertEqual(cachepurginsettings.cachingProxies, ('http://sylar.upc.es:9011', ))
