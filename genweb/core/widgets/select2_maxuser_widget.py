from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import textarea

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from genweb.core.widgets.interfaces import IAjaxSelectWidget

import zope.component
import zope.interface
import zope.schema


class Select2MAXUserInputWidget(textarea.TextAreaWidget):
    """Widget for select site users"""
    zope.interface.implementsOnly(IAjaxSelectWidget)
    klass = u'user-token-input-widget'
    display_template = ViewPageTemplateFile('templates/select2_maxuser_display.pt')
    input_template = ViewPageTemplateFile('templates/select2_maxuser_input.pt')

    # JavaScript template
    js_template = u"""\
    (function($) {
        $().ready(function() {
            $('#'+'%(id)s').select2({
                tags: [],
                tokenSeparators: [","],
                minimumInputLength: 3,
                ajax: {
                    url: portal_url + '/max.ajaxusersearch',
                    quietMillis: 700,
                    data: function (term, page) {
                        return {
                            q: term,
                            page: page, // page number
                        };
                    },
                    results: function (data, page) {
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
def Select2MAXUserInputFieldWidget(field, request):
    """IFieldWidget factory for Select2MAXUserInputWidget."""
    return widget.FieldWidget(field, Select2MAXUserInputWidget(request))
