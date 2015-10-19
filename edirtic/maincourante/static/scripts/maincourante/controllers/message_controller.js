'use strict';

angular.module("edir.maincourante.controllers", []);

angular.module('edir.maincourante.controllers')
  .controller('MainCtrl', ['$scope', 'Message', 'MessageManager', '$modal', 'focus', prepareMainController]);

function prepareMainController($scope, Message, MessageManager, $modal, focus){
	
	$scope.messages = [];
    $scope.childrenMessages = [];
    $scope.onMessageDelete = false;

    $scope.addMessage = function(){
        var message = new Message();
        message.expediteur = $scope.from;
        message.recipiendaire = $scope.to;
		message.corps = $scope.body;
		message.cree = new Date();
        if(!message.isValid()){
            return;
        }
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
        message.enableEdition();
        focus("onEdit");
    }

    $scope.validateMessageEditionListener = function(event, message){
        if(event.keyCode == 13){ //ENTER KEY
            $scope.validateMessageEdition(message);
        }else if(event.keyCode == 27){
            $scope.cancelMessageEdition(message);
        }
    }

    $scope.validateMessageEdition = function(message){
        if(message.oldMessage == message.corps){
            $scope.cancelMessageEdition(message);
            return;
        }
        MessageManager.modify(message).then(
            function(message) {
                message.oldMessage.edit = false;
                loadMessages();
            },
            function(errorPayload) {
                alert(errorPayload);
            });
    }

    $scope.cancelMessageEdition = function(message){
        message.cancelEdition();
        focus('onNewMessage');
    }

    $scope.toggleMessageHistory = function(message){
        if(message.history){
            message.history = null;
        }else{
            message.history = $scope.childrenMessages[message.id]
        }
    }

    function loadMessages() {
        MessageManager.load().then(
            function (messages) {
                $scope.messages = [];
                $scope.childrenMessages = [];
                angular.forEach(messages, function (message, key) {
                    if(message.parent) {
                        var parentArray = $scope.childrenMessages[message.parent];
                        if(!parentArray){
                            parentArray = new Array();
                        }
                        parentArray.push(message);
                        $scope.childrenMessages[message.parent] = parentArray;
                    }else{
                        $scope.messages.push(message)
                    }
                });
                focus('onNewMessage');
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
