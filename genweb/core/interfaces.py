from zope.interface import Interface

class IGenwebLayer(Interface):
    """A layer specific for upc.genweb.core.

    We will use this to register browser pages that should only be used
    when upc.genweb.core is installed in the site.
    """