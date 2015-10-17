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
        cree: null,

        setMessage: function (data) {

        },
        equals: function () {
            throw new Error("Not implemented");
        },
        toString: function () {
            return ""
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
            $http.put(entry_point+"/"+message.id, message)
                .success(function (data) {
                    var newMessage = new Message();
                    newMessage.expediteur = message.expediteur;
                    newMessage.recipiendaire = message.recipiendaire;
                    newMessage.corps = message.oldMessage;
                    newMessage.cree = new Date();
                    newMessage.parent = message.id;
                    _this.add(newMessage, message).then(
                        function(message) {
                            message.oldMessage.edit = false;
                            deferred.resolve(message);
                        },
                        function(errorPayload) {
                            alert(errorPayload);
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
            $http.get(entry_point+"?format=json")
                .success(function (data) {
                    deferred.resolve(data.objects);
                })
                .error(function () {
                    deferred.reject();
                });
            return deferred.promise;
        }
    };
    return messageManager;
}