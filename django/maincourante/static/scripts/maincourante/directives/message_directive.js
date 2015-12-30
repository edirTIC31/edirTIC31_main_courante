angular.module("edir.maincourante.directives", []);
angular.module('edir.maincourante.directives').directive('messages', function(){
    return {
        controller : 'MessageDirectiveCtrl',
        templateUrl : message_directive_template_url
    }
});


angular.module('edir.maincourante.controllers').controller('MessageDirectiveCtrl', function ($scope) {

});
