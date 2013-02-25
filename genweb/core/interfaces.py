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
