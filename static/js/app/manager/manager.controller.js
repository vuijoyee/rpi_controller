;(function () {

   function handleRequest(res) {
      return res.data;
   }

   function ManagerCtrl(manager, auth, $location) {
      if (!auth.isAuthed()) {
         $location.path("/login");
      }

      vm = this;
      vm.dashboardRoute = function (id) {
         console.log('hello world');
         $location.path('device-control/' + id);
      };

      vm.createDeviceRoute = function () {
         $location.path('/device/new');
      };

      var getDevices = function () {
         return manager.get()
            .then(function (res) {
               console.log(res.data);
               vm.devices = res.data;
            });
      };

      getDevices();
   }

   angular.module('RPi.manager')
      .controller('ManagerCtrl', ManagerCtrl)
})();