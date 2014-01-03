from five import grok
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.component import adapts
from zope.component.hooks import getSite
from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import textarea
from z3c.form.browser.widget import HTMLInputWidget
from z3c.form.converter import BaseDataConverter
from zope.schema.interfaces import IList

from Products.CMFCore.utils import getToolByName

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from genweb.core.interfaces import IGenwebLayer
from genweb.core.widgets.interfaces import IAjaxSelectWidget

import json
import zope.component
import zope.interface
import zope.schema


class Select2UserInputWidget(textarea.TextAreaWidget):
    """Widget for select site users"""
    zope.interface.implementsOnly(IAjaxSelectWidget)
    klass = u"user-token-input-widget"
    display_template = ViewPageTemplateFile('select2_user_display.pt')
    input_template = ViewPageTemplateFile('select2_user_input.pt')

    # JavaScript template
    js_template = u"""\
    (function($) {
        $().ready(function() {
            $('#'+'%(id)s').select2({
                tags: [],
                minimumInputLength: 3,
                ajax: {
                    url: portal_url + '/genweb.ajaxusersearch',
                    data: function (term, page) {
                        return {
                            q: term,
                            page: page, // page number
                        };
                    },
                    results: function (data, page) {
                        console.log(data);
                        return data;
                    },
                },
                initSelection: function(element, callback) {
                    var id=$(element).val();
                    $.ajax(portal_url + '/genweb.fromusername2displayname', {
                        data: {
                            q: id,
                        },
                    }).done(function(data) { callback(data); });
                },
            });
        });
    })(jQuery);
    """

    def js(self):
        return self.js_template % dict(id=self.id)

    def render(self):
        if self.mode == interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)


@zope.interface.implementer(interfaces.IFieldWidget)
def Select2UserInputFieldWidget(field, request):
    """IFieldWidget factory for Select2UserInputWidget."""
    return widget.FieldWidget(field, Select2UserInputWidget(request))


class SelectWidgetConverter(BaseDataConverter):
    """Data converter for ICollection."""

    adapts(IList, IAjaxSelectWidget)

    def toWidgetValue(self, value):
        """Converts from field value to widget.

        :param value: Field value.
        :type value: list |tuple | set

        :returns: Items separated using separator defined on widget
        :rtype: string
        """
        if not value:
            return self.field.missing_value
        separator = getattr(self.widget, 'separator', ',')
        return separator.join(unicode(v) for v in value)

    def toFieldValue(self, value):
        """Converts from widget value to field.

        :param value: Value inserted by AjaxSelect widget.
        :type value: string

        :returns: List of items
        :rtype: list | tuple | set
        """
        if not value:
            return self.field.missing_value
        separator = getattr(self.widget, 'separator', ',')
        return [v for v in value.split(separator)]


class fromUsername2DisplayName(grok.View):
    grok.context(Interface)
    grok.name('genweb.fromusername2displayname')
    grok.require('genweb.authenticated')
    grok.layer(IGenwebLayer)

    def render(self):
        self.request.response.setHeader("Content-type", "application/json")
        query = self.request.form.get('q', '')

        if query:
            portal = getSite()
            pm = getToolByName(portal, 'portal_membership')

            usernames = [username for username in query.split(',')]
            to_fullnames = []
            for username in usernames:
                if pm.getMemberInfo(username):
                    to_fullnames.append(
                        dict(id=username,
                             text=u'{} ({})'.format(pm.getMemberInfo(username).get('fullname', username).decode('utf-8'), username.decode('utf-8')))
                    )
                else:
                    to_fullnames.append(
                        dict(id=username,
                             text=username)
                    )
            return json.dumps(to_fullnames)
        else:
            return json.dumps({"error": "No query found"})
