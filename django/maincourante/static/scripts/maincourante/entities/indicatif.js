angular.module("edir.maincourante.entities")
    .factory("Indicatif", [IndicatifFactory])
    .factory("IndicatifManager", ["Indicatif", "$q", "$http", IndicatifManagerFactory]);

function IndicatifFactory() {
    function Indicatif(data) {
        if (data) {
            this.setIndicatif(data);
        }
    }

    Indicatif.prototype = {
        id: null,
        name: null,
        evenementId: null,
        setIndicatif: function (data) {
            this.id = data.id;
            this.name = data.nom;
            this.evenementId = data.evenementId;
        }
    };
    return Indicatif;
}


function IndicatifManagerFactory(Indicatif, $q, $http) {
    var entry_point = '/api/v1/indicatif/';
    var indicatiManager = {
        load: function () {
            var deferred = $q.defer();
            $http.get(entry_point+"?format=json&limit=0")
                .success(function (data) {
                    var indicatifs = new Array();
                    if(data.objects != null){
                        angular.forEach(data.objects, function (data, key) {
                            var indicatif = new Indicatif(data)
                            indicatifs.push(indicatif);
                        });
                    }
                    deferred.resolve(indicatifs);
                })
                .error(function () {
                    deferred.reject();
                });
            return deferred.promise;
        }
    };
    return indicatiManager;
}
