/***
tinyMCE.DOM.doc: TOTA la pàgina
tinyMCEPopup.editor.dom.doc: el contingut de l'editor a sota, NO el del popup
document: tot el contingut del popup, inclosos els botons
***/

tinyMCEPopup.requireLangPack();

var TemplateDialog = {
    preInit : function() {
       
    },

    init : function() {
        var editor = tinyMCEPopup.editor;
        var body = editor.getBody();
        // busquem el carousel seleccionat en l'editor
        this.carousel = tinyMCE.DOM.getParent(editor.selection.getNode(), function(p){ if (tinyMCE.DOM.hasClass(p,'carousel-inner')) return p; }, body);
        items = tinyMCE.DOM.select('.item', this.carousel);
        var carousel_items = '';
        this.length = items.length;
        for (var x=0; x<this.length; x++) {
            carousel_items = carousel_items + this.addItem(items[x], x) + '<hr>';
        }
                

        var popup = document.forms[0];
        this.popupcontent = window.frames['templatesrc'].document;
    
        
        this.popupcontent.body.innerHTML = carousel_items;
        //tinyMCE.DOM.bind('add_item', 'click', this.add_item);
        document.getElementById('add_item').addEventListener('click', this.addNewItem, false);
        
        this.resize();
    },

    addItem : function(item, index) {
        tag = '<div class="slide" id="slide-' + index + '">';
        tag = tag + '<a href="#" onclick="document.getElementById(\'slide-' + index + '\').remove();return false;">elimina</a>';
        tag = tag + '<p>Titol:<input class="titol" id="titol-' + index + '" value="' +      item.getElementsByTagName('h4')[0].innerHTML + '"></input></p>';
        tag = tag + '<p>Descripció:<input class="descripcio" id="descripcio-' + index + '" value="' + item.getElementsByTagName('p')[0].innerHTML + '"></input></p>';
        tag = tag + '<p>Imatge:<input class="imatge" id="imatge-' + index + '" value="' +     item.getElementsByTagName('img')[0].getAttribute('src') + '"></input></p>';
        tag = tag + '<p><img style="max-width:200px" src="' +     item.getElementsByTagName('img')[0].getAttribute('src') + '"></p>';
        tag = tag + '</div>';
        return  tag;
    },

    addNewItem : function() {
        tag = '<div class=\"slide\" id=\"slide-' + this.length + '\">';
        tag = tag + '<a href=\"#\" onclick=\"document.getElementById(\'slide-' + this.length + '\').remove();return false;\">elimina</a>';
        tag = tag + '<p>Titol:<input class=\"titol\" id=\"titol-' + this.length + '\" value=\"\"></input></p>';
        tag = tag + '<p>Descripció:<input class=\"descripcio\" id=\"descripcio-' + this.length + '\" value=\"\"></input></p>';
        tag = tag + '<p>Imatge:<input class=\"imatge\" id=\"imatge-' + this.length + '\" value=\"\"></input></p>';
        tag = tag + '<p><img style=\"max-width:200px\" src=\"\"></p>';
        tag = tag + '</div>';
        window.frames['templatesrc'].document.body.innerHTML += tag;
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
        var body = window.frames['templatesrc'].document.getElementsByTagName('body')[0];
        var slides = body.getElementsByClassName('slide');
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

    resize : function() {
        var w, h, e;

        if (!self.innerWidth) {
            w = document.body.clientWidth - 50;
            h = document.body.clientHeight - 160;
        } else {
            w = self.innerWidth - 50;
            h = self.innerHeight - 170;
        }
        
        e = document.getElementById('templatesrc');

        if (e) {
            e.style.height = Math.abs(h - 80) + 'px';
            e.style.width  = Math.abs(w - 100) + 'px';
        }
    },

};

TemplateDialog.preInit();
tinyMCEPopup.onInit.add(TemplateDialog.init, TemplateDialog);