;(function () {
   angular.module("RPi", ['ngRoute', 'RPi.auth', 'RPi.home', 'RPi.manager'])
      .config(function ($routeProvider) {
         console.log("RPi Controller v0.1");
         $routeProvider
            .when("/device-control/:id", {
               templateUrl: "ng/templates/home/home.html",
               controller: "ContentCtrl"
            })
            .when("/login", {
               templateUrl: "ng/templates/auth/auth.html",
               controller: "AuthCtrl",
               controllerAs: "auth"
            })

            .when("/register", {
               templateUrl: "ng/templates/auth/register.html",
            })

            .when("/device-manager", {
               templateUrl: "ng/templates/device/device-manager.html",
               controller: "ManagerCtrl",
               controllerAs: "manager"
            })
            .otherwise('/device-manager');
      })
})();

loading_screen.finish();

