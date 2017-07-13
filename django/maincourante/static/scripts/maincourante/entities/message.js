angular.module("edir.maincourante.entities", []);

angular.module("edir.maincourante.entities")
    .factory("Message", [MessageFactory])
    .factory("MessageManager", ["Message", "$q", "$http", MessageManagerFactory]);

function MessageFactory() {
    function Message(data) {
        if (data) {
            this.setMessage(data);
        }else{
            this.getAsObject();
        }
    }

    Message.prototype = {
        id: null,
        evenement: 1,
        sender: null,
        body: null,
        receiver: null,
        edit: false,
        previousBody: null,
        cree: null,
        operateur: null,
        deleted: null,
        modified: null,
        displayCreationDate: null,
        timestamp: null,
        setMessage: function (data) {
            var self = this;
            self.id = data.id;
            self.evenement = data.evenement;
            self.sender = data.sender;
            self.receiver = data.receiver;
            self.body = data.body;
            self.cree = new Date(data.timestamp);
            self.displayCreationDate = new Date(data.timestamp);
            self.operateur = data.operateur;
            self.timestamp = data.timestamp;
            self.deleted = data.deleted;
            self.modified = data.modified;
        },
        getAsObject: function () {
            var self = this;
            return {
                id: self.id,
                sender: self.sender,
                body: self.body,
                receiver: self.receiver,
                edit: self.edit,
                previousBody: self.previousBody,
                operateur: self.operateur,
                cree: self.timestamp,
                deleted: self.deleted,
                modified: self.modified,
                displayCreationDate: null,
                timestamp: self.timestamp
            };
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
    var entry_point = api_url + 'message/';
    var messageManager = {
        ready: false,
        add: function (message) {
            var deferred = $q.defer();
            var _this = this;
            $http.post(entry_point, message)
             .success(function (data) {
                deferred.resolve(new Message(data));
             })
             .error(function (resp) {
                _this.handleErrorMessage("Erreur lors de l'ajout d'un message", resp);
                deferred.reject();
             });
            return deferred.promise;
        },
        modify: function (message) {
            var deferred = $q.defer();
            var _this = this;
            $http.put(entry_point+message.id, message)
                .success(function (messageData) {
                    deferred.resolve(message);
                })
                .error(function (resp) {
                    _this.handleErrorMessage("Erreur lors de la modification d'un message", resp);
                    deferred.reject();
                });
            return deferred.promise;
        },
        delete: function (message, suppressionMessage) {
            var deferred = $q.defer();
            var _this = this;
            $http.delete(entry_point+message.id+"?reason="+suppressionMessage, message)
                .success(function (data) {
                    deferred.resolve(message);
                })
                .error(function (resp) {
                    _this.handleErrorMessage("Erreur lors de la suppression d'un message", resp);
                    deferred.reject();
                });
            return deferred.promise;

        },
        load: function (lastTimestamp) {
            var deferred = $q.defer();
            var _this = this;
            var loadUrl = entry_point+"?format=json&limit=0&evenement="+EVENEMENT_ID;
            if(lastTimestamp){
                loadUrl += "&newer-than="+lastTimestamp;
            }
            $http.get(loadUrl)
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
                .error(function (resp) {
                    _this.handleErrorMessage("Erreur lors du chargement des messages", resp);
                    deferred.reject();
                });
            return deferred.promise;
        },
        handleErrorMessage: function(message, error){
            console.log(error);
            console.log("URL " + window.location.origin + entry_point);
            if(message !== undefined && error.error_message !== undefined){
                alert(message +" : "+error.error_message);
            }else{
                alert(message);
            }
        }
    };
    return messageManager;
}
