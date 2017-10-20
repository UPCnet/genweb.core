# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone import api
from genweb.core.testing import GENWEB_INTEGRATION_TESTING
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

from repoze.catalog.query import Eq
from repoze.catalog.query import Contains
from souper.soup import get_soup
from souper.soup import Record


class TestOmega13(unittest.TestCase):

    layer = GENWEB_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_directory_self_updates_on_user_creation(self):
        api.user.create(email='test@upcnet.es', username='testdirectory',
                        properties=dict(fullname='Test Directory User',
                                        location='Barcelona',
                                        ubicacio='NX',
                                        telefon='44002, 54390'))
        portal = api.portal.get()
        soup = get_soup('user_properties', portal)
        exist = [r for r in soup.query(Eq('username', 'testdirectory'))]
        self.assertEqual('44002, 54390', exist[0].attrs['telefon'])
        exist = [r for r in soup.query(Eq('fullname', 'Test*'))]
        self.assertEqual(u'Test Directory User', exist[0].attrs['fullname'])

    def test_directory_self_updates_on_user_property_edit(self):
        api.user.create(email='test@upcnet.es', username='testdirectory',
                        properties=dict(fullname='Test Directory User',
                                        location='Barcelona',
                                        ubicacio='NX',
                                        telefon='44002, 54390'))
        portal = api.portal.get()
        user = api.user.get(username='testdirectory')
        user.setMemberProperties(mapping={'location': 'Barcelona', 'telefon': '654321'})
        soup = get_soup('user_properties', portal)
        exist = [r for r in soup.query(Eq('username', 'testdirectory'))]
        self.assertEqual('654321', exist[0].attrs['telefon'])
        self.assertEqual('Barcelona', exist[0].attrs['location'])

    def test_full_directory_update(self):
        api.user.create(email='test@upcnet.es', username='testdirectory',
                        properties=dict(fullname='Test Directory User',
                                        location='Barcelona',
                                        ubicacio='NX',
                                        telefon='44002, 54390'))
        api.user.create(email='test@upcnet.es', username='testdirectory2',
                        properties=dict(fullname='Test Directory User',
                                        location='Barcelona',
                                        ubicacio='NX',
                                        telefon='44002, 54390'))

        view = getMultiAdapter((self.portal, self.request), name='rebuild_user_catalog')
        view.render()

    def test_directory_self_updates_on_user_creation_with_unicode(self):
        api.user.create(email='test@upcnet.es', username='testdirectory',
                        properties=dict(fullname=u'Víctor',
                                        location=u'Barcelona',
                                        ubicacio=u'NX',
                                        telefon=u'44002, 54390'))
        portal = api.portal.get()
        soup = get_soup('user_properties', portal)
        exist = [r for r in soup.query(Eq('username', 'testdirectory'))]
        self.assertEqual('44002, 54390', exist[0].attrs['telefon'])
        exist = [r for r in soup.query(Eq('fullname', u'Ví*'))]
        self.assertEqual(u'Víctor', exist[0].attrs['fullname'])
