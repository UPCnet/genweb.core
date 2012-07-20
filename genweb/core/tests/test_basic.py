import unittest2 as unittest
from genweb.core.testing import GENWEBUPC_INTEGRATION_TESTING
from AccessControl import Unauthorized
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import login, logout
from plone.app.testing import setRoles

from plone.app.testing import applyProfile


class IntegrationTest(unittest.TestCase):

    layer = GENWEBUPC_INTEGRATION_TESTING

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
        request = self.layer['request']
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

        # Extender dels links
        f1.invokeFactory('Link', 'enllac', title=u"Soc un link")
        link = f1['enllac']
        self.assertEqual(link.obrirfinestra, False)

    def testAdditionalProducts(self):
        portal = self.layer['portal']
        request = self.layer['request']
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
