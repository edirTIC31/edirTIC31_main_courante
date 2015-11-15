'use strict';

angular.module("edir.maincourante.controllers", []);

angular.module('edir.maincourante.controllers')
  .controller('MainCtrl', ['$scope', 'Message', 'MessageManager', 'IndicatifManager', '$modal', '$interval','focus', prepareMainController]);

function prepareMainController($scope, Message, MessageManager, IndicatifManager,  $modal, $interval, focus){
	
	$scope.messages = [];
    $scope.childrenMessages = [];
    $scope.onMessageDelete = false;
    $scope.editionMode = false;
    $scope.indicatifs = new Array();
    $scope.errorMessage = null;

    $scope.addMessage = function(){
        var message = new Message();
        if(!$scope.sender || !$scope.receiver){
            return;
        }
        message.sender = $scope.sender.title ? $scope.sender.title: $scope.sender.originalObject;
        message.receiver = $scope.receiver.title ? $scope.receiver.title: $scope.receiver.originalObject;
        message.evenement = 'marathon-2015';
		message.body = $scope.body;
		if(!message.isValid()){
            return;
        }
		MessageManager.add(message).then(
            function(message) {
                $scope.body = null;
//                $scope.$broadcast('angucomplete-alt:clearInput', 'from');
//                $scope.$broadcast('angucomplete-alt:clearInput', 'to');
                $scope.$broadcast('angucomplete-alt:changeInput', 'ex1');
            },
            function(errorPayload) {
                alert("Erreur lors de l'ajout du nouveau message");
            });
	}

    $scope.enableMessageEdition = function(message){
        $scope.editionMode = true;
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
        if(message.oldMessage == message.body){
            $scope.cancelMessageEdition(message);
            return;
        }
        MessageManager.modify(message).then(
            function(message) {
                message.oldMessage.edit = false;
                $scope.editionMode = false;
                loadMessages();
                focus('onNewMessage');
            },
            function(errorPayload) {
                alert("Erreur lors de l'edition du message");
            });
    }

    $scope.cancelMessageEdition = function(message){
        message.cancelEdition();
        focus('onNewMessage');
        $scope.editionMode = false;
    }

    function loadMessages() {
        if($scope.editionMode){
            return;
        }
        MessageManager.load().then(
            function (messages) {
                $scope.messages = messages;
                $scope.errorMessage = null;
            },
            function (errorPayload) {
                $scope.errorMessage = "Erreur lors du chargement des messages";
            }
        );
    }

    function loadIndicaifs(){
        IndicatifManager.load().then(
            function (indicatifs) {
                $scope.indicatifs = indicatifs;
                $scope.errorMessage = null;
            },
            function (errorPayload) {
                $scope.errorMessage = "Erreur lors du chargement des messages";
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
    loadIndicaifs();
    focus('onNewMessage');
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
            alert("Erreur lors de la suppression du message");
        });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});
