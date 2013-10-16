/**
 * Homepage specific features
 */
(function($){

    "use strict";

    var MIN_WIDTH_FOR_EQUAL_HEIGHT = 767;

    /**
     * Equal for featured panels
     */
    var handle_panel_height = function() {
        if ($(window).width() >= MIN_WIDTH_FOR_EQUAL_HEIGHT) {
            $('.marketing .panel').equalHeights();
        } else {
            $('.marketing .panel').css({ height: 'auto' });
        }
    };


    $(function() {
        // Equal height for marketing panels
        $(window).resize(handle_panel_height);
        handle_panel_height();
    });

}(window.jQuery));
