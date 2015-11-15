angular.module("edir.maincourante.entities", []);

"use strict";

angular.module("edir.maincourante.entities")
    .factory("Message", [MessageFactory])
    .factory("MessageManager", ["Message", "$q", "$http", MessageManagerFactory]);

function MessageFactory() {
    function Message(data) {
        if (data) {
            this.setMessage(data);
        }
    }

    Message.prototype = {
        id: null,
        evenement: null,
        sender: null,
        body: null,
        receiver: null,
        edit: false,
        previousBody: null,
        cree: null,
        parent: null,
        suppression: null,
        displayCreationDate: null,
        timestamp: null,
        setMessage: function (data) {
            this.id = data.id;
            this.evenement = data.evenement;
            this.sender = data.sender;
            this.receiver = data.receiver;
            this.body = data.body;
            this.cree = new Date(data.timestamp);
            this.displayCreationDate = new Date(data.timestamp);
            this.parent = data.parent;
            this.timestamp = data.timestamp;
        },
        equals: function () {
            throw new Error("Not implemented");
        },
        toString: function () {
            return ""
        },
        isValid: function (){
            return (this.body != null && this.body != "" && this.sender != null && this.sender != "" && this.receiver != null && this.receiver != "")
        },
        enableEdition: function(){
            this.edit = true;
            this.previousBody = this.body;
        },
        cancelEdition: function(){
            this.corps = this.previousBody;
            this.previousBody = null;
            this.edit = false;
        }
    };
    return Message;
}

function MessageManagerFactory(Message, $q, $http) {
    var entry_point = '/api/v1/message/';
    var messageManager = {
        ready: false,
        add: function (message, previousMessage) {
            var deferred = $q.defer();
            if(previousMessage != undefined){
                message.parent = previousMessage.id;
            }
            $http.post(entry_point, message)
             .success(function (data) {
                deferred.resolve({message: message, previousMessage: previousMessage});
             })
             .error(function () {
                deferred.reject();
             });
            return deferred.promise;
        },
        modify: function (message) {
            var deferred = $q.defer();
            var _this = this;
            $http.put(entry_point+message.id, message)
                .success(function (data) {
                    var newMessage = new Message();
                    newMessage.sender = message.sender;
                    newMessage.receiver = message.receiver;
                    newMessage.body = message.previousMessage;
                    newMessage.parent = message.id;
                    _this.add(newMessage, message).then(
                        function(message) {
                            deferred.resolve(message);
                        },
                        function(errorPayload) {
                            alert("Erreur lors de la sauvegarde de l'ancien message");
                    });
                })
                .error(function () {
                    deferred.reject();
                });
            return deferred.promise;
        },
        delete: function (message, suppressionMessage) {
            var deferred = $q.defer();
            message.suppression = suppressionMessage;
            $http.put(entry_point+"/"+message.id, message)
                .success(function (data) {
                    deferred.resolve(message);
                })
                .error(function () {
                    deferred.reject();
                });
            return deferred.promise;

        },
        load: function () {
            var deferred = $q.defer();
            $http.get(entry_point+"?format=json&limit=1000")
                .success(function (data) {
                    var messages = new Array();
                    if(data.messages != null){
                        angular.forEach(data.messages, function (messageData, key) {
                            var message = new Message(messageData)
                            messages.push(message);
                        });
                    }
                    deferred.resolve(messages);
                })
                .error(function () {
                    deferred.reject();
                });
            return deferred.promise;
        }
    };
    return messageManager;
}
