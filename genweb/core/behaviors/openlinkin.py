from zope.component import adapts
from zope.interface import implements, alsoProvides
from zope import schema

from plone.directives import form

from plone.app.contenttypes.interfaces import ILink

from genweb.core import _


class IOpenlinkin(form.Schema):
    """Add open in new window field to link content
    """

    openlinkin = schema.Bool(
        title=_(u"open_link_in_new_window"),
        description=_(u"help_open_link_in_new_window"),
        required=False,
        default=False
    )

alsoProvides(IOpenlinkin, form.IFormFieldProvider)


class Openlinkin(object):
    implements(IOpenlinkin)
    adapts(ILink)

    def __init__(self, context):
        self.context = context
