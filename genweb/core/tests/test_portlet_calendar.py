# -*- coding: utf-8 -*-
from plone import api
from plone.app.event.base import localized_now
from Products.CMFCore.utils import getToolByName
from genweb.theme.portlets import esdeveniments
from genweb.core.testing import GENWEBUPC_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import setRoles
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.component.hooks import setHooks
from zope.component.hooks import setSite

from plone.app.event.dx.behaviors import EventAccessor

import unittest2 as unittest

TZNAME = "Europe/Vienna"


class RendererTest(unittest.TestCase):
    layer = GENWEBUPC_INTEGRATION_TESTING

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

    def create_event(self, context, id='e1', title='New event', days=(1, 1), start=0, end=1, whole_day=False, open_end=False):
        now = localized_now().replace(minute=0, second=0, microsecond=0)
        if now.day > 30:
            target_day_start = 1
            target_day_end = 1 + days[1]
        else:
            target_day_start = now.day + days[0]
            target_day_end = now.day + days[1]
        if now.hour == 23:
            target_hour_start = 1
            target_hour_end = 2
        else:
            target_hour_start = now.hour + start
            target_hour_end = now.hour + end

        start = localized_now().replace(day=target_day_start, hour=target_hour_start)
        end = localized_now().replace(day=target_day_end, hour=target_hour_end)

        EventAccessor.event_type = 'Event'
        acc = EventAccessor.create(
            container=context,
            content_id=id,
            title=title,
            start=start,
            end=end,
            timezone=TZNAME,
            whole_day=whole_day,
            open_end=open_end
        )
        acc.location = u"Graz, Austria"

        return context[id]

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
        assignment = assignment or esdeveniments.Assignment()

        return getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer
        )

    def test_basic_event(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        event = self.create_event(self.folder)
        api.content.transition(event, to_state='published')
        portlet = self.renderer(context=self.folder, assignment=esdeveniments.Assignment())
        portlet.update()
        rd = portlet.render()

        near_event = portlet.published_events()
        self.assertTrue(len(near_event) == 1)
        self.assertTrue('e1' in rd)

    def test_whole_day_event_spanning_one_day(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        event = self.create_event(self.folder, whole_day=True)
        api.content.transition(event, to_state='published')
        portlet = self.renderer(context=self.folder, assignment=esdeveniments.Assignment())
        portlet.update()
        rd = portlet.render()

        near_event = portlet.published_events()
        self.assertTrue(len(near_event) == 1)
        self.assertTrue('e1' in rd)

    def test_whole_day_event_spanning_two_days(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        event = self.create_event(self.folder, days=(1, 2), whole_day=True)
        api.content.transition(event, to_state='published')
        portlet = self.renderer(context=self.folder, assignment=esdeveniments.Assignment())
        portlet.update()
        rd = portlet.render()

        near_event = portlet.published_events()
        self.assertTrue(len(near_event) == 1)
        self.assertTrue('e1' in rd)
