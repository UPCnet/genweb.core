from plone.app.contentmenu.menu import DisplaySubMenuItem
from genweb.core import GenwebMessageFactory as _


class gwDisplaySubMenuItem(DisplaySubMenuItem):

    title = _(u'label_choose_template', default=u'Display')
