# -*- coding: utf-8 -*-
from five import grok
from plone import api
from repoze.catalog.query import Eq
from souper.soup import get_soup
from souper.soup import Record
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from genweb.controlpanel.core import IGenwebCoreControlPanelSettings
from zope.interface import alsoProvides

import ldap
import os


def get_ldap_config():
    """ return config ldap """
    registry = queryUtility(IRegistry)
    gw_settings = registry.forInterface(IGenwebCoreControlPanelSettings)
    ALT_LDAP_URI = gw_settings.alt_ldap_uri if gw_settings.alt_ldap_uri is not None else os.environ.get('alt_ldap_uri', '')
    ALT_LDAP_DN = gw_settings.alt_bind_dn if gw_settings.alt_bind_dn is not None else os.environ.get('alt_bind_dn', '')
    ALT_LDAP_PASSWORD = gw_settings.alt_bindpasswd if gw_settings.alt_bindpasswd is not None else os.environ.get('alt_bindpasswd', '')
    BASEDN = gw_settings.alt_base_dn if gw_settings.alt_base_dn is not None else os.environ.get('alt_base_dn', '')
    GROUPS_QUERY = gw_settings.groups_query if gw_settings.groups_query is not None else os.environ.get('groups_query', '')
    USER_GROUPS_QUERY = gw_settings.user_groups_query if gw_settings.user_groups_query is not None else os.environ.get('user_groups_query', '')

    return ALT_LDAP_URI, ALT_LDAP_DN, ALT_LDAP_PASSWORD, BASEDN, GROUPS_QUERY, USER_GROUPS_QUERY


def search_ldap_groups():
    ALT_LDAP_URI, ALT_LDAP_DN, ALT_LDAP_PASSWORD, BASEDN, GROUPS_QUERY, USER_GROUPS_QUERY = get_ldap_config()
    conn = ldap.initialize(ALT_LDAP_URI)
    conn.simple_bind_s(ALT_LDAP_DN, ALT_LDAP_PASSWORD)
    return conn.search_s(BASEDN, ldap.SCOPE_SUBTREE, GROUPS_QUERY, ['cn'])


class SyncLDAPGroups(grok.View):
    grok.context(IPloneSiteRoot)
    grok.require('cmf.ManagePortal')

    def render(self):

        try:
            results = search_ldap_groups()
        except:
            # Just in case the user raise a "SIZE_LIMIT_EXCEEDED"
            api.portal.send_email(
                recipient='plone.team@upcnet.es',
                sender='noreply@ulearn.upcnet.es',
                subject='[uLearn] Exception raised: SIZE_LIMIT_EXCEEDED',
                body='The sync view on the uLearn instance has reached the SIZE_LIMIT_EXCEEDED and the groups has not been updated',
            )

        try:
            from plone.protect.interfaces import IDisableCSRFProtection
            alsoProvides(self.request, IDisableCSRFProtection)
        except:
            pass

        if results:
            portal = api.portal.get()
            soup = get_soup('ldap_groups', portal)
            soup.clear()
            to_print = []

            for dn, attrs in results:
                group_id = attrs['cn'][0]
                exist = [r for r in soup.query(Eq('id', group_id))]
                if exist:
                    to_print.append('* Already existing record for group: {}'.format(group_id))
                else:
                    record = Record()
                    record.attrs['id'] = group_id

                    # Index entries MUST be unicode in order to search using special chars
                    record.attrs['searchable_id'] = group_id.decode('utf-8')
                    soup.add(record)
                    to_print.append('Added record for group: {}'.format(group_id))

            return '\n'.join(to_print)
        else:
            return 'No results'
