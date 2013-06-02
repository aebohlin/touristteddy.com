'use strict';

var touristteddyApp = angular.module('touristteddyApp', [])
    .config(function ($interpolateProvider) {
        // To prevent the conflict of `{{` and `}}` symbols
        // between django templating and angular templating we need
        // to use different symbols for angular.
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    });


touristteddyApp.directive('openFancybox', function() {
    return function(scope, element, attrs) {
        $(element).click(function(event) {
            event.preventDefault();
            $(attrs.href).lightbox_me();
            //    $('#try-1').click(function(e) {
            //        $('#sign_up').lightbox_me({
            //            centered: true,
            //            onLoad: function () {
            //                $('#sign_up').find('input:first').focus()
            //            }
            //        });
            //        e.preventDefault();
            //    });
        });
    };
});