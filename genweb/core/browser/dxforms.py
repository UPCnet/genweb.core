from plone.dexterity.browser import edit


class EditForm(edit.DefaultEditForm):
    """ This hacks the default edit form for all dexterities and disables right
        column for all of them.
    """

    def update(self):
        super(EditForm, self).update()
        self.request.set('disable_plone.rightcolumn', True)
