/***
tinyMCE.DOM.doc: TOTA la pàgina
tinyMCEPopup.editor.dom.doc: el contingut de l'editor a sota, NO el del popup
document: tot el contingut del popup, inclosos els botons
***/

tinyMCEPopup.requireLangPack();

var TemplateDialog = {
    init : function() {
        var editor = tinyMCEPopup.editor;
        var body = editor.getBody();

        // busquem el carousel seleccionat en l'editor
        this.carousel = tinyMCE.DOM.getParent(editor.selection.getNode(), function(p){ if (tinyMCE.DOM.hasClass(p,'carousel-inner')) return p; }, body);
        items = tinyMCE.DOM.select('.item', this.carousel);
        var carousel_items = '';
        this.length = items.length;

        for (var x=0; x<this.length; x++) {
            carousel_items = carousel_items + addItem(false, x, items[x]);
        }

        var popup = document.forms[0];
        var popupcontent = window.document.getElementById('templatesrc');
        
        popupcontent.innerHTML = '<table id="carousel-items">' + carousel_items + '</table>';
        document.getElementById('add_item_before').addEventListener('click', this.addNewItemBefore, false);
        document.getElementById('add_item_after').addEventListener('click', this.addNewItemAfter, false);
        
        //this.resize();
    },

    addNewItemBefore : function() {
        tag = addItem(true);
        window.document.getElementById('carousel-items').innerHTML = tag + window.document.getElementById('carousel-items').innerHTML;
    },

    addNewItemAfter : function() {
        tag = addItem(true);
        window.document.getElementById('carousel-items').innerHTML += tag;
    },

    loadCSSFiles : function(d) {
        var ed = tinyMCEPopup.editor;

        tinymce.each(ed.getParam("content_css", '').split(','), function(u) {
            d.write('<link href="' + ed.documentBaseURI.toAbsolute(u) + '" rel="stylesheet" type="text/css" />');
        });
    },

    insert : function() {
        var slides = window.document.getElementsByClassName('slide');
        var nou_carousel = '';
        for (var x=0; x<slides.length; x++) {
            nou_carousel = nou_carousel + this.insertSlide(slides[x], x);
        }
        tinyMCEPopup.execCommand('mcePloneInsertTemplate', false, {
            content : nou_carousel,
            carousel: this.carousel
        });

        tinyMCEPopup.close();
    },

    insertSlide: function(slide, x) {
        tag = '<div class="item' + ((x==0)?' active':'') + '">';
        tag = tag + '<img src="' + slide.getElementsByClassName('imatge')[0].value + '">';
        tag = tag + '<div class="carousel-caption">';
        tag = tag + '<h4>' + slide.getElementsByClassName('titol')[0].value + '</h4>';
        tag = tag + '<p>' + slide.getElementsByClassName('descripcio')[0].value + '</p>';
        tag = tag + '</div></div>';
        return tag;
    },

};

tinyMCEPopup.onInit.add(TemplateDialog.init, TemplateDialog);


function addItem(empty, index=-1, item=null) {
    var titol = '';
    var descripcio = '';
    var imatge = '';

    if (!empty) {
        titol = item.getElementsByTagName('h4')[0].innerHTML;
        descripcio = item.getElementsByTagName('p')[0].innerHTML;
        imatge = item.getElementsByTagName('img')[0].getAttribute('src');
    } else {
        index = window.document.getElementsByClassName('slide').length +1;
    }
    tag =       '<tr class="slide" id="slide-' + index + '">';
    tag = tag + '<td><img src="' + tinyMCEPopup.editor.documentBaseURI.toAbsolute(imatge) + '"></td>';
    tag = tag + '<td><a class="elimina" href="#" onclick="document.getElementById(\'slide-' + index + '\').remove();return false;">Elimina</a>';
    tag = tag + '<p>Titol:</p><p><input class="titol" id="titol-' + index + '" value="' + titol + '"></input></p>';
    tag = tag + '<p>Descripció:</p><p><input class="descripcio" id="descripcio-' + index + '" value="' + descripcio + '"></input></p>';
    tag = tag + '<p>Imatge:</p><p><input class="imatge" id="imatge-' + index + '" value="' + imatge + '"></input></p>';
    tag = tag + '</td></tr>';
    return  tag;
}