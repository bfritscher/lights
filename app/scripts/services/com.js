'use strict';

/**
 * @ngdoc service
 * @name lightsApp.com
 * @description
 * # com
 * Service in the lightsApp.
 */
angular.module('lightsApp')
  .service('com', function ($timeout, $rootScope) {
     var com = this;

     this.config = {
        MATRIX_HEIGHT: 20,
        MATRIX_WIDTH: 14
     };

     var ws;

     function connect(){
        // Connect to Web Socket
        //ws = new WebSocket("ws://ne.fritscher.ch:9001/");
        ws = new WebSocket("ws://192.168.101.154:9001/");

        ws.onmessage = function(e) {
            $timeout(function(){
                var msg = JSON.parse(e.data);
                if ( msg.type === 'config') {
                    com.config.MATRIX_HEIGHT = msg.MATRIX_HEIGHT;
                    com.config.MATRIX_WIDTH = msg.MATRIX_WIDTH;
                    com.config.ANIMATIONS = msg.ANIMATIONS;
                    com.config.queue = msg.queue;
                    com.config.client_id = msg.client_id;
                }
                if ( msg.type === 'data') {
                    com.config.matrixData = msg.data;
                    $rootScope.$broadcast('ledata', msg.data);
                }
                if ( msg.type === 'queue') {
                    com.config.queue = msg.data;
                }
            });
        };

        ws.onerror = function(e) {
            console.log(e);
        };

        ws.onclose = function(){
            //try to reconnect in 5 seconds
            $timeout(function(){
                connect();
            }, 2000);
        };
      }
      connect();

      this.send = function(data){
          ws.send(data);
      };

  });
