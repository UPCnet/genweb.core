

def getToolbars(self, config):
    """ Patch th method for calculate number of toolbar rows from length of
        buttons replacing it with a hardcoded one for our convenience. Also,
        take advantage of the argument reference and add a missing value in
        TinyMCE configuration.
    """

    config['theme_advanced_blockformats'] = "p,div,h2,h3,h4"

    return ["fullscreen,|,code,|,save,newdocument,|,plonetemplates,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,|,cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor",
            "formatselect,style,|,cleanup,removeformat,|,image,media,|,tablecontrols,styleprops,|,visualaid,|,sub,sup,|,charmap",
            "", ""]
