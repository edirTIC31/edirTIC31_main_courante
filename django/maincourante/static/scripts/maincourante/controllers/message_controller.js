angular.module("edir.maincourante.controllers", []);

angular.module('edir.maincourante.controllers')
  .controller('MainCtrl', ['$scope', 'Message', 'MessageManager', 'IndicatifManager', '$modal', '$interval','focus', '$filter', prepareMainController]);

function prepareMainController($scope, Message, MessageManager, IndicatifManager,  $modal, $interval, focus, $filter){
	
	$scope.messages = [];
    $scope.isLoading = true;
    $scope.editionMode = false;
    $scope.disableAutoLoad = false;
    $scope.indicatifs = new Array();
    $scope.errorMessage = null;
    $scope.lastRetrivalDate = null;

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
                $scope.disableAutoLoad = false;
                message.edit = false;
                message.modified = true;
                //loadMessages();
                focus('onNewMessage');
            },
            function(errorPayload) {
                alert("Erreur lors de l'edition du message");
                $scope.disableAutoLoad = false;
            });
    }

    $scope.cancelMessageEdition = function(message){
        message.cancelEdition();
        focus('onNewMessage');
        $scope.disableAutoLoad = false;
    }

    function loadMessages() {
        if(!$scope.disableAutoLoad) {
            MessageManager.load($scope.lastRetrivalDate).then(
                function (newMessages) {
                    if(newMessages && newMessages.length > 0) {
                        if( $scope.messages.length == 0){
                            $scope.messages = newMessages;
                        }else{
                            angular.forEach(newMessages, function (newMessage){
                                var found = false;
                                angular.forEach($scope.messages, function (existingMessage, key) {
                                    if(existingMessage.id == newMessage.id){
                                        $scope.messages[key].body = newMessage.body;
                                        $scope.messages[key].deleted = newMessage.deleted;
                                        $scope.messages[key].modified = newMessage.modified;
                                        found = true;
                                    }
                                });
                                if(!found){
                                    $scope.messages.push(newMessage);
                                }
                            });
                        }
                        $scope.lastRetrivalDate = $filter('date')(new Date(), 'yyyy-MM-ddTHH:mm:ss.sss');
                    }
                    $scope.errorMessage = null;
                    $scope.isLoading = false;
                },
                function (errorPayload) {
                    $scope.errorMessage = "Erreur lors du chargement des messages";
                }
            );
        }
    }

    function loadIndicatifs(){
        IndicatifManager.load().then(
            function (indicatifs) {
                $scope.indicatifs = indicatifs;
            },
            function (errorPayload) {
                $scope.errorMessage = "Erreur lors du chargement des indicatifs";
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
            loadMessages();
        }, function () {

        });
    };

    $scope.toggleAnimation = function () {
        $scope.animationsEnabled = !$scope.animationsEnabled;
    };

    loadMessages();
    focus('onNewMessage');
    $interval(loadMessages, 12000);

    $scope.enableEditionMode = function() {
        $scope.editionMode = true;
        loadIndicatifs();
        $interval(loadIndicatifs, 12000);
    }
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

angular.module('edir.maincourante.controllers').controller('ModalReplyMessageCtrl', function ($scope, $modalInstance, MessageManager, Message, focus, message, messages) {
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
                $modalInstance.close();
                focus('onNewMessage');
            },
            function(errorPayload) {
                alert("Erreur lors de l'ajout de la reponse");
        });
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});