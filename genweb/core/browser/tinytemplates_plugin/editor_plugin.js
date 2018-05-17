/**
 * Plone templates plugin.
 *
 * @author Rob Gietema
 */

(function() {
    var each = tinymce.each;
    
    tinymce.create('tinymce.plugins.PloneTemplatesPlugin', {
        init : function(ed, url) {
            var t = this;
            t.editor = ed;

            // Register css
            tinymce.DOM.loadCSS(url + '/css/content.css');

            // Register commands
            ed.addCommand('mcePloneTemplates', function(ui) {
                ed.windowManager.open({
                    file : url + '/template.htm',
                    width : ed.getParam('template_popup_width', 750),
                    height : ed.getParam('template_popup_height', 600),
                    inline : 1
                }, {
                    plugin_url : url
                });
            });

            // Executa acció del popup
            ed.addCommand('mcePloneInsertTemplate', t._insertTemplate, t);

            // Register buttons: afegeix el botó a la botonera del tiny
            ed.addButton('plonetemplates', {title : 'template.desc', cmd : 'mcePloneTemplates'});
        },

        _insertTemplate : function(ui, v) {
            var ed = this.editor; 
            var h, el; 

            // Elimina els items del carousel
            var items = v['carousel'].getElementsByClassName('item');
            var length = items.length;
            for (var x=length-1; x>=0; x--) {
                items[x].remove();
            }

            // i substitueix pel nou
            v['carousel'].innerHTML = v.content;

            el = ed.dom.create('div', null, h);

            ed.execCommand('mceInsertContent', false, el.innerHTML);
            ed.addVisual();
        },

    });

    // Register plugin
    tinymce.PluginManager.add('plonetemplates', tinymce.plugins.PloneTemplatesPlugin);
})();
