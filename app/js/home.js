// IIFE
(function(init) {

// The global jQuery object is passed as a parameter
    init(window.jQuery, window, document);

}(function($, window, document) {

    // The $ is now locally scoped 

    // Listen for the jQuery ready event on the document
    $(function() {
        // The DOM is ready!
        $('#open-menu').on('click', function() {
            $('#nav-menu').toggle(250);
        });

        $('.teams').on('click', function(e) {
            $('.teamlist').toggle();

        });
    });

// DOM isn't ready, but code can still go here

}));