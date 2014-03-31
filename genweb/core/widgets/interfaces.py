from z3c.form import interfaces


class ITokenInputWidget(interfaces.ITextLinesWidget):
    """Text lines widget."""


class IAjaxSelectWidget(interfaces.ITextWidget):
    """Marker interface for the Select2Widget."""


class ITagsSelectWidget(interfaces.ITextWidget):
    """Marker interface for the tags Select2Widget."""
