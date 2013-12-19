/**
 * Register done specific features
 */
(function($, Config) {

    "use strict";


    $(function() {
        // Equal height for marketing panels
        $('#org-search')
            .typeahead(Config.typeahead.organizations)
            .on('typeahead:selected typeahead:autocompleted', function(e, data, dataset) {
                window.location = Config.urls.organization(data.name);
            })
            .siblings('input.tt-hint').addClass('hint-large');;
    });

}(window.jQuery, window.EtalabConfig));
