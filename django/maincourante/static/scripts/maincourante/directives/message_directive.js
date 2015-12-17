angular.module("edir.maincourante.directives", []);
angular.module('edir.maincourante.directives').directive('messages', function(){
    return {
        controller : 'MessageDirectiveCtrl',
        templateUrl : '/static/scripts/maincourante/directives/message.html'
    }
});


angular.module('edir.maincourante.controllers').controller('MessageDirectiveCtrl', function ($scope) {

});