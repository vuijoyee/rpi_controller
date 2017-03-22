;(function () {

    function AnalogInputService($http, API) {
        srvc = this;
        srvc.get = function (id) {
            return $http.get(API + 'lift/' + id + '/analog-input/')
        };
    }

    function AnalogOutputService($http, API) {
        srvc = this;
        srvc.get = function (id) {
            return $http.get(API + 'lift/' + id + '/analog-output/')
        };
        srvc.put= function (id, data) {
            return $http.put(API + 'lift/' + id + '/analog-output/', data)
        }
    }

    function DigitalInputService($http, API) {
        srvc = this;
        srvc.get = function (id) {
            return $http.get(API + 'lift/' + id + '/digital-input/')
        }
    }


    function DigitalOutputService($http, API) {
        srvc = this;
        srvc.get = function (id) {
            return $http.get(API + 'lift/' + id + '/digital-output/')
        }
    }

    function PinService($http, API) {
        srvc = this;
        srvc.get = function (id) {
            return $http.get(API + 'lift/' + id + '/pin/')
        };

        srvc.put = function (id, data) {
            return $http.put(API + 'lift/' + id + '/pin/', data)
        }
    }

    angular.module('RPi.home')
    .service('AnalogInputService', AnalogInputService)
    .service('AnalogOutputService', AnalogOutputService)
    .service('DigitalInputService', DigitalInputService)
    .service('DigitalOutputService', DigitalOutputService)
    .service('PinService', PinService)
    .constant('API', '/api/v1/')
})();