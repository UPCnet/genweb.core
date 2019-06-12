tinyMCEPopup.requireLangPack();

var TemplateDialog = {
    preInit : function() {

        // Use this parameter to load another JavaScript file with template
        // definitions. By default, we load our own list using the semantics
        // described in the README.
        var url = tinyMCEPopup.getParam("template_external_list_url");

        if (url != null)
            document.write('<script language="javascript" type="text/javascript" src="' + tinyMCEPopup.editor.documentBaseURI.toAbsolute(url) + '"></script>');
    },

    init : function() {
        var ed = tinyMCEPopup.editor, tsrc, sel, x, u;


        // Load templates from an explicit parameter. By default, we don't
        // use this
        tsrc = ed.getParam("template_templates", false);
        sel = document.getElementById('tpath');

        // Use external template list as a fallback
        if (!tsrc && typeof(tinyMCETemplateList) != 'undefined') {
            for (x=0, tsrc = []; x<tinyMCETemplateList.length; x++)
                tsrc.push({id : tinyMCETemplateList[x][0], title : tinyMCETemplateList[x][1], src : tinyMCETemplateList[x][2], description : tinyMCETemplateList[x][3]});
        }

        for (x=0; x<tsrc.length; x++)
            sel.options[sel.options.length] = new Option(tsrc[x].title, tsrc[x].id);

        this.resize();
        this.tsrc = tsrc;
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

    loadCSSFiles : function(d) {
        var ed = tinyMCEPopup.editor;
        tinymce.each(ed.getParam("content_css", '').split(','), function(u) {
            d.write('<link href="' + ed.documentBaseURI.toAbsolute(u) + '" rel="stylesheet" type="text/css" />');
        });
    },

    selectTemplate : function(u, ti) {
        value = document.getElementById("tpath").value;
        if(value.length > 0){
            document.getElementById("templateOptions").style.display = 'block';
            document.getElementById("conf").innerHTML = '';

            if (value.includes('carousel')) {
                document.getElementById("templateOptionsCarousel").style.display = 'block';
            } else {
                document.getElementById("templateOptionsCarousel").style.display = 'none';
            }

            document.getElementById('add_item_before').addEventListener('click', this.addNewItemBefore, false);
            document.getElementById('add_item_after').addEventListener('click', this.addNewItemAfter, false);

            var d = window.frames['templatesrc'].document, x, tsrc = this.tsrc;

            if (!u)
                return;

            for (x=0; x<tsrc.length; x++) {
                if (tsrc[x].title == ti)
                    document.getElementById('tmpldesc').innerHTML = tsrc[x].description || '';

                if (tsrc[x].id == u)
                    d.body.innerHTML = this.templateHTML = this.getFileContents(tsrc[x].src);
            }
        }else{
            document.getElementById("templateOptions").style.display = 'none';
            document.getElementById("conf").innerHTML = '';
            document.getElementById('tmpldesc').innerHTML = '';
            window.frames['templatesrc'].document.body.innerHTML = '';
        }
    },

    addNewItemBefore : function() {
        document.getElementById('conf').insertAdjacentHTML('afterbegin', addItem());
    },

    addNewItemAfter : function() {
        document.getElementById('conf').insertAdjacentHTML('beforeend', addItem());
    },

    insert : function() {
        tinyMCEPopup.execCommand('mcePloneInsertTemplate', false, {
            content : this.getContentTemplate(),
            selection : tinyMCEPopup.editor.selection.getContent()
        });

        tinyMCEPopup.close();
    },

    getContentTemplate : function() {
        switch (document.getElementById("tpath").value) {
            case 'carousel-dimatges':
                return this.getCarouselHTML();
                break;

            case 'acordio':
                return this.getAcordioHTML();
                break;

            case 'pestanyes':
                return this.getPestanyesHTML();
                break;

            case 'pestanyes-caixa':
                return this.getPestanyesCaixaHTML();
                break;

            default:
                return '';
        }
    },

    getCarouselHTML : function() {
        var template = '';
        var seconds = document.getElementById("seconds").value * 1000;
        var random = Math.floor((Math.random() * 1000000)) + 1;

        /* JS */
        if (document.getElementById("autojs").checked) {
            template += '<script type="text/javascript">';
            template +=     '$(document).ready(function(event) {';
            template +=         '$(".carousel").carousel({';
            template +=             'interval: $("#myCarousel' + random + '").attr("data-interval"),';
            template +=             'ride: true';
            template +=         '});';
            template +=     '});';
            template += '</script>';
        }

        /* INICIO */
        template += '<div id="myCarousel' + random + '" class="carousel slide" data-interval="' + seconds + '">';
        template +=     '<div class="carousel-inner">';

        /* CONTENIDO */
        var slides = window.document.getElementsByClassName('slide');
        for (var x=0; x<slides.length; x++) {
            title = slides[x].getElementsByClassName('title')[0].value;
            description = slides[x].getElementsByClassName('description')[0].value;
            image = slides[x].getElementsByClassName('image')[0].value;

            if (x == 0) {
                template += '<div class="active item">';
            } else {
                template += '<div class="item">';
            }
            template +=         '<img src="' + image + '" alt="' + title + '">';
            template +=         '<div class="carousel-caption">';
            template +=             '<h4>' + title + '</h4>';
            template +=             '<p>' + description + '</p>';
            template +=         '</div>';
            template +=     '</div>';
        }

        /* FIN */
        template +=     '</div>';
        template +=     '<a class="carousel-control left" href="#myCarousel" data-slide="prev">&lsaquo;</a>';
        template +=     '<a class="carousel-control right" href="#myCarousel" data-slide="next">&rsaquo;</a>';
        template += '</div>';
        template += '<p></p>';

        return template;
    },

    getAcordioHTML : function() {
        var template = '';
        var random = Math.floor((Math.random() * 1000000)) + 1;

        /* INICIO */
        template += '<div class="accordion" id="accordion' + random + '">';

        /* CONTENIDO */
        var slides = window.document.getElementsByClassName('slide');
        for (var x=0; x<slides.length; x++) {
            title = slides[x].getElementsByClassName('title')[0].value;
            description = slides[x].getElementsByClassName('description')[0].value;

            template += '<div class="accordion-group">';
            template +=     '<div class="accordion-heading">';
            if (x == 0) {
                template +=     '<a class="accordion-toggle collapsed" href="#collapse' + x + '' + random + '" data-toggle="collapse" data-parent="#accordion' + random + '">' + title + '</a>';
            } else {
                template +=     '<a class="accordion-toggle" href="#collapse' + x + '' + random + '" data-toggle="collapse" data-parent="#accordion' + random + '">' + title + '</a>';
            }
            template +=     '</div>';
            template +=     '<div class="accordion-body collapse" id="collapse' + x + '' + random + '">';
            template +=         '<div class="accordion-inner">' + description + '</div>';
            template +=     '</div>';
            template += '</div>';
        }

        /* FIN */
        template += '</div>';
        template += '<p></p>';

        return template;
    },

    getPestanyesHTML : function() {
        var template = '';
        var random = Math.floor((Math.random() * 1000000)) + 1;

        /* INICIO */
        template += '<ul class="nav nav-tabs" id="myTab">';

        /* CONTENIDO */
        var slides = window.document.getElementsByClassName('slide');
        for (var x=0; x<slides.length; x++) {
            title = slides[x].getElementsByClassName('title')[0].value;

            if (x == 0) {
                template += '<li class="active">';
            } else {
                template += '<li>';
            }
            template +=         '<a href="#tab' + x + '' + random + '" data-toggle="tab">' + title + '</a>';
            template +=     '</li>';
        }

        /* FIN + INICIO */
        template += '</ul>';
        template += '<div class="tab-content">';

        /* CONTENIDO */
        for (var x=0; x<slides.length; x++) {
            description = slides[x].getElementsByClassName('description')[0].value;

            if (x == 0) {
                template += '<div class="tab-pane active" id="tab' + x + '' + random + '">' + description + '</div>';
            } else {
                template += '<div class="tab-pane" id="tab' + x + '' + random + '">' + description + '</div>';
            }
        }

        /* FIN */
        template += '</div>';
        template += '<p></p>';

        return template;
    },

    getPestanyesCaixaHTML : function() {
        var template = '';
        var random = Math.floor((Math.random() * 1000000)) + 1;

        /* INICIO */
        template += '<div class="beautytab">';
        template +=     '<ul id="myTab">';

        /* CONTENIDO */
        var slides = window.document.getElementsByClassName('slide');
        for (var x=0; x<slides.length; x++) {
            title = slides[x].getElementsByClassName('title')[0].value;

            if (x == 0) {
                template += '<li class="formTab firstFormTab active">';
            } else {
                template += '<li class="formTab firstFormTab">';
            }
            template +=         '<a href="#tabBox' + x + '' + random + '" data-toggle="tab">' + title + '</a>';
            template +=     '</li>';
        }

        /* FIN + INICIO */
        template +=     '</ul>';
        template +=     '<div class="tab-content beautytab-content">';

        /* CONTENIDO */
        for (var x=0; x<slides.length; x++) {
            description = slides[x].getElementsByClassName('description')[0].value;

            if (x == 0) {
                template += '<div class="tab-pane active" id="tabBox' + x + '' + random + '">' + description + '</div>';
            } else {
                template += '<div class="tab-pane" id="tabBox' + x + '' + random + '">' + description + '</div>';
            }
        }

        /* FIN */
        template +=     '</div>';
        template += '</div>';
        template += '<p></p>';

        return template;
    },

    getFileContents : function(u) {
        var x, d, t = 'text/plain';

        function g(s) {
            x = 0;

            try {
                x = new ActiveXObject(s);
            } catch (s) {
            }

            return x;
        };

        x = window.ActiveXObject ? g('Msxml2.XMLHTTP') || g('Microsoft.XMLHTTP') : new XMLHttpRequest();

        // Synchronous AJAX load file
        x.overrideMimeType && x.overrideMimeType(t);
        x.open("GET", u, false);
        x.send(null);

        return x.responseText;
    }

};

TemplateDialog.preInit();
tinyMCEPopup.onInit.add(TemplateDialog.init, TemplateDialog);


function addItem() {

    index = window.document.getElementsByClassName('slide').length +1;

    tag =       '<tr class="slide" id="slide-' + index + '">';
    tag = tag + '<td><a class="elimina" href="#" onclick="document.getElementById(\'slide-' + index + '\').remove();return false;">Elimina</a>';
    tag = tag + '<p>Titol:</p><p><input type="text" name="title" class="title" id="title-' + index + '" value=""></input></p>';
    if (document.getElementById("tpath").value.includes('carousel')){
        tag = tag + '<p>Imatge:</p><p><input type="text" name="image" class="image" id="image-' + index + '" value=""></input></p>';
    }
    tag = tag + '<p>Descripció:</p><p><textarea name="description" class="description" id="description-' + index + '" value=""></textarea></p>';
    tag = tag + '</td></tr>';
    return  tag;
}
