# -*- coding: utf-8 -*-
from five import grok
from plone import api
from repoze.catalog.query import Eq
from souper.soup import get_soup
from souper.soup import Record
from Products.CMFPlone.interfaces import IPloneSiteRoot

import ldap
import os

ALT_LDAP_URI = os.environ.get('alt_ldap_uri', '')
ALT_LDAP_DN = os.environ.get('alt_bind_dn', '')
ALT_LDAP_PASSWORD = os.environ.get('alt_bindpasswd', '')
BASEDN = os.environ.get('alt_base_dn', '')


def search_ldap_groups():
    conn = ldap.initialize(ALT_LDAP_URI)
    conn.simple_bind_s(ALT_LDAP_DN, ALT_LDAP_PASSWORD)
    return conn.search_s(BASEDN, ldap.SCOPE_SUBTREE, '(objectClass=groupOfNames)', ['cn'])


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

        if results:
            portal = api.portal.get()
            soup = get_soup('ldap_groups', portal)
            to_print = []

            for dn, attrs in results:
                group_id = attrs['cn'][0]
                exist = [r for r in soup.query(Eq('id', group_id))]
                if exist:
                    to_print.append('* Already existing record for group: {}'.format(group_id))
                else:
                    record = Record()
                    record.attrs['id'] = group_id
                    record.attrs['searchable_id'] = group_id
                    soup.add(record)
                    to_print.append('Added record for group: {}'.format(group_id))

            return '\n'.join(to_print)
        else:
            return 'No results'
