from zope.configuration import xmlconfig

from plone.testing import z2
from plone.testing.z2 import ZSERVER_FIXTURE
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

        import Products.PloneLDAP
        xmlconfig.file('configure.zcml',
                       Products.PloneLDAP,
                       context=configurationContext)

        # Install archetypes-based products
        z2.installProduct(app, 'upc.genweb.banners')
        z2.installProduct(app, 'upc.genweb.logosfooter')
        z2.installProduct(app, 'Products.PloneFormGen')
        z2.installProduct(app, 'Products.Collage')
        z2.installProduct(app, 'Products.PlonePopoll')
        z2.installProduct(app, 'Products.windowZ')
        z2.installProduct(app, 'Products.Ploneboard')
        z2.installProduct(app, 'Products.PloneSurvey')
        z2.installProduct(app, 'upc.genweb.meetings')
        z2.installProduct(app, 'upcnet.simpleTask')
        # z2.installProduct(app, 'Products.Poi')

        # Productes addicionals opcionals
        z2.installProduct(app, 'upc.genweb.serveis')
        z2.installProduct(app, 'upc.genweb.descriptorTIC')
        z2.installProduct(app, 'upc.genweb.kbpuc')
        z2.installProduct(app, 'upc.genweb.objectiusCG')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'genweb.core:default')
        # Let anz.casclient do not interfere in tests
        portal.acl_users.manage_delObjects('CASUPC')

    def tearDownZope(self, app):
        # Uninstall archetypes-based products
        z2.uninstallProduct(app, 'upc.genweb.banners')
        z2.uninstallProduct(app, 'upc.genweb.logosfooter')
        z2.uninstallProduct(app, 'Products.PloneFormGen')
        z2.uninstallProduct(app, 'Products.Collage')
        z2.uninstallProduct(app, 'Products.PlonePopoll')
        z2.uninstallProduct(app, 'Products.windowZ')
        z2.uninstallProduct(app, 'Products.Ploneboard')
        z2.uninstallProduct(app, 'Products.PloneSurvey')
        z2.uninstallProduct(app, 'upc.genweb.meetings')
        z2.uninstallProduct(app, 'upcnet.simpleTask')
        # z2.uninstallProduct(app, 'Products.Poi')

        # Productes addicionals opcionals
        z2.uninstallProduct(app, 'upc.genweb.serveis')
        z2.uninstallProduct(app, 'upc.genweb.descriptorTIC')
        z2.uninstallProduct(app, 'upc.genweb.kbpuc')
        z2.uninstallProduct(app, 'upc.genweb.objectiusCG')


GENWEBUPC_FIXTURE = GenwebUPC()
GENWEBUPC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(GENWEBUPC_FIXTURE,),
    name="GenwebUPC:Integration")
GENWEBUPC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GENWEBUPC_FIXTURE,),
    name="GenwebUPC:Functional")
GENWEBUPC_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(GENWEBUPC_FIXTURE, ZSERVER_FIXTURE),
    name="GenwebUPC:Acceptance")
