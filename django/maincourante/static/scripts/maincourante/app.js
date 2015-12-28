'use strict';

angular.module('maincouranteApp', [
    'ui.bootstrap',
    'ngRoute',
    'ngResource',
    'ngAnimate',
    'focusOn',
    'angucomplete-alt',
    'edir.maincourante.controllers',
    'edir.maincourante.entities',
    'edir.maincourante.directives'
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
