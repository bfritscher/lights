'use strict';

/**
 * @ngdoc function
 * @name lightsApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the lightsApp
 */
angular.module('lightsApp')
  .controller('MainCtrl', function ($scope) {
    var main = this;
    main.currentName = 'default';
    var refresh = false;

    function initData(){
      refresh = true;
      for(var i=0; i < main.config.nbRows; i++){
        if(!main.config.data[i]) {
          main.config.data[i] = [];
        }
        for(var j=Math.min(main.config.data[i].length, main.config.nbColumns); j < main.config.nbColumns; j++){
          main.config.data[i][j] = 0;
        }
        main.config.data[i] = main.config.data[i].slice(0, j);
      }
      main.config.data = main.config.data.slice(0, i);
      refresh = false;
    }

    main.paint = function($event, row, index){
      if ( $event.shiftKey ) {
        row[index] = 'none';
      } else {
        row[index] = main.config.color;
      }
    };

    main.save = function(){
      main.config.name = main.currentName;
    };

    main.load = function(){
      var config = localStorage.getItem(main.currentName);
      if(!config){
        this.config = {
          data: [],
          nbRows: 32,
          nbColumns: 48,
          columnSpace: 120,
          rowSpace: 20,
          color: '#ff0000',
          name: main.currentName
        };
        initData();
      } else {
        this.config = angular.fromJson(config);
      }
    };

    main.export = function(){
        return JSON.stringify(main.config.data.map(function(r){ return r.map(function(i){ return i===0 || i==='none' ? 0 : 1;});}));
    };

    main.load();

    $scope.$watch('main.config', function(oldVal, newVal){
        if(!refresh){
          if(oldVal.nbRows !== newVal.nbRows || oldVal.nbColumns !== newVal.nbColumns){
            initData();
          }
          localStorage.setItem(main.config.name, angular.toJson(main.config));
        }
    }, true);

  });