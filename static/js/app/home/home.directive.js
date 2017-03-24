;(function () {
   function slider() {
      return {
         restrict: 'A',
         link: function (scope, element, attrs) {
            attrs.$observe('sliderValue', function (newVal, oldVal) {
               console.log(newVal);
               element.slider('setValue', newVal);
            });
         }
      }
   }

   function sliderBind($parse) {
      return {
         restrict: 'A',
         link: function (scope, element, attrs) {
            var val = $parse(attrs.sliderBind);
            scope.$watch(val, function (newVal, oldVal) {
               console.log('Slider Bind: ' + attrs.sliderBind + ' -- ' + newVal);
               element.slider('setValue', newVal);
            });

            // when the slider is changed, update the scope
            // property.
            // Note that this will only update it when you stop dragging.
            // If you need it to happen whilst the user is dragging the
            // handle, change it to "slide" instead of "slideStop"
            // (this is not as efficient so I left it up to you)
            element.on('slide', function (event) {
               // if expression is assignable
               if (val.assign) {
                  val.assign(scope, event.value);
                  scope.$digest();
               }
            });
         }
      }
   }

   angular.module('RPi.home')
      .directive('slider', slider)
      .directive('sliderBind', sliderBind)
})();