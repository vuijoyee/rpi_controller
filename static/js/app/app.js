;(function () {
    angular.module("RPi", ['ngRoute', 'RPi.auth', 'RPi.home'])
    .config(function ($routeProvider) {
        console.log("RPi Controller v0.1");
        $routeProvider
        .when("/", {
            templateUrl: "api/templates/home/home.html",
            controller: "ContentCtrl"
        })
        .when("/register-new-device", {
            templateUrl: "api/templates/home/home.html"
        })
        .when("/auth", {
            templateUrl: "api/templates/auth/auth.html",
            controller: "AuthCtrl",
            controllerAs: "auth"
        })

        .when("/device-list", {
            templateUrl: "api/templates/home/device-list.html",
            controller: "DeviceListCtrl",
            controllerAs: "list"
        })
    })

})();
