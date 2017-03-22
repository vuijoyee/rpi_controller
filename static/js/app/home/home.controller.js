;(function () {

    function ContentCtrl($scope,
                         $rootScope,
                         $location,
                         $interval,
                         auth,
                         PinService,
                         DigitalInputService,
                         DigitalOutputService,
                         AnalogOutputService,
                         AnalogInputService) {


        if (!auth.isAuthed()) {
            $location.path("/auth");
        }


        function handleRequest(res) {
            console.log(res.data);
            return res.data;
        }


        $rootScope.showNavigation = true;
        $scope.slider = 46;
        $scope.slider2 = 182;
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
                debug: false
            },
            checked: false,
            relays: {
                A0: true,
                A1: false,
                A2: false,
                A3: false,
                A4: true,
                A5: false,
                A6: false,
                A7: false
            },

            digital_input: {
                DIN1: false,
                DIN2: false
            },
            digital_output: {
                DOUT1: false,
                DOUT2: false

            },

            analog_input: {
                random: false,
                checked: true,
                IN1: 1.8,
                IN2: 37
            },
            analog_output: {
                OUT1: 0,
                OUT2: 0,
            }
        };


        $scope.$watch('data.analog_output.OUT1', function (val) {
            //console.log('AOUT1: ' + val);
            $scope.data.analog_output.AOUT1 = val;
            console.log($scope.data.analog_output);
            AnalogOutputService.put(4, $scope.data.analog_output)
                .then(handleRequest);

        });

        $scope.$watch('data', function (val) {
            console.log(data);
        });

        $scope.$watch('data.analog_output.OUT2', function (val) {
            //console.log('AOUT2' + val);
            $scope.data.analog_output.AOUT2 = val;
            console.log($scope.data.analog_output);
            AnalogOutputService.put(4, $scope.data.analog_output);
        });


        $scope.writePins = function (id) {
            PinService.put(id, $scope.data.relays).then(handleRequest);
            console.log($scope.data.relays);

        };

        AnalogOutputService.put(4, $scope.data.analog_output);
    }

    angular.module('RPi.home')
        .controller('ContentCtrl', ContentCtrl)
})();
