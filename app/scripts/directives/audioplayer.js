'use strict';

/**
 * @ngdoc directive
 * @name lightsApp.directive:audioPlayer
 * @description
 * # audioPlayer
 */
angular.module('lightsApp')
  .directive('audioPlayer', function () {
    return {
      template: '<div></div>',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        element.text('this is the audioPlayer directive');
      }
    };
  });
