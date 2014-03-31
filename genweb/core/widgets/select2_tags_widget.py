# -*- coding: utf-8 -*-
from zope.component import adapts
from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import textarea
from z3c.form.converter import BaseDataConverter
from zope.schema.interfaces import ITuple

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import adapter
from zope.interface import implementer
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from plone.app.dexterity.behaviors.metadata import ICategorization

from genweb.core.interfaces import IGenwebLayer
from genweb.core.widgets.interfaces import ITagsSelectWidget

import zope.component
import zope.interface
import zope.schema


class Select2TagsInputWidget(textarea.TextAreaWidget):
    """Widget for select site tags"""
    zope.interface.implementsOnly(ITagsSelectWidget)
    klass = u"tags-token-input-widget"
    display_template = ViewPageTemplateFile('select2_user_display.pt')
    input_template = ViewPageTemplateFile('select2_user_input.pt')

    # JavaScript template
    js_template = u"""\
    (function($) {
        $().ready(function() {
            $('#'+'%(id)s').select2({
                tags: [],
                tokenSeparators: [","],
                minimumInputLength: 1,
                ajax: {
                    url: portal_url + '/getVocabulary?name=plone.app.vocabularies.Keywords&field=subjects',
                    data: function (term, page) {
                        return {
                            query: term,
                            page: page, // page number
                        };
                    },
                    results: function (data, page) {
                        console.log(data);
                        return data;
                    },
                },
                initSelection: function(element, callback) {
                    var data = [];
                    $(element.val().split(",")).each(function () {
                        data.push({id: this, text: this});
                    });
                    callback(data);
                },
                // Allow manually entered text in drop down.
                createSearchChoice:function(term, data) {
                    if ( $(data).filter( function() {
                            return this.text.localeCompare(term)===0;
                        }).length===0) {
                        return {id:term, text:term};
                    }
                }
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


@adapter(getSpecification(ICategorization['subjects']), IGenwebLayer)
@implementer(IFieldWidget)
def SubjectsFieldWidget(field, request):
    return FieldWidget(field, Select2TagsInputWidget(request))


@zope.interface.implementer(interfaces.IFieldWidget)
def Select2TagsInputFieldWidget(field, request):
    """IFieldWidget factory for Select2TagsInputWidget."""
    return widget.FieldWidget(field, Select2TagsInputWidget(request))


class TagsSelectWidgetConverter(BaseDataConverter):
    """Data converter for ICollection."""

    adapts(ITuple, ITagsSelectWidget)

    def toWidgetValue(self, value):
        """Converts from field value to widget.

        :param value: Field value.
        :type value: list |tuple | set

        :returns: Items separated using separator defined on widget
        :rtype: string
        """
        if not value:
            return u''
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
        return tuple([v for v in value.split(separator)])
