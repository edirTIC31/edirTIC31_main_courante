'use strict';

angular.module("edir.maincourante.controllers", []);

angular.module('edir.maincourante.controllers')
  .controller('MainCtrl', ['$scope', 'Message', 'MessageManager', '$modal', prepareMainController]);

function prepareMainController($scope, Message, MessageManager, $modal){
	
	$scope.messages = []

    $scope.addMessage = function(){
        var message = new Message();
        message.expediteur = $scope.from;
        message.recipiendaire = $scope.to;
		message.corps = $scope.body;
		message.cree = new Date();
		MessageManager.add(message).then(
            function(message) {
                $scope.from = null;
                $scope.to = null;
                $scope.body = null;
                loadMessages();
            },
            function(errorPayload) {
                alert(errorPayload);
            });
	}

    $scope.enableMessageEdition = function(message){
        message.edit = true;
        message.newMessage = message.corps;
    }

    $scope.validateMessageEdition = function(oldMessage){
        if(oldMessage.newMessage == oldMessage.corps){
            $scope.cancelMessageEdition(oldMessage);
            return;
        }
        var newMessage = new Message();
        newMessage.expediteur = oldMessage.expediteur;
        newMessage.recipiendaire = oldMessage.recipiendaire;
        newMessage.corps = oldMessage.newMessage;
        newMessage.cree = new Date();
        newMessage.parent = oldMessage.id;
        newMessage.parent_id = oldMessage.id;
        MessageManager.add(newMessage, oldMessage).then(
            function(message) {
                message.oldMessage.edit = false;
                loadMessages();
            },
            function(errorPayload) {
                alert(errorPayload);
            });
    }

    $scope.cancelMessageEdition = function(message){
        message.newMessage = null;
        message.edit = false;
    }

    function loadMessages() {
        MessageManager.load().then(
            function (messages) {
                $scope.messages = [];
                angular.forEach(messages, function (value, key) {
                    value.cree = new Date(value.cree);
                    value.edit = false;
                    $scope.messages.push(value)
                });

            },
            function (errorPayload) {
                alert(errorPayload);
            }
        );
    }

    $scope.deleteMessage = function(message) {

        var modalInstance = $modal.open({
            animation: $scope.animationsEnabled,
            templateUrl: 'myModalContent.html',
            controller: 'ModalInstanceCtrl',
            resolve: {
                message: function () {
                    return message;
                }
            }
        });

        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.toggleAnimation = function () {
        $scope.animationsEnabled = !$scope.animationsEnabled;
    };
    loadMessages();
}

// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $uibModal service used above.

angular.module('edir.maincourante.controllers').controller('ModalInstanceCtrl', function ($scope, $modalInstance, MessageManager, message) {
    $scope.ok = function () {
        MessageManager.delete(message, $scope.suppressionMessage).then(
         function(message) {
             $modalInstance.close();
         },
         function(errorPayload) {
            alert("error");
        });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});
