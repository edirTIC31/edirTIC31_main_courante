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
        corps: null,
        expediteur: null,
        recipiendaire: null,
        oldMessage: null,
        edit: false,
        showHistory: false,
        cree: null,
        parent: null,
        suppression: null,
        setMessage: function (data) {
            this.id = data.id;
            this.corps = data.corps;
            this.expediteur = data.expediteur;
            this.recipiendaire = data.recipiendaire;
            this.cree = new Date(data.cree);
            this.parent = data.parent;
            this.suppression = data.suppression;
        },
        equals: function () {
            throw new Error("Not implemented");
        },
        toString: function () {
            return ""
        },
        isValid: function (){
            return (this.corps != null && this.corps != "" && this.expediteur != null && this.expediteur != "" && this.recipiendaire != null && this.recipiendaire != "")
        },
        enableEdition: function(){
            this.edit = true;
            this.oldMessage = this.corps;
        },
        cancelEdition: function(){
            this.corps = this.oldMessage;
            this.oldMessage = null;
            this.edit = false;
        }
    };
    return Message;
}

function MessageManagerFactory(Message, $q, $http) {
    var entry_point = '/api/v1/message/';
    var messageManager = {
        ready: false,
        add: function (message, oldMessage) {
            var deferred = $q.defer();
            if(oldMessage != undefined){
                message.parent = oldMessage.id;
            }
            $http.post(entry_point, message)
             .success(function (data) {
                deferred.resolve({message: message, oldMessage: oldMessage});
             })
             .error(function () {
                deferred.reject();
             });
            return deferred.promise;
        },
        modify: function (message) {
            var deferred = $q.defer();
            var _this = this;
            var olCreationDate = message.cree;
            message.cree = null;
            $http.put(entry_point+message.id, message)
                .success(function (data) {
                    var newMessage = new Message();
                    newMessage.expediteur = message.expediteur;
                    newMessage.recipiendaire = message.recipiendaire;
                    newMessage.corps = message.oldMessage;
                    newMessage.cree = new Date();
                    newMessage.parent = message.id;
                    _this.add(newMessage, message).then(
                        function(message) {
                            message.oldMessage.cree = olCreationDate;
                            message.oldMessage.edit = false;
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
                    if(data.objects != null){
                        var childrenMessages = new Array();
                        angular.forEach(data.objects, function (messageData, key) {
                            var message = new Message(messageData)
                            if(message.parent) {
                                var parentArray = childrenMessages[message.parent];
                                if(!parentArray){
                                    parentArray = new Array();
                                }
                                parentArray.push(message);
                                childrenMessages[message.parent] = parentArray;
                            }else{
                                messages.push(message);
                            }
                        });
                        angular.forEach(messages, function (message, key) {
                           message.history = childrenMessages[message.id];
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
