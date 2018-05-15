tinyMCEPopup.requireLangPack();

var TemplateDialog = {
    preInit : function() {
       
    },

    init : function() {
        var editor = tinyMCEPopup.editor;
        var popup = document.forms[0];
        var popupcontent = window.frames['templatesrc'].document;

        var body = editor.getBody();
        var items = body.getElementsByClassName('item');
        console.log(items);
        
        // desplegable
        var sel = document.getElementById('tpath');

        // busquem el carousel selecionat en l'editor
        e = editor.selection.getNode();
        carousel = tinyMCE.DOM.getParent(e, function(p){ if (tinyMCE.DOM.hasClass(p,'carousel')) return p; }, body);
        items = tinyMCE.DOM.select('.item',carousel);

        for (var x=1; x<items.length+1; x++) {
            sel.options[sel.options.length] = new Option('slide ' + x);
        }
        
        popupcontent.body.innerHTML = items[0].outerHTML;
        //document.getElementById('mceTemplatePreview').innerHTML = items[0].outerHTML;


        this.templateHTML = carousel.outerHTML;
    },

    loadCSSFiles : function(d) {
        var ed = tinyMCEPopup.editor;

        tinymce.each(ed.getParam("content_css", '').split(','), function(u) {
            d.write('<link href="' + ed.documentBaseURI.toAbsolute(u) + '" rel="stylesheet" type="text/css" />');
        });
    },

    selectTemplate : function(u, ti) {
        var d = window.frames['templatesrc'].document, x, tsrc = this.tsrc;

        if (!u)
            return;

        d.body.innerHTML = this.templateHTML = this.getFileContents(u);

        for (x=0; x<tsrc.length; x++) {
            if (tsrc[x].title == ti)
                document.getElementById('tmpldesc').innerHTML = tsrc[x].description || '';
        }
    },

    insert : function() {
        tinyMCEPopup.execCommand('mcePloneInsertTemplate', false, {
            content : this.templateHTML,
            selection : tinyMCEPopup.editor.selection.getContent()
        });

        tinyMCEPopup.close();
    },

};

TemplateDialog.preInit();
tinyMCEPopup.onInit.add(TemplateDialog.init, TemplateDialog);