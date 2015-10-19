'use strict';

angular.module('maincouranteApp', [
    'ui.bootstrap',
    'ngRoute',
    'ngResource',
    'focusOn',
    'edir.maincourante.controllers',
    'edir.maincourante.entities'
])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '/static/view/main.html',
                controller: 'MainCtrl',
                controllerAs: 'main'
            })
            .otherwise({
                redirectTo: '/'
            });
    });

angular.module('maincouranteApp').config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});
