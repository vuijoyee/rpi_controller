;(function () {
   angular.module("RPi.manager", [])
    .config(function ($httpProvider) {
        $httpProvider.defaults.ContentType = 'application/json';
        $httpProvider.defaults.AccessControlAllowOrigin = '*';
        $httpProvider.interceptors.push('authInterceptor');
    })
})();