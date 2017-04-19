;(function () {
   function DeviceInformationService($http, API) {
      srvc = this;
      srvc.get = function (id) {
         return $http.get(API + 'device/' + id + '/')
      };
   }

   function AnalogInputService($http, API) {
      srvc = this;
      srvc.get = function (id) {
         return $http.get(API + 'device/' + id + '/analog-input/')
      };
   }

   function AnalogOutputService($http, API) {
      srvc = this;
      srvc.get = function (id) {
         return $http.get(API + 'device/' + id + '/analog-output/')
      };
      srvc.put = function (id, data) {
         return $http.put(API + 'device/' + id + '/analog-output/', data)
      }
   }

   function DigitalInputService($http, API) {
      srvc = this;
      srvc.get = function (id) {
         return $http.get(API + 'device/' + id + '/digital-input/')
      }
   }


   function DigitalOutputService($http, API) {
      srvc = this;
      srvc.get = function (id) {
         return $http.get(API + 'device/' + id + '/digital-output/')
      };

      srvc.put = function (id, data) {
         return $http.put(API + 'device/' + id + '/digital-output/', data)
      };
   }

   function PinService($http, API) {
      srvc = this;
      srvc.get = function (id) {
         return $http.get(API + 'device/' + id + '/relay/')
      };

      srvc.put = function (id, data) {
         return $http.put(API + 'device/' + id + '/relay/', data)
      }
   }

   angular.module('RPi.home')
      .service('AnalogInputService', AnalogInputService)
      .service('DeviceInformationService', DeviceInformationService)
      .service('AnalogOutputService', AnalogOutputService)
      .service('DigitalInputService', DigitalInputService)
      .service('DigitalOutputService', DigitalOutputService)
      .service('PinService', PinService)
      .constant('API', '/api/v1/')
})();