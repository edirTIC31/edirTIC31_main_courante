'use strict';

angular.module("edir.maincourante.controllers", []);

angular.module('edir.maincourante.controllers')
  .controller('MainCtrl', ['$scope', 'Message', 'MessageManager', '$modal', '$interval','focus', prepareMainController]);

function prepareMainController($scope, Message, MessageManager, $modal, $interval, focus){
	
	$scope.messages = [];
    $scope.childrenMessages = [];
    $scope.onMessageDelete = false;
    $scope.editionMode = false;
    $scope.openHistory = new Array();
    $scope.indicatifs = new Array();

    $scope.addMessage = function(){
        var message = new Message();
        if(!$scope.from || !$scope.to){
            return;
        }
        message.expediteur = $scope.from.title ? $scope.from.title: $scope.from.originalObject;
        message.recipiendaire = $scope.to.title ? $scope.to.title: $scope.to.originalObject;
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
                $scope.$broadcast('angucomplete-alt:clearInput', 'from');
                $scope.$broadcast('angucomplete-alt:clearInput', 'to');
                loadMessages();
                focus('onNewMessage');
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
        if(message.oldMessage == message.corps){
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

    $scope.toggleMessageHistory = function(message){
        if(message.showHistory){
            var idx = $scope.openHistory.indexOf(message.id);
            if(idx != -1) {
                $scope.openHistory.splice(idx, 1);
            }
            message.showHistory = false;
        }else{
            $scope.openHistory.push(message.id);
            message.showHistory = true;
        }
    }

    function loadMessages() {
        if($scope.editionMode){
            return;
        }
        MessageManager.load().then(
            function (messages) {
                $scope.messages = messages;
                manageOpenHistoryMessage();
                manageIndicatifs();
            },
            function (errorPayload) {
                alert("Erreur lors du chargement des messages");
            }
        );
    }

    function manageOpenHistoryMessage(){
        angular.forEach($scope.openHistory, function (messageID, key) {
            angular.forEach($scope.messages, function (message, key) {
                if(messageID == message.id){
                    message.showHistory = true;
                }
            });
        });
    }

    function manageIndicatifs(){
        $scope.indicatifs = [];
        angular.forEach($scope.messages, function (message, key) {
            addIndicatifs(message.expediteur);
            addIndicatifs(message.recipiendaire);
        });
    }

    function addIndicatifs(indicatif){
       var found = false;
        angular.forEach($scope.indicatifs, function (indic, key) {
            if(indic.name == indicatif){
                found = true;
            }
        });
        if(!found) {
            $scope.indicatifs.push({"name": indicatif});
        }
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
    focus('onNewMessage');
    $interval(loadMessages, 10000);
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
