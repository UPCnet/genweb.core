from zope.i18nmessageid import MessageFactory
GenwebMessageFactory = MessageFactory('genweb.core')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
