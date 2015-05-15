from zope.component.hooks import getSite
from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import textarea

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from genweb.core.widgets.interfaces import ITokenInputWidget

import zope.component
import zope.interface
import zope.schema


class KeywordsTokenInputWidget(textarea.TextAreaWidget):
    """Widget for adding new keywords and autocomplete with the ones in the
    system."""
    zope.interface.implementsOnly(ITokenInputWidget)
    klass = u'token-input-widget'
    display_template = ViewPageTemplateFile('token_input_display.pt')
    input_template = ViewPageTemplateFile('token_input_input.pt')

    # JavaScript template
    js_template = u"""\
    (function($) {
        $().ready(function() {
            var newValues = [%(newtags)s];
            var oldValues = [%(oldtags)s];
            $('#%(id)s').data('klass','%(klass)s');
            keywordTokenInputActivate('%(id)s', newValues, oldValues);
        });
    })(jQuery);
    """

    def js(self):
        values = self.context.portal_catalog.uniqueValuesFor('Subject')
        old_values = self.context.Subject()
        tags = u''
        old_tags = u''
        index = 0
        for index, value in enumerate(values):
            if isinstance(value, str):
                value = value.decode('utf-8')
            tags += u'{id: "%s", name: "%s"}' % (
                value.replace(u"'", u"\\'"), value.replace(u"'", u"\\'"))  # noqa
            if index < len(values) - 1:
                tags += ', '

        # prepopulate
        for index, value in enumerate(old_values):
            if isinstance(value, str):
                value = value.decode('utf-8')
            old_tags += u'{id: "%s", name: "%s"}' % (value.replace(
                u"'", u"\\'"), value.replace(u"'", u"\\'"))  # noqa
            if index < len(old_values) - 1:
                old_tags += ', '
        result = self.js_template % dict(
            id=self.id,
            klass=self.klass,
            newtags=tags,
            oldtags=old_tags
        )
        return result

    def render(self):
        if self.mode == interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)


@zope.interface.implementer(interfaces.IFieldWidget)
def KeywordsTokenInputFieldWidget(field, request):
    """IFieldWidget factory for KeywordsTokenInputWidget."""
    return widget.FieldWidget(field, KeywordsTokenInputWidget(request))


class UsersTokenInputWidget(KeywordsTokenInputWidget):
    """ Site's user list selection tokenized widget """

    def js(self):
        portal = getSite()
        mutable_properties = getToolByName(portal, 'acl_users').mutable_properties
        values = [userinfo.get('login') for userinfo in mutable_properties.enumerateUsers()]
        if getattr(self.context, 'subscribed', False):
            old_values = self.context.subscribed
        else:
            old_values = ()

        tags = u''
        old_tags = u''
        index = 0
        for index, value in enumerate(values):
            if isinstance(value, str):
                value = value.decode('utf-8')
            tags += u'{id: "%s", name: "%s"}' % (
                value.replace(u"'", u"\\'"), value.replace(u"'", u"\\'"))  # noqa
            if index < len(values) - 1:
                tags += ', '

        # prepopulate
        for index, value in enumerate(old_values):
            if isinstance(value, str):
                value = value.decode('utf-8')
            old_tags += u'{id: "%s", name: "%s"}' % (value.replace(
                u"'", u"\\'"), value.replace(u"'", u"\\'"))  # noqa
            if index < len(old_values) - 1:
                old_tags += ', '
        result = self.js_template % dict(
            id=self.id,
            klass=self.klass,
            newtags=tags,
            oldtags=old_tags
        )
        return result


@zope.interface.implementer(interfaces.IFieldWidget)
def UsersTokenInputFieldWidget(field, request):
    """IFieldWidget factory for UsersTokenInputWidget."""
    return widget.FieldWidget(field, UsersTokenInputWidget(request))
