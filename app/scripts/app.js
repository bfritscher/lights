'use strict';

/**
 * @ngdoc overview
 * @name lightsApp
 * @description
 * # lightsApp
 *
 * Main module of the application.
 */
angular
  .module('lightsApp', [
    'ngAnimate',
    'ngRoute',
    'ngMaterial',
    'angularSpectrumColorpicker',
    'ngMQTT',
    'ui.codemirror'
  ])
  .config(['MQTTProvider',function(MQTTProvider){
        MQTTProvider.setHref('ws://192.168.101.1:1884');
    }])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/editor', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/snowflake', {
        templateUrl: 'views/snowflake.html',
        controller: 'SnowflakeCtrl',
        controllerAs: '$ctrl'
      })
      .when('/preview', {
        templateUrl: 'views/preview.html',
        controller: 'PreviewCtrl',
        controllerAs: 'preview'
      })
      .otherwise({
        redirectTo: '/preview'
      });
  });
