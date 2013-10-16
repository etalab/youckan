/**
 * Avatar management
 */
(function($){

    "use strict";

    // var on_avatar_file_change = function() {

    // };
    //
    //

        // /**
        //  * Trigger image browse and prepare form data.
        //  */
        // _on_view_upload: function(e) {
        //     var $form = $(e.currentTarget).closest('form'),
        //         $popup = $('#upload-modal'),
        //         $input = $('#source-input'),
        //         formdata = new FormData(),
        //         thumbnailUrl = $form.find('#download-button').attr('href');

        //     formdata.append('_source','');
        //     formdata.append('view_id', $form.find('[name="view_id"]').val());

        //     $popup.find('.modal-footer button').show();
        //     $popup.find('.progress').hide();
        //     $popup.find('#old-thumbnail').attr('src', thumbnailUrl);
        //     $popup
        //         .data('formdata', formdata)
        //         .data('formaction', $form.attr('action'));

        //     $input.click();
        // },

    // /**
    //  * Display confirm popup
    //  */
    // on_sourceinput_change: function(e) {
    //     var $input = $(e.currentTarget),
    //         $popup = $('#upload-modal'),
    //         file = $input[0].files[0],
    //         formdata = $('#upload-modal').data('formdata'),
    //         reader = new FileReader();

    //     $popup.appendTo("body").modal('show');

    //     reader.onload = function(e) {
    //         $popup.find('#new-thumbnail').attr('src',this.result);
    //     };
    //     reader.readAsDataURL(file);

    //     formdata.append('source', file);
    // },

    // /**
    //  * Upload source image using AJAX on confirm.
    //  */
    // on_confirm_upload: function(e) {
    //     var $popup = $('#upload-modal'),
    //         formdata = $popup.data('formdata'),
    //         formaction = $popup.data('formaction');

    //     $popup.find('.progress').show();
    //     $popup.find('.modal-footer button').hide();

    //     $.ajax({
    //         url: formaction,
    //         type: 'POST',
    //         xhr: function() {
    //             var XHR = $.ajaxSettings.xhr();
    //             if(XHR.upload){
    //                 $(XHR.upload).on('progress', ControlView._on_upload_progress);
    //             }
    //             return XHR;
    //         },
    //         data: formdata,
    //         cache: false,
    //         contentType: false,
    //         processData: false,
    //         success: function(data, textStatus, jqXHR) {
    //             $popup.modal('hide');
    //             Minidoor.success('Image source envoyée.');
    //         },
    //         error: function(jqXHR, textStatus, errorThrown) {
    //             $popup.modal('hide');
    //             var errorMsg = jqXHR.status === 415 ? jqXHR.responseText : jqXHR.status +' - '+errorThrown;
    //             Minidoor.error(errorMsg);
    //         }
    //     });
    // },

    // _on_upload_progress: function(e) {
    //     var evt = e.originalEvent, progress, percent;
    //     if (evt.lengthComputable) {
    //         progress = (evt.loaded / evt.total);
    //         if (progress <= 1) {
    //             percent = (progress * 100).toFixed(2) + '%';
    //             $('#upload-modal').find('.bar').width(percent).html(percent);
    //         }
    //     }
    // },
    //

    var displaySource = function(e) {
        var $input = $(e.currentTarget),
            $popup = $input.closest('.modal'),
            file = $input[0].files[0],
            reader = new FileReader();

        reader.onload = function(e) {
            var $container = $popup.find('.crop-container'),
                image = new Image();

            image.src = this.result;
            $container.empty().append(image);

            $(image).Jcrop({
                onChange: updatePreview,
                onSelect: updatePreview,
                boxWidth: $container.width(),
                aspectRatio: 1
            });
        };
        reader.readAsDataURL(file);

    };

    var updatePreview = function(crop) {
        if (crop.h === 0 || crop.w === 0) {
            return;
        }

        var $container = $('.preview-container'),
            $preview = $('.preview-container img'),
            $original = $('.crop-container img'),
            image = new Image(),
            size = $container.data('size'),
            ratio = size / crop.w;

        image.src = $original.attr('src');

        $preview.attr('src', image.src)
            .removeAttr('width').removeAttr('height');

        $preview.css({
            position: 'absolute',
            width: Math.round(ratio * image.width) + 'px',
            height: Math.round(ratio * image.height) + 'px',
            marginLeft: '-' + Math.round(ratio * crop.x) + 'px',
            marginTop: '-' + Math.round(ratio * crop.y) + 'px'
        });
    };

    $(function() {
        var $container = $('.preview-container'),
            size = $container.data('size');

        $container.css({
            width: size + 'px',
            height: size + 'px',
            position: 'relative',
            overflow: 'hidden'
        });

        $('#change-avatar-modal input[type="file"]').change(displaySource);
    });

}(window.jQuery));



