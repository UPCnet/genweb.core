from zope.interface import Interface


class IGenwebLayer(Interface):
    """A layer specific for genweb.core.

    We will use this to register browser pages that should only be used
    when genweb.core is installed in the site.
    """


class IConstrainedFolder(Interface):
    """ Marker interface for constrained folders """


class IHomePage(Interface):
    """ Marker interface for home page documents """


class ITranslatable(Interface):
    """ Fake marker interface in case Products.LinguaPlone is not installed """


class IGenwebUtils(Interface):
    """ Marker describing the functionality of the convenience methods
        placeholder genweb.utils view.
    """

    def havePermissionAtRoot(self):
        """Funcio que retorna si es Editor a l'arrel"""

    def getDadesUnitat(self):
        """ Retorna les dades proporcionades pel WebService del SCP """

    def getContentClass(self, view=None):
        """ Returns the correct class for content container (span) """
