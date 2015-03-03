# -*- coding: utf-8 -*-
from five import grok
from plone import api
from zope.interface import Interface
from repoze.catalog.query import Eq
from repoze.catalog.query import Or
from souper.soup import get_soup
from zope.component import getUtility

from genweb.core.utils import add_user_to_catalog
from mrs.max.utilities import IMAXClient

import json
import re


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
