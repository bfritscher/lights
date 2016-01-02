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
    'ngTouch',
    'ngMaterial'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/editor', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
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
