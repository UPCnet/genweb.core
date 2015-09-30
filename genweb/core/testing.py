from zope.configuration import xmlconfig
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE


class Genweb(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE, PLONE_FIXTURE)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import genweb.core
        xmlconfig.file('configure.zcml',
                       genweb.core,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        # Needed for PAC not complain about not having one... T_T
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

        # Install into Plone site using portal_setup
        applyProfile(portal, 'genweb.core:default')

        # Create a document front-page
        # setRoles(portal, TEST_USER_ID, ['Manager'])
        # portal.invokeFactory('Document', 'front-page', title='Us donem la benvinguda a Genweb')
        # transaction.commit()
        # setRoles(portal, TEST_USER_ID, ['Member'])

        # Let anz.casclient do not interfere in tests
        # portal.acl_users.manage_delObjects('CASUPC')

    def tearDownZope(self, app):
        # Uninstall archetypes-based products
        pass

GENWEB_FIXTURE = Genweb()
GENWEB_INTEGRATION_TESTING = IntegrationTesting(
    bases=(GENWEB_FIXTURE,),
    name='Genweb:Integration')
GENWEB_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GENWEB_FIXTURE,),
    name='Genweb:Functional')
# Commented as acceptance tests are not needed for this product
# GENWEBUPC_ACCEPTANCE_TESTING = FunctionalTesting(
#     bases=(GENWEBUPC_FIXTURE, ZSERVER_FIXTURE),
#     name="GenwebUPC:Acceptance")
