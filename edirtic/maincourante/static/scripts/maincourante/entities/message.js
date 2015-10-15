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
    var messageManager = {

        ready: false,

        add: function (message) {
            var deferred = $q.defer();
            //TODO PUT
            /*$http.post("/api/v1/message/?format=json")
             .success(function (data) {
             deferred.resolve(message);
             })
             .error(function () {
             deferred.reject();
             });*/
            deferred.resolve(message); //TODO Remove this line when update function is implemented
            return deferred.promise;
        },
        delete: function (index, message) {
            var deferred = $q.defer();
            //TODO PUT
            /*$http.post("/api/v1/message/?format=json")
             .success(function (data) {
             deferred.resolve(message);
             })
             .error(function () {
             deferred.reject();
             });*/
            deferred.resolve(message); //TODO Remove this line when update function is implemented
            return deferred.promise;

        },
        load: function () {
            var deferred = $q.defer();
            $http.get("/api/v1/message/?format=json")
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