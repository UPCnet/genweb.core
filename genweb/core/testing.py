from zope.configuration import xmlconfig

from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class GenwebUPC(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import genweb.core
        xmlconfig.file('configure.zcml',
                       genweb.core,
                       context=configurationContext)

        import upc.genwebupctheme
        xmlconfig.file('configure.zcml',
                       upc.genwebupctheme,
                       context=configurationContext)

        # Install archetypes-based products
        z2.installProduct(app, 'upc.genweb.banners')
        z2.installProduct(app, 'upc.genweb.logosfooter')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'genweb.core:default')
        # Let anz.casclient do not interfere in tests
        # portal.acl_users.manage_delObjects('CASUPC')

    def tearDownZope(self, app):
        # Uninstall archetypes-based products
        z2.uninstallProduct(app, 'upc.genweb.banners')
        z2.uninstallProduct(app, 'upc.genweb.logosfooter')


GENWEBUPC_FIXTURE = GenwebUPC()
GENWEBUPC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(GENWEBUPC_FIXTURE,),
    name="GenwebUPC:Integration")
GENWEBUPC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GENWEBUPC_FIXTURE,),
    name="GenwebUPC:Functional")
# Commented as acceptance tests are not needed for this product
# GENWEBUPC_ACCEPTANCE_TESTING = FunctionalTesting(
#     bases=(GENWEBUPC_FIXTURE, ZSERVER_FIXTURE),
#     name="GenwebUPC:Acceptance")
