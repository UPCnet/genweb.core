# -*- coding: utf-8 -*-
from plone import api
from Products.CMFCore.utils import getToolByName
from genweb.theme.portlets import news_events_listing
from genweb.core.testing import GENWEB_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.component.hooks import setHooks
from zope.component.hooks import setSite

import unittest2 as unittest


class NewsEventsRendererTest(unittest.TestCase):
    layer = GENWEB_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.request = self.layer['request']
        self.wft = getToolByName(self.portal, 'portal_workflow')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        setHooks()
        setSite(portal)
        folder_id = self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal[folder_id]

        # Make sure Events use simple_publication_workflow
        self.portal.portal_workflow.setChainForPortalTypes(
            ['Event'], ['simple_publication_workflow']
        )

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.portal
        request = request or self.request
        view = view or context.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager,
            name='plone.rightcolumn',
            context=self.portal
        )

        return getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer
        )

    def test_portlet_newsevents(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        portlet = self.renderer(context=self.portal, assignment=news_events_listing.Assignment(('tag1'), ('Events')))
        portlet.update()
        portlet.render()
