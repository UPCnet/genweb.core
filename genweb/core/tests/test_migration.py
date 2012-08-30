# -*- coding: utf-8 -*-
import unittest2 as unittest
from os.path import abspath
from os.path import dirname
from os.path import join
from AccessControl import Unauthorized
from zope.component import getMultiAdapter
from zope.component import queryUtility

from Products.CMFCore.utils import getToolByName
from Products.LinguaPlone.tests.utils import makeTranslation

from plone.registry.interfaces import IRegistry
from plone.app.folder.utils import findObjects
from plone.locking.interfaces import ILockable

from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import login, logout
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.testing import z2

from genweb.core.testing import GENWEBUPC_INTEGRATION_TESTING
from genweb.controlpanel.interface import IGenwebControlPanelSettings


class MigrationIntegrationTest(unittest.TestCase):

    layer = GENWEBUPC_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def testHelperViewsAvailable(self):
        portal = self.layer['portal']
        self.failUnless(portal.unrestrictedTraverse('@@migrateControlPanel'))

    def testHelperViewsNotAvailableForAnonymous(self):
        portal = self.layer['portal']
        self.assertRaises(Unauthorized, portal.restrictedTraverse, '@@migrateControlPanel')

    def test_migrateControlPanel(self):
        portal = self.layer['portal']
        request = self.layer['request']
        applyProfile(portal, 'upc.genwebupctheme:default')
        applyProfile(portal, 'genweb.controlpanel:default')
        genweb_props = getToolByName(portal, 'portal_properties').genwebupc_properties

        # Fix unicode errors in legacy control panel
        genweb_props.titolespai_ca = "Títol de l'espai en català".decode('utf-8')
        genweb_props.titolespai_es = "Títol de l'espai en castellà".decode('utf-8')
        genweb_props.titolespai_en = "Títol de l'espai en anglès".decode('utf-8')
        genweb_props.firmaunitat_ca = "Firma de la unitat en català".decode('utf-8')
        genweb_props.firmaunitat_es = "Firma de la unitat en castellà".decode('utf-8')
        genweb_props.firmaunitat_en = "Firma de la unitat en anglès".decode('utf-8')

        registry = queryUtility(IRegistry)
        genweb_settings = registry.forInterface(IGenwebControlPanelSettings)
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        migrationview = getMultiAdapter((portal, request), name='migrateControlPanel')
        migrationview.render()

        self.assertEqual(genweb_settings.html_title_ca, genweb_props.titolespai_ca)
        self.assertEqual(genweb_settings.amaga_identificacio, False)

        self.assertEqual(genweb_settings.treu_menu_horitzontal, False)

    def test_migrateSecciotype(self):
        z2.installProduct(self.layer['app'], 'Products.LinguaPlone')
        path = join(abspath(dirname(__file__)), 'seccio.zexp')
        path_ca = join(abspath(dirname(__file__)), 'seccio-ca.zexp')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        ptypes = getToolByName(self.portal, 'portal_types')
        ptypes['Plone Site'].allowed_content_types = ['Document', 'File', 'Folder', 'Image', 'Seccio']
        pw = getToolByName(self.portal, 'portal_workflow')
        pw.setDefaultChain('genweb_simple')
        pw.setChainForPortalTypes(('Seccio',), 'genweb_simple')
        self.portal._importObjectFromFile(path)
        self.portal._importObjectFromFile(path_ca)

        self.assertEqual(len([obj for obj in findObjects(self.portal['arealseccio'])]), 6)
        test_page = self.portal['arealseccio'].unrestrictedTraverse('/plone/arealseccio/anotherfolder/withotherfolder/otherpage')
        self.assertEqual(test_page.id, 'otherpage')

        # Lock a page for testing
        ILockable(test_page).lock()
        self.assertEqual(ILockable(test_page).locked(), True)

        # Once we have the fixture in place, test the migration
        migrationview = getMultiAdapter((self.portal, self.request), name='migrateSeccioType')
        migrationview.render()

        # Test the new objects are the same, and are correct.
        self.assertEqual(self.portal['arealseccio'].portal_type, 'Folder')
        self.assertEqual(self.portal['arealseccio_old'].portal_type, 'Seccio')
        self.assertEqual(self.portal['arealseccio_old'].objectIds(), [])
        self.assertEqual(len([obj for obj in findObjects(self.portal['arealseccio'])]), 6)
        self.assertEqual(test_page.id, 'otherpage')

        self.assertEqual(self.portal['arealseccio'].getLanguage(), 'en')
        self.assertEqual(self.portal['arealseccio'].getTranslations().keys(), ['ca', 'en'])
        self.assertEqual(self.portal['arealseccio'].getTranslations()['ca'][0], self.portal['arealseccio-ca'])
