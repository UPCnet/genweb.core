from zope.i18nmessageid import MessageFactory
GenwebMessageFactory = MessageFactory('genweb')

import pkg_resources

try:
    pkg_resources.get_distribution('Products.LinguaPlone')
except pkg_resources.DistributionNotFound:
    HAS_LINGUAPLONE = False
    from genweb.core.interfaces import ITranslatable
else:
    HAS_LINGUAPLONE = True
    from Products.LinguaPlone.interfaces import ITranslatable

try:
    pkg_resources.get_distribution('upcnet.cas')
except pkg_resources.DistributionNotFound:
    HAS_CAS = False
else:
    HAS_CAS = True

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_DXCT = False
else:
    HAS_DXCT = True


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
