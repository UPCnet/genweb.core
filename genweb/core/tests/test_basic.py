import unittest2 as unittest
from genweb.core.testing import GENWEBUPC_INTEGRATION_TESTING
from genweb.core.testing import GENWEBUPC_FUNCTIONAL_TESTING
from AccessControl import Unauthorized
from zope.component import getMultiAdapter, queryUtility
from Products.CMFCore.utils import getToolByName

from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import login, logout
from plone.app.testing import setRoles
from plone.app.testing import applyProfile

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from genweb.core.interfaces import IHomePage
from genweb.theme.portlets import homepage

import transaction


class IntegrationTest(unittest.TestCase):

    layer = GENWEBUPC_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def testSetupViewAvailable(self):
        portal = self.layer['portal']
        self.failUnless(portal.unrestrictedTraverse('@@setup-view'))

    def testSetupViewNotAvailableForAnonymous(self):
        portal = self.layer['portal']
        self.assertRaises(Unauthorized, portal.restrictedTraverse, '@@setup-view')

    def testSetupView(self):
        portal = self.layer['portal']
        request = self.layer['request']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        setupview = getMultiAdapter((portal, request), name='setup-view')
        setupview.createContent()
        self.assertEqual(portal['news'].Title(), u"News")
        self.assertEqual(portal['banners-es'].Title(), u"Banners")
        self.assertEqual(portal['logosfooter-ca'].Title(), u"Logos peu")

    def testTemplatesFolderPermissions(self):
        portal = self.layer['portal']
        request = self.layer['request']
        # Login as manager
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        setupview = getMultiAdapter((portal, request), name='setup-view')
        setupview.createContent()
        logout()
        acl_users = getToolByName(portal, 'acl_users')
        acl_users.userFolderAddUser('user1', 'secret', ['Member', 'Contributor', 'Editor', 'Reader', 'Reviewer'], [])
        # setRoles(portal, 'user1', ['Contributor', 'Editor', 'Reader', 'Reviewer'])
        login(portal, 'user1')
        self.assertRaises(Unauthorized, portal.manage_delObjects, 'templates')

    def testPortalConstrains(self):
        portal_allowed_types = ['Folder', 'File', 'Image', 'Document']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.assertEqual(sorted([ct.id for ct in self.portal.allowedContentTypes()]), sorted(portal_allowed_types))

    def testLinkExtender(self):
        """Test for ATLink extender and related index and metadata"""
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'f2', title=u"Soc una carpeta")
        f2 = portal['f2']
        f2.invokeFactory('Link', 'enllac', title=u"Soc un link")
        link = f2['enllac']
        self.assertEqual(link.obrirfinestra, False)

        results = portal.portal_catalog.searchResults(portal_type='Link')
        self.assertEqual(results[0].obrirEnFinestraNova, False)

        link.obrirfinestra = True
        link.reindexObject()

        results = portal.portal_catalog.searchResults(portal_type='Link')
        self.assertEqual(results[0].obrirEnFinestraNova, True)

    def testHomePageMarkerInterface(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        setupview = getMultiAdapter((self.portal, self.request), name='setup-view')
        setupview.createContent()
        logout()
        self.assertTrue(IHomePage.providedBy(self.portal['benvingut']))

    def testAdapters(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Document', 'test_adapter', title=u"Soc una pagina")
        from genweb.core.adapters import IImportant
        obj = IImportant(self.portal.test_adapter)
        self.assertEqual(obj.is_important, False)
        obj.is_important = True
        obj2 = IImportant(self.portal.test_adapter)
        self.assertEqual(obj2.is_important, True)


class FunctionalTest(unittest.TestCase):

    layer = GENWEBUPC_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.app = self.layer['app']
        self.browser = Browser(self.app)
        # Let anz.casclient do not interfere in tests
        # self.portal.acl_users.manage_delObjects('CASUPC')
        # Setup view, to put all default pages in place
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        setupview = getMultiAdapter((self.portal, self.request), name='setup-view')
        setupview.createContent()
        transaction.commit()

        # Create a portlet in a slot
        benvingut = self.portal['benvingut']
        manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager2', context=benvingut)
        assignments = getMultiAdapter((benvingut, manager), IPortletAssignmentMapping)
        homepage_assignment = homepage.Assignment()
        assignments['homepage'] = homepage_assignment
        transaction.commit()
        logout()
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def testHomePagePortlet(self):
        portalURL = self.portal.absolute_url()

        self.browser.open(portalURL)

        self.assertTrue("Us donem la benvinguda a Genweb UPC" in self.browser.contents)
