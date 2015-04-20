from five import grok
from plone import api
from Products.PluggableAuthService.interfaces.authservice import IPropertiedUser
from Products.PluggableAuthService.interfaces.events import IPrincipalCreatedEvent
from Products.PluggableAuthService.interfaces.events import IPropertiesUpdatedEvent
from repoze.catalog.query import Eq
from souper.interfaces import ICatalogFactory
from souper.soup import get_soup
from souper.soup import Record
from zope.component import getUtility
from zope.component import getUtilitiesFor

from genweb.core import IAMULEARN
from genweb.core.directory import METADATA_USER_ATTRS

import unicodedata


@grok.subscribe(IPropertiedUser, IPrincipalCreatedEvent)
@grok.subscribe(IPropertiedUser, IPropertiesUpdatedEvent)
def add_user_to_catalog(principal, event):
    """ This subscriber hooks on user creation and adds user properties to the
        soup-based catalog for later searches
    """
    portal = api.portal.get()
    soup = get_soup('user_properties', portal)
    exist = [r for r in soup.query(Eq('id', principal.getUserName()))]
    user_properties_utility = getUtility(ICatalogFactory, name='user_properties')

    if exist:
        user_record = exist[0]
    else:
        record = Record()
        record_id = soup.add(record)
        user_record = soup.get(record_id)

    if isinstance(principal.getUserName(), str):
        user_record.attrs['username'] = principal.getUserName().decode('utf-8')
        user_record.attrs['id'] = principal.getUserName().decode('utf-8')
    else:
        user_record.attrs['username'] = principal.getUserName()
        user_record.attrs['id'] = principal.getUserName()

    if IPropertiesUpdatedEvent.providedBy(event):
        for attr in user_properties_utility.properties + METADATA_USER_ATTRS:
            if attr in event.properties:
                if isinstance(event.properties[attr], str):
                    user_record.attrs[attr] = event.properties[attr].decode('utf-8')
                else:
                    user_record.attrs[attr] = event.properties[attr]

    # Build the searchable_text field for wildcard searches
    user_record.attrs['searchable_text'] = ' '.join([unicodedata.normalize('NFKD', user_record.attrs[key]).encode('ascii', errors='ignore') for key in user_properties_utility.properties if user_record.attrs.get(key, False)])

    soup.reindex(records=[user_record])

    # If uLearn is present, then lookup for a customized set of fields and its
    # related soup. The soup has the form 'user_properties_<client_name>'. This
    # feature is currently restricted to uLearn as the client name (in fact, we
    # are reusing the domain name) is stored in MAX settings but should be easy
    # to backport it to Genweb as long as it gets its own storage for the
    # <client_name> value.
    if IAMULEARN:
        try:
            client = api.portal.get_registry_record('mrs.max.browser.controlpanel.IMAXUISettings.domain')
        except:
            client = ''

        if 'user_properties_{}'.format(client) in [a[0] for a in getUtilitiesFor(ICatalogFactory)]:
            extended_soup = get_soup('user_properties_{}'.format(client), portal)
            exist = []
            exist = [r for r in extended_soup.query(Eq('id', principal.getUserName()))]
            extended_user_properties_utility = getUtility(ICatalogFactory, name='user_properties_{}'.format(client))

            if exist:
                extended_user_record = exist[0]
            else:
                record = Record()
                record_id = extended_soup.add(record)
                extended_user_record = extended_soup.get(record_id)

            if isinstance(principal.getUserName(), str):
                extended_user_record.attrs['username'] = principal.getUserName().decode('utf-8')
                extended_user_record.attrs['id'] = principal.getUserName().decode('utf-8')
            else:
                extended_user_record.attrs['username'] = principal.getUserName()
                extended_user_record.attrs['id'] = principal.getUserName()

            if IPropertiesUpdatedEvent.providedBy(event):
                for attr in extended_user_properties_utility.properties:
                    if attr in event.properties:
                        if isinstance(event.properties[attr], str):
                            extended_user_record.attrs[attr] = event.properties[attr].decode('utf-8')
                        else:
                            extended_user_record.attrs[attr] = event.properties[attr]

            # Update the searchable_text of the standard user record field with
            # the ones in the extended catalog
            user_record.attrs['searchable_text'] = user_record.attrs['searchable_text'] + ' '.join([unicodedata.normalize('NFKD', extended_user_record.attrs[key]).encode('ascii', errors='ignore') for key in extended_user_properties_utility.properties if extended_user_record.attrs.get(key, False)])

            # Save for free the extended properties in the main user_properties soup
            # for easy access with one query
            for attr in extended_user_properties_utility.properties:
                if attr in event.properties:
                    if isinstance(event.properties[attr], str):
                        user_record.attrs[attr] = event.properties[attr].decode('utf-8')
                    else:
                        user_record.attrs[attr] = event.properties[attr]

            soup.reindex(records=[user_record])
            extended_soup.reindex(records=[extended_user_record])
