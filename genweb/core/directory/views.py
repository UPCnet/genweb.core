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
import logging
import ldap
import os

logger = logging.getLogger(__name__)


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
    grok.require('zope2.View')

    def render(self):
        results = []
        try:
            results = search_ldap_groups()
        except ldap.SERVER_DOWN:
            api.portal.send_email(
                recipient='plone.team@upcnet.es',
                sender='noreply@ulearn.upcnet.es',
                subject='[uLearn] No LDAP SERVER found in ' + self.context.absolute_url(),
                body="Can't contact with ldap_server to syncldapgroups in " + self.context.absolute_url(),
            )
            return "Can't connect LDAP_SERVER."
        except:
            # Just in case the user raise a "SIZE_LIMIT_EXCEEDED"
            api.portal.send_email(
                recipient='plone.team@upcnet.es',
                sender='noreply@ulearn.upcnet.es',
                subject='[uLearn] Exception raised: SIZE_LIMIT_EXCEEDED at ' + self.context.absolute_url(),
                body='The sync view on the uLearn instance ' + self.context.absolute_url() + ' has reached the SIZE_LIMIT_EXCEEDED and groups have not been updated.',
            )
            return "Error searching groups."

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
                if 'cn' in attrs:
                    group_id = attrs['cn'][0]

                    record = Record()
                    record.attrs['id'] = group_id

                    # Index entries MUST be unicode in order to search using special chars
                    record.attrs['searchable_id'] = group_id.decode('utf-8')
                    soup.add(record)
                    to_print.append(group_id)

            logger.info('[SYNCLDAPGROUPS]: {}'.format(to_print))
            api.portal.send_email(
                recipient='UPCnet.ServOp.WaCS@llistes.upcnet.es',
                sender='noreply@ulearn.upcnet.es',
                subject='[uLearn] OK! Import LDAP groups: ' + self.context.absolute_url(),
                body='OK - Sync LDAP groups to communities. URL: ' + self.context.absolute_url(),
            )

            return 'Ok, groups imported.'
        else:
            api.portal.send_email(
                recipient='UPCnet.ServOp.WaCS@llistes.upcnet.es',
                sender='noreply@ulearn.upcnet.es',
                subject='[uLearn] FAIL! Import LDAP groups: ' + self.context.absolute_url(),
                body='KO - No groups found syncing LDAP groups to communities. URL: ' + self.context.absolute_url(),
            )
            return 'KO, no groups found.'
