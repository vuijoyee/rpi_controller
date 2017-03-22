;(function () {
    function authInterceptor(API, auth, $location) {
        return {
            // automatically attach Authorization header
            request: function (config) {
                var token = auth.getToken();
                if (config.url.indexOf(API) === 0 && token) {
                    config.headers.Authorization = 'JWT ' + token;
                }
                return config;
            },

            response: function (response) {
                if (response.config.url.indexOf(API) === 0 && response.data.token) {
                    auth.saveToken(response.data.token);
                }

                if (response.status == 401) {
                    $location.path('/auth');
                    console.log('401 -- Bad Request.');
                }

                return response;
            }
        }
    }

    angular.module('RPi.home', [])
    .factory('authInterceptor', authInterceptor)
    .config(function ($httpProvider) {
        $httpProvider.defaults.ContentType = 'application/json';
        $httpProvider.defaults.AccessControlAllowOrigin = '*';
        $httpProvider.interceptors.push('authInterceptor');
    })
})();