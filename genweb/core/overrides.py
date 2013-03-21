from plone.app.contentmenu.menu import DisplaySubMenuItem, FactoriesSubMenuItem
from genweb.core import GenwebMessageFactory as _


class gwDisplaySubMenuItem(DisplaySubMenuItem):

    title = _(u'label_choose_template', default=u'Display')


class gwFactoriesSubMenuItem(FactoriesSubMenuItem):

    title = _(u'label_add_new_item', default=u'Add new\u2026')
