

class PloneLibrary(object):

    def get_site_owner_name(self):
        import plone.app.testing
        return plone.app.testing.interfaces.SITE_OWNER_NAME

    def get_site_owner_password(self):
        import plone.app.testing
        return plone.app.testing.interfaces.SITE_OWNER_PASSWORD
