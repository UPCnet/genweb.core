/**
 * --------------------------------------------------------------------
 * jQuery customfileinput plugin
 * Author: Scott Jehl, scott@filamentgroup.com
 * Copyright (c) 2009 Filament Group
 * licensed under MIT (filamentgroup.com/examples/mit-license.txt)
 * --------------------------------------------------------------------
 */

$.fn.customFileInput = function(){
	var i18n_strings = {
		ca: {
				canvia: 'Canvia...',
				navegar: 'Navega...',
				fitxer_no_seleccionat: 'Cap fitxer seleccionat...'
			},
		en: {
				canvia: 'Change...',
				navegar: 'Browse...',
				fitxer_no_seleccionat: 'No file selected...'
			},
		es: {
				canvia: 'Cambiar...',
				navegar: 'Navegar...',
				fitxer_no_seleccionat: 'Ningún archivo seleccionado...'
		}
	};
	var gwtranslate = function(i18n_id) {
		var lang = $('html').attr('lang');
		var translation = i18n_strings[lang][i18n_id];
		if (translation === undefined) {
			return i18n_strings['en'][i18n_id];
		} else {
			return translation;
		}
	};
	//apply events and styles for file input element
	var fileInput = $(this)
		.addClass('customfile-input') //add class for CSS
		.mouseover(function(){ upload.addClass('customfile-hover'); })
		.mouseout(function(){ upload.removeClass('customfile-hover'); })
		.focus(function(){
			upload.addClass('customfile-focus');
			fileInput.data('val', fileInput.val());
		})
		.blur(function(){
			upload.removeClass('customfile-focus');
			$(this).trigger('checkChange');
		})
		.bind('disable',function(){
			fileInput.attr('disabled',true);
			upload.addClass('customfile-disabled');
		})
		.bind('enable',function(){
			fileInput.removeAttr('disabled');
			upload.removeClass('customfile-disabled');
		})
		.bind('checkChange', function(){
			if(fileInput.val() && fileInput.val() != fileInput.data('val')){
				fileInput.trigger('change');
			}
		})
		.bind('change',function(){
			//get file name
			var fileName = $(this).val().split(/\\/).pop();
			//get file extension
			var fileExt = 'customfile-ext-' + fileName.split('.').pop().toLowerCase();
			//update the feedback
			uploadFeedback
				.text(fileName) //set feedback text to filename
				.removeClass(uploadFeedback.data('fileExt') || '') //remove any existing file extension class
				.addClass(fileExt) //add file extension class
				.data('fileExt', fileExt) //store file extension for class removal on next change
				.addClass('customfile-feedback-populated'); //add class to show populated state
			//change text of button
			uploadButton.text(gwtranslate('canvia'));
		})
		.click(function(){ //for IE and Opera, make sure change fires after choosing a file, using an async callback
			fileInput.data('val', fileInput.val());
			setTimeout(function(){
				fileInput.trigger('checkChange');
			},100);
		});

	//create custom control container
	var upload = $('<div class="customfile well well-small"></div>');
	//create custom control button
	var uploadButton = $('<span class="customfile-button btn pull-right" aria-hidden="true"><i class="icon-upload"></i>'+gwtranslate("navegar")+'</span>').appendTo(upload);
	//create custom control feedback
	var uploadFeedback = $('<span class="customfile-feedback" aria-hidden="true">'+gwtranslate("fitxer_no_seleccionat")+'</span>').appendTo(upload);

	//match disabled state
	if(fileInput.is('[disabled]')){
		fileInput.trigger('disable');
	}


	//on mousemove, keep file input under the cursor to steal click
	upload

		.mousemove(function(e){
			fileInput.css({
				/*
				'left': e.pageX - upload.offset().left - fileInput.outerWidth() + 130, //position right side 20px right of cursor X)
				'top': e.pageY - upload.offset().top - $(window).scrollTop() + 360
				*/
				'left': e.pageX - upload.offset().left - fileInput.outerWidth() + 20, //position right side 20px right of cursor X)
				'top': fileInput.outerHeight() - 45
			});
		})

		.insertAfter(fileInput); //insert after the input

	fileInput.appendTo(upload);

	//return jQuery
	return $(this);
};
