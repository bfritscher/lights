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
