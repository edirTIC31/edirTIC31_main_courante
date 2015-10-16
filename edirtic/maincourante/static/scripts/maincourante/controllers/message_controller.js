'use strict';

angular.module("edir.maincourante.controllers", []);

angular.module('edir.maincourante.controllers')
  .controller('MainCtrl', ['$scope', 'Message', 'MessageManager', prepareMainController]);

function prepareMainController($scope, Message, MessageManager){
	
	$scope.messages = []

    $scope.addMessage = function(){
        var message = new Message();
        message.expediteur = $scope.from;
        message.recipiendaire = $scope.to;
		message.corps = $scope.body;
		message.cree = new Date();
		MessageManager.add(message).then(
            function(message) {
                $scope.messages.push(message);
            },
            function(errorPayload) {
                alert(errorPayload);
            });
	}

	$scope.deleteMessage = function(index,message){
		MessageManager.delete(index,message).then(
            function(message) {
                delete $scope.messages[index];
                $scope.messages.splice(index, 1);
            },
            function(errorPayload) {
                alert(errorPayload);
            });
	}

    MessageManager.load().then(
        function(messages) {
            angular.forEach(messages, function(value, key) {
                value.cree = new Date(value.cree);
                $scope.messages.push(value)
            });

        },
        function(errorPayload) {
            alert(errorPayload);
        }
    );

}
