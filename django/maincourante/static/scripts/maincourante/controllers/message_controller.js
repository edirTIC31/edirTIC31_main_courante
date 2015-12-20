angular.module("edir.maincourante.controllers", []);

angular.module('edir.maincourante.controllers')
  .controller('MainCtrl', ['$scope', 'Message', 'MessageManager', 'IndicatifManager', '$modal', '$interval','focus', prepareMainController]);

function prepareMainController($scope, Message, MessageManager, IndicatifManager,  $modal, $interval, focus){
	
	$scope.messages = [];
    $scope.isLoading = true;
    $scope.editionMode = false;
    $scope.disableAutoLoad = false;
    $scope.indicatifs = new Array();
    $scope.errorMessage = null;

    $scope.addMessage = function(){
        var message = new Message();
        if(!$scope.sender || !$scope.receiver){
            return;
        }
        message.sender = $scope.sender.title ? $scope.sender.title: $scope.sender.originalObject;
        message.receiver = $scope.receiver.title ? $scope.receiver.title: $scope.receiver.originalObject;
        message.evenement = EVENEMENT;
		message.body = $scope.body;
		if(!message.isValid()){
            return;
        }
		MessageManager.add(message).then(
            function(msg) {
                if($scope.response){
                    var response = new Message();
                    response.receiver = msg.sender;
                    response.sender = msg.receiver;
                    response.evenement = EVENEMENT;
                    response.body = $scope.response;
                    MessageManager.add(response).then(
                        function(resp) {
                        $scope.body = null;
                        $scope.response = null;
                        $scope.messages.push(resp);
                    },
                    function(errorPayload) {
                        alert("Erreur lors de l'ajout de la reponse");
                    });
                }
                $scope.messages.push(msg);
                $scope.sender = null;
                $scope.receiver = null;
                $scope.body = null;
                $scope.$broadcast('angucomplete-alt:clearInput', 'sender');
                $scope.$broadcast('angucomplete-alt:clearInput', 'receiver');
                focus('onNewMessage');
            },
            function(errorPayload) {
                alert("Erreur lors de l'ajout du nouveau message");
            });
	}

    $scope.enableMessageEdition = function(message){
        $scope.disableAutoLoad = true;
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
                message.disableAutoLoad = false;
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
        message.disableAutoLoad = false;
    }

    function loadMessages() {
        if(!$scope.disableAutoLoad) {
            MessageManager.load().then(
                function (messages) {
                    $scope.messages = messages;
                    $scope.errorMessage = null;
                    $scope.isLoading = false;
                },
                function (errorPayload) {
                    $scope.errorMessage = "Erreur lors du chargement des messages";
                }
            );
        }
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
            templateUrl: 'modal-delete-message.html',
            controller: 'ModalDeleteMessageCtrl',
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

    $scope.replyMessage = function(message) {
        var modalInstance = $modal.open({
            animation: $scope.animationsEnabled,
            templateUrl: 'modal-reply-message.html',
            controller: 'ModalReplyMessageCtrl',
            resolve: {
                message: function () {
                    return message;
                },
                messages: function () {
                    return $scope.messages;
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

    $interval(loadMessages, 120000);
    $interval(loadIndicaifs, 120000);
}

// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $uibModal service used above.

angular.module('edir.maincourante.controllers').controller('ModalDeleteMessageCtrl', function ($scope, $modalInstance, MessageManager, message) {

    $scope.ok = function () {
        MessageManager.delete(message, $scope.suppressionMessage).then(
         function(message) {
             message.deleted = true;
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

angular.module('edir.maincourante.controllers').controller('ModalReplyMessageCtrl', function ($scope, $modalInstance, MessageManager, Message, message, messages) {
    $scope.message = message;
    $scope.ok = function () {
        var response = new Message();
        response.receiver = message.sender;
        response.sender = message.receiver;
        response.evenement = EVENEMENT;
        response.body = $scope.response;
        MessageManager.add(response).then(
            function(resp) {
                $scope.body = null;
                $scope.response = null;
                messages.push(resp);
                $modalInstance.close();
            },
            function(errorPayload) {
                alert("Erreur lors de l'ajout de la reponse");
        });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});