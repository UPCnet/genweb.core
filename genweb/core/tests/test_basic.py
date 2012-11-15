import unittest2 as unittest
from genweb.core.testing import GENWEBUPC_INTEGRATION_TESTING
from genweb.core.testing import GENWEBUPC_FUNCTIONAL_TESTING
from AccessControl import Unauthorized
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import login, logout
from plone.app.testing import setRoles

from plone.app.testing import applyProfile

from genweb.core.interfaces import IHomePage


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

    def testBasicProducts(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'f1', title=u"Soc una carpeta")
        f1 = portal['f1']

        # Collage
        f1.invokeFactory('Collage', 'collage', title=u"Soc un collage")
        self.assertEqual(f1['collage'].Title(), u"Soc un collage")
        # PloneFormGen
        f1.invokeFactory('FormFolder', 'formulari', title=u"Soc un formulari")
        self.assertEqual(f1['formulari'].Title(), u"Soc un formulari")
        # PlonePopoll
        f1.invokeFactory('PlonePopoll', 'enquesta', title=u"Soc una enquesta")
        self.assertEqual(f1['enquesta'].Title(), u"Soc una enquesta")
        # windowZ
        f1.invokeFactory('Window', 'window', title=u"Soc un window")
        self.assertEqual(f1['window'].Title(), u"Soc un window")
        # Ploneboard
        f1.invokeFactory('Ploneboard', 'forum', title=u"Soc un forum")
        self.assertEqual(f1['forum'].Title(), u"Soc un forum")
        # PloneSurvey
        f1.invokeFactory('Survey', 'questionari', title=u"Soc un questionari")
        self.assertEqual(f1['questionari'].Title(), u"Soc un questionari")
        # Meeting
        f1.invokeFactory('Meeting', 'reunio', title=u"Soc una reunio")
        self.assertEqual(f1['reunio'].Title(), u"Soc una reunio")
        # Tasques
        f1.invokeFactory('simpleTask', 'tasca', title=u"Soc una tasca")
        self.assertEqual(f1['tasca'].Title(), u"Soc una tasca")

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

    def testAdditionalProducts(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'f1', title=u"Soc una carpeta")
        f1 = portal['f1']

        # Serveis
        applyProfile(portal, 'upc.genweb.serveis:default')
        f1.invokeFactory('Servei', 'servei', title=u"Soc un servei")
        self.assertEqual(f1['servei'].Title(), u"Soc un servei")

        # Descriptor TIC
        applyProfile(portal, 'upc.genweb.descriptorTIC:default')
        f1.invokeFactory('CarpetaTIC', 'carpetaTIC', title=u"Soc una carpetaTIC")
        self.assertEqual(f1['carpetaTIC'].Title(), u"Soc una carpetaTIC")

        # ObjectiusCG
        applyProfile(portal, 'upc.genweb.objectiusCG:default')
        f1.invokeFactory('ObjectiuGeneralCG', 'objectiuGeneralCG', title=u"Soc una objectiuGeneralCG")
        self.assertEqual(f1['objectiuGeneralCG'].Title(), u"Soc una objectiuGeneralCG")

    def testFolderConstrains(self):
        from genweb.core.events import CONSTRAINED_TYPES, IMMEDIATELY_ADDABLE_TYPES
        from zope.event import notify
        from Products.Archetypes.event import ObjectInitializedEvent
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Folder', 'userfolder', title=u"Soc una carpeta")
        folder = self.portal['userfolder']
        notify(ObjectInitializedEvent(folder))
        self.assertEqual(sorted(folder.getLocallyAllowedTypes()), sorted(CONSTRAINED_TYPES))
        self.assertEqual(sorted(folder.getImmediatelyAddableTypes()), sorted(IMMEDIATELY_ADDABLE_TYPES))

    def testPortalConstrains(self):
        portal_allowed_types = ['Folder', 'File', 'Image', 'Document']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.assertEqual(sorted([ct.id for ct in self.portal.allowedContentTypes()]), sorted(portal_allowed_types))

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
        self.assertEqual(obj.is_important, True)


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
        logout()
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        import transaction
        transaction.commit()

    def testHomePage(self):
        portalURL = self.portal.absolute_url()
        self.browser.open(portalURL)

        self.assertTrue(u"Benvingut" in self.browser.contents)
