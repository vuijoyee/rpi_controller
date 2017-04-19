;(function () {

   function ContentCtrl($scope,
                        $rootScope,
                        $routeParams,
                        $location,
                        auth,
                        PinService,
                        DeviceInformationService,
                        DigitalInputService,
                        DigitalOutputService,
                        AnalogOutputService,
                        AnalogInputService) {


      if (!auth.isAuthed()) {
         $location.path("/login");
      }

      var device = {
         id: $routeParams.id
      };


      function handleRequest(res) {
         console.log(res.data);
         return res.data;
      }

      $scope.data = {
         global_settings: {
            device: null,
            hello: "world"
         },
         show_settings: {
            relay_control: false,
            digital_output: false,
            digital_input: false,
            analog_input: false,
            analog_output: false
         },
         show_panel: {
            relay_control: false,
            digital_output: false,
            digital_input: false,
            analog_input: false,
            analog_output: false,
            debug: true
         },
         checked: false,
         relays: device.relay,
         digital_input: {
            DIN1: null,
            DIN2: null
         },
         digital_output: {
            DOUT1: null,
            DOUT2: null
         },
         analog_input: {
            AIN1: null,
            AIN2: null
         },
         analog_output: {
            AOUT1: null,
            AOUT2: null
         }
      };


      DeviceInformationService.get(device.id).then(function (res) {
         device.data = res.data;
         device.relay = device.data.relay;
         $scope.device = device.data;

         $scope.data.digital_input.DIN1 = device.data.digitalinput.DIN1;
         $scope.data.digital_input.DIN2 = device.data.digitalinput.DIN2;

         $scope.data.digital_output.DOUT1 = device.data.digitaloutput.DOUT1;
         $scope.data.digital_output.DOUT2 = device.data.digitaloutput.DOUT2;
         $scope.data.digital_output.DOUT3 = device.data.digitaloutput.DOUT3;
         $scope.data.digital_output.DOUT4 = device.data.digitaloutput.DOUT4;

         $scope.data.analog_input.AIN1 = device.data.analoginput.AIN1;
         $scope.data.analog_input.AIN2 = device.data.analoginput.AIN2;

         $scope.data.analog_output.AOUT1 = device.data.analogoutput.AOUT1;
         $scope.data.analog_output.AOUT2 = device.data.analogoutput.AOUT1;
      });

      $scope.$watch('data.analog_output.AOUT1', function (val) {
         $scope.data.analog_output.AOUT1 = val;
         AnalogOutputService.put(device.id, $scope.data.analog_output)
            .then(handleRequest);

      });

      $scope.$watch('data.analog_output.AOUT2', function (val) {
         $scope.data.analog_output.AOUT2 = val;
         AnalogOutputService.put(device.id, $scope.data.analog_output)
            .then(handleRequest);
      });


      $scope.$watch('data.digital_output.DOUT1', function (val) {
         $scope.data.digital_output.DOUT1 = val;
         new PNotify({
            title: 'Digital Output Section Updated!',
            text: 'That thing that you were trying to do worked!',
            type: 'success',
            delay: 500
         });
         DigitalOutputService.put(device.id, $scope.data.digital_output)
            .then(handleRequest);

      });

      $scope.$watch('data.digital_output.DOUT2', function (val) {
         $scope.data.digital_output.DOUT2 = val;
         DigitalOutputService.put(device.id, $scope.data.digital_output)
            .then(handleRequest);
      });


      $scope.writePins = function () {
         PinService.put(device.id, $scope.data.relays).then(handleRequest);
         console.log($scope.data.relays);

      };
   }

   angular.module('RPi.home')
      .controller('ContentCtrl', ContentCtrl)
})();
