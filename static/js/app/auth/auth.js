;(function () {
   function authInterceptor(API, auth) {
      return {
         // automatically attach Authorization header
         request: function (config) {
            var token = auth.getToken();
            if (config.url.indexOf(API) === 0 && token) {
               config.headers.Authorization = 'JWT ' + token;
            }
            return config;
         },

         response: function (res) {
            if (res.config.url.indexOf(API) === 0 && res.data.token) {
               auth.saveToken(res.data.token);
            }
            return res;
         }
      }
   }

   function authService($window) {
      var srvc = this;

      srvc.parseJwt = function (token) {
         var base64Url = token.split('.')[1];
         var base64 = base64Url.replace('-', '+').replace('_', '/');
         return JSON.parse($window.atob(base64));
      };

      srvc.saveToken = function (token) {
         $window.localStorage['jwtToken'] = token
      };

      srvc.logout = function () {
         $window.localStorage.removeItem('jwtToken');
      };

      srvc.getToken = function () {
         return $window.localStorage['jwtToken'];
      };

      srvc.isAuthed = function () {
         var token = srvc.getToken();
         if (token) {
            var params = srvc.parseJwt(token);
            return Math.round(new Date().getTime() / 1000) <= params.exp;
         } else {
            return false;
         }
      }

   }

   function userService($http, TokenAuth, auth) {
      var srvc = this;

      srvc.register = function (username, password) {
         return $http.post(TokenAuth + '/auth/register', {
            username: username,
            password: password
         });
      };

      srvc.login = function (username, password) {
         return $http.post(TokenAuth + 'token/', {
            username: username,
            password: password
         }).then(srvc.handleRequest, srvc.handleRequest)
      };
   }

// We won't touch anything in here
   function AuthCtrl(user, auth, $location, $rootScope) {
      var self = this;
      $rootScope.showNavigation = false;

      function handleRequest(res) {
         var token = res.data ? res.data.token : null;
         if (token) {
            console.log('JWT:', token);
            auth.saveToken(token);
            $rootScope.loggedIn = true;
            $location.path("/");
         }
         self.message = res.data.non_field_errors;
      }

      self.login = function () {
         user.login(self.username, self.password)
            .then(handleRequest, handleRequest)
      };
      self.register = function () {
         user.register(self.username, self.password)
            .then(handleRequest, handleRequest)
      };
      self.logout = function () {
         auth.logout && auth.logout()
      };
      self.isAuthed = function () {
         return auth.isAuthed ? auth.isAuthed() : false
      };
   }

   angular.module('RPi.auth', [])
      .factory('authInterceptor', authInterceptor)
      .service('user', userService)
      .service('auth', authService)
      .constant('TokenAuth', '/auth/')
      .constant('API', '/api/v1/')
      .config(function ($httpProvider) {
         $httpProvider.defaults.ContentType = 'application/json';
         $httpProvider.defaults.AccessControlAllowOrigin = '*';
         $httpProvider.interceptors.push('authInterceptor');
      })
      .controller('AuthCtrl', AuthCtrl)
})();