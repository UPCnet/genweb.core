import unittest2 as unittest
from genweb.core.testing import GENWEB_INTEGRATION_TESTING
from AccessControl import Unauthorized
from zope.component import getMultiAdapter
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import login, logout
from plone.app.testing import setRoles

from genweb.core.browser.helpers import getDorsal
from plone.cachepurging.interfaces import ICachePurgingSettings

import os


class HelperViewsIntegrationTest(unittest.TestCase):

    layer = GENWEB_INTEGRATION_TESTING

    def setconfig(self, **kw):
        import App.config
        config = App.config.getConfiguration()
        for key, value in kw.items():
            setattr(config, key, value)
        App.config.setConfiguration(config)

    def testHelperViewsAvailable(self):
        portal = self.layer['portal']
        self.failUnless(portal.unrestrictedTraverse('configure_site_cache'))

    def testHelperViewsNotAvailableForAnonymous(self):
        logout()
        portal = self.layer['portal']
        self.assertRaises(Unauthorized, portal.restrictedTraverse, 'configure_site_cache')

    def test_getDorsal(self):
        # self.setconfig(product_config={'genwebconfig': {'zeo': '1'}})
        os.environ['dorsal'] = '1'
        self.assertEqual(getDorsal(), os.environ['dorsal'])

    def test_configure_site_cache(self):
        # old way using Zope product_config:
        # self.setconfig(product_config={'genwebconfig': {'zeo': '1'}})
        os.environ['varnish_url'] = 'http://alec.upc.edu:9001'
        portal = self.layer['portal']
        request = self.layer['request']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        cachesetup = getMultiAdapter((portal, request), name='configure_site_cache')
        cachesetup.render()
        registry = queryUtility(IRegistry)
        cachepurginsettings = registry.forInterface(ICachePurgingSettings)
        self.assertEqual(cachepurginsettings.cachingProxies, (os.environ['varnish_url'], ))

    # No longer needed.
    # def test_configure_site_cache_with_2_digits(self):
    #     self.setconfig(product_config={'genwebconfig': {'zeo': '11'}})
    #     portal = self.layer['portal']
    #     request = self.layer['request']
    #     setRoles(portal, TEST_USER_ID, ['Manager'])
    #     login(portal, TEST_USER_NAME)
    #     cachesetup = getMultiAdapter((portal, request), name='configure_site_cache')
    #     cachesetup.render()
    #     registry = queryUtility(IRegistry)
    #     cachepurginsettings = registry.forInterface(ICachePurgingSettings)
    #     self.assertEqual(cachepurginsettings.cachingProxies, ('http://sylar.upc.es:9011', ))
