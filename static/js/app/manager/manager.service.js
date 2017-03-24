;(function () {

   function ManagerService($http, API) {

      srvc = this;
      srvc.get = function () {
         return $http.get(API + 'devices/')
      };

      srvc.put = function (id, data) {
         return $http.put(API + 'device/' + id, data)
      }
   }

   angular.module('RPi.manager')
      .service('manager', ManagerService)
   
})();