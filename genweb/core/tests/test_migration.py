# -*- coding: utf-8 -*-
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

from genweb.controlpanel.interface import IGenwebControlPanelSettings


class MigrationIntegrationTest(unittest.TestCase):

    layer = GENWEBUPC_INTEGRATION_TESTING

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
