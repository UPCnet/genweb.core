# -*- coding: utf-8 -*-
from five import grok
from plone import api
from zope.interface import Interface
from repoze.catalog.query import Eq
from repoze.catalog.query import Or
from souper.soup import get_soup
from zope.component import getUtility
from souper.soup import Record
from Products.CMFPlone.interfaces import IPloneSiteRoot

from genweb.core.utils import add_user_to_catalog
from mrs.max.utilities import IMAXClient

import json
import ldap
import re
import os

ALT_LDAP_URI = os.environ.get('alt_ldap_uri', '')
ALT_LDAP_DN = os.environ.get('alt_bind_dn', '')
ALT_LDAP_PASSWORD = os.environ.get('alt_bindpasswd', '')
BASEDN = os.environ.get('alt_base_dn', '')


class Omega13UserSearch(grok.View):
    grok.context(Interface)

    def render(self, result_threshold=100):
        query = self.request.form.get('q', '')
        last_query = self.request.form.get('last_query', '')
        last_query_count = self.request.form.get('last_query_count', 0)
        if query:
            portal = api.portal.get()
            self.request.response.setHeader("Content-type", "application/json")
            soup = get_soup('user_properties', portal)
            searching_surname = len(re.match(r'^[^\ \.]+(?: |\.)*(.*?)$', query).groups()[0])

            normalized_query = query.replace('.', ' ') + '*'
            users_in_soup = [dict(id=r.attrs.get('username'),
                                  displayName=r.attrs.get('fullname'))
                                  for r in soup.query(Or(Eq('username', normalized_query),
                                                         Eq('fullname', normalized_query)))]
            too_much_results = len(users_in_soup) > result_threshold

            is_useless_request = query.startswith(last_query) and len(users_in_soup) == last_query_count

            if is_useless_request and (not too_much_results or searching_surname):
                current_user = api.user.get_current()
                oauth_token = current_user.getProperty('oauth_token', '')

                maxclient, settings = getUtility(IMAXClient)()
                maxclient.setActor(current_user.getId())
                maxclient.setToken(oauth_token)

                max_users = maxclient.people.get(qs={'limit': 0, 'username': query})
                users_in_max = [dict(id=user.get('username'), displayName=user.get('displayName')) for user in max_users]

                for user in users_in_max:
                    add_user_to_catalog(user['id'], dict(displayName=user['displayName']))

                return json.dumps(dict(results=users_in_max,
                                       last_query=query,
                                       last_query_count=len(users_in_max)))
            else:
                return json.dumps(dict(results=users_in_soup,
                                       last_query=query,
                                       last_query_count=len(users_in_soup)))

        else:
            return json.dumps(dict(error='No query found',
                                   last_query='',
                                   last_query_count=0))


class Omega13GroupSearch(grok.View):
    grok.context(Interface)

    def render(self):
        query = self.request.form.get('q', '')
        if query:
            portal = api.portal.get()
            soup = get_soup('ldap_groups', portal)
            normalized_query = query.replace('.', ' ') + '*'

            results = [dict(id=r.attrs.get('id')) for r in soup.query(Eq('searchable_id', normalized_query))]
            return json.dumps(dict(results=results))
        else:
            return json.dumps(dict(id='No results yet.'))


class SyncLDAPGroups(grok.View):
    grok.context(IPloneSiteRoot)
    grok.require('cmf.ManagePortal')

    def render(self):
        conn = ldap.initialize(ALT_LDAP_URI)
        conn.simple_bind_s(ALT_LDAP_DN, ALT_LDAP_PASSWORD)

        try:
            results = conn.search_s(BASEDN, ldap.SCOPE_SUBTREE, '(objectClass=groupOfNames)', ['cn'])
        except:
            # Just in case the user raise a "SIZE_LIMIT_EXCEEDED"
            api.portal.send_email(
                recipient="plone.team@upcnet.es",
                sender="noreply@ulearn.upcnet.es",
                subject="[uLearn] Exception raised: SIZE_LIMIT_EXCEEDED",
                body="The sync view on the uLearn instance has reached the SIZE_LIMIT_EXCEEDED and the groups has not been updated",
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
