'use strict';

var touristteddyApp = angular.module('touristteddyApp', [])
    .config(function ($interpolateProvider) {
        // To prevent the conflict of `{{` and `}}` symbols
        // between django templating and angular templating we need
        // to use different symbols for angular.
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    });