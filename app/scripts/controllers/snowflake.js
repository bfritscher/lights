'use strict';

/**
 * @ngdoc function
 * @name lightsApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the lightsApp
 */
angular.module('lightsApp')
  .controller('SnowflakeCtrl', function ($scope, MQTTService) {
    $scope.editorOptions = {
      mode: 'python',
      lineNumbers: true,
    };

    $scope.colorPickerOptions = {
        preferredFormat: 'rgb',
        showInput: true,
        containerClassName: 'colorpicker',
        flat: true,
        showInitial: false,
        localStorageKey: 'colorpicker',
        showPalette: true,
        showSelectionPalette: true,
        chooseText: 'save to palette',
        cancelText: '',
        palette: [ '#001F3F', '#0074D9', '#7FDBFF', '#39CCCC',
                   '#3D9970', '#2ECC40', '#01FF70', '#FFDC00',
                   '#FF851B', '#FF4136', '#F012BE', '#B10DC9',
                   '#85144B', '#FFFFFF', '#AAAAAA', '#DDDDDD',
                   '#111111'
        ]
      };

    $scope.animation = 'sf.color(Color(0,0,255))\n'
      + 'wait(500)\n'
      + 'sf.color(Color(0,255,0))\n'
      + 'wait(500)\n'
      + 'sf.color(Color(255,0,0))\n'
      + 'wait(500)\n';

    MQTTService.on('lights/snowflake/error', function (data) {
      $scope.error = data;
    });

    $scope.send = function () {
      $scope.error = '';
      MQTTService.send('lights/snowflake', $scope.animation);
    };




  });
