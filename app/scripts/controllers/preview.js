'use strict';


// convert 0..255 R,G,B values to a hexidecimal color string
var RGBToHex = function(r,g,b){
    var bin = r << 16 | g << 8 | b;
    return '#' + (function(h){
        return new Array(7-h.length).join("0") + h;
    })(bin.toString(16).toUpperCase());
};

// convert a 24 bit binary color to 0..255 R,G,B
var intToRGB = function(int){
    var r = int >> 16;
    var g = int >> 8 & 0xFF;
    var b = int & 0xFF;
    return [r,g,b];
};

/**
 * @ngdoc function
 * @name lightsApp.controller:PreviewCtrl
 * @description
 * # PreviewCtrl
 * Controller of the lightsApp
 */
angular.module('lightsApp')
  .controller('PreviewCtrl', function ($timeout) {

      var preview = this;
      var ws;

      preview.columnSpace = 40;
      preview.rowSpace = 10;

      preview.MATRIX_HEIGHT = 20;
      preview.MATRIX_WIDTH = 14;

      function connect(){
        // Connect to Web Socket
        ws = new WebSocket("ws://localhost:9001/");

        ws.onmessage = function(e) {
            $timeout(function(){
                var msg = JSON.parse(e.data);
                if ( msg.type === 'config') {
                    preview.MATRIX_HEIGHT = msg.MATRIX_HEIGHT;
                    preview.MATRIX_WIDTH = msg.MATRIX_WIDTH;
                    preview.ANIMATIONS = msg.ANIMATIONS;
                    preview.queue = msg.queue;
                }
                if ( msg.type === 'data') {
                    preview.matrixData = msg.data;
                }
                if ( msg.type === 'queue') {
                    preview.queue = msg.data;
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

      this.nextAnimation = function(){
          ws.send(JSON.stringify({
              'type': 'next'
          }));
      };

      this.removeAnimation = function(id){
          ws.send(JSON.stringify({
              'type': 'remove',
              'id': id
          }));
      };

      this.addAnimation = function(force){
          var paramsList = preview.ANIMATIONS[preview.selectedAnimationKey].params || [];
          var params = {};
          paramsList.forEach(function(p) {
                if (p.name) {
                    params[p.name] = p.default;
                }
          });
          ws.send(JSON.stringify({
              'type': 'anim',
              'name': preview.selectedAnimationKey,
              'force': force,
              'params': params
          }));
      };

      this.sendAction = function(param){
          var paramsList = param.params || [];
          var params = {};
          paramsList.forEach(function(p) {
                if (p.name) {
                    params[p.name] = p.default;
                }
          });

          ws.send(JSON.stringify({
              'type': 'action',
              'action': param.action,
              'params': params
          }));
      };

      this.getPixelPos = function(x, y) {
          return x * preview.MATRIX_HEIGHT + (x % 2 !== 0 ? y : preview.MATRIX_HEIGHT - y-1);
      };

      this.getPixelColor = function (x, y) {
          if (preview.matrixData) {
            var c = preview.matrixData[preview.getPixelPos(x, y)];
            return RGBToHex.apply(preview, intToRGB(c));
          }
          return '#000';
      };

      function getParam(params, key, value){
          for(var i=0; i < params.length; i++){
              if( params[i][key] === value){
                  return params[i];
              }
          }
      }

      this.sendXYClick = function(x, y){
        var param = getParam(preview.ANIMATIONS[preview.queue[0].name].params, 'type', 'xyclick');
        if (param) {
            param.params = param.params || [];
            var px = getParam(param.params, 'name', 'x');
            if(!px){
                px = {};
                param.params.push(px);
            }
            px.name = 'x';
            px.default = x;

            var py = getParam(param.params, 'name', 'y');
            if(!py){
                py = {};
                param.params.push(py);
            }
            py.name = 'y';
            py.default = y;

            preview.sendAction(param);
        }
      };

      this.sendXYOver = function(x, y){
        var param = getParam(preview.ANIMATIONS[preview.queue[0].name].params, 'type', 'xyover');
        if (param) {
            param.params = param.params || [];
            var px = getParam(param.params, 'name', 'x');
            if(!px){
                px = {};
                param.params.push(px);
            }
            px.name = 'x';
            px.default = x;

            var py = getParam(param.params, 'name', 'y');
            if(!py){
                py = {};
                param.params.push(py);
            }
            py.name = 'y';
            py.default = y;

            preview.sendAction(param);
        }
      };

      this.range = function(r){
          return Array.apply(null, new Array(r)).map(function (_, i) {return i;});
      };

      this.keys = function(object){
          if(object){
            var keys = Object.keys(object);
            keys.sort();
            return keys;
          }
      };



function makeGradientColor(color1, color2, percent) {
    var newColor = {};

    function makeChannel(a, b) {
        return a + Math.round((b-a) * percent);
    }

    function makeColorPiece(num) {
        num = Math.min(num, 255);   // not more than 255
        num = Math.max(num, 0);     // not less than 0
        var str = num.toString(16);
        if (str.length < 2) {
            str = "0" + str;
        }
        return(str);
    }

    newColor.r = makeChannel(color1.r, color2.r);
    newColor.g = makeChannel(color1.g, color2.g);
    newColor.b = makeChannel(color1.b, color2.b);
    return  "#" +
                        makeColorPiece(newColor.r) +
                        makeColorPiece(newColor.g) +
                        makeColorPiece(newColor.b);
}


      /* Test audio api */
      /* http://www.smartjava.org/examples/webaudio/example3.html */

    // create the audio context (chrome only for now)
    if (! window.AudioContext) {
        if (! window.webkitAudioContext) {
            alert('no audiocontext found');
        }
        window.AudioContext = window.webkitAudioContext;
    }
    var context = new AudioContext();
    var sourceNode;
    var analyser;
    var javascriptNode;

    // load the sound
    setupAudioNodes();
    loadSound('../01 Main title.mp3');


    function setupAudioNodes() {

        // setup a javascript node
        javascriptNode = context.createScriptProcessor(2048, 1, 1);
        // connect to destination, else it isn't called
        javascriptNode.connect(context.destination);


        // setup a analyzer
        analyser = context.createAnalyser();
        analyser.smoothingTimeConstant = 0.3;
        analyser.fftSize = Math.max(32, preview.MATRIX_WIDTH * 2);

        // create a buffer source node
        sourceNode = context.createBufferSource();
        sourceNode.connect(analyser);
        analyser.connect(javascriptNode);

        sourceNode.connect(context.destination);
    }

    // load the specified sound
    function loadSound(url) {
        var request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.responseType = 'arraybuffer';

        // When loaded decode the data
        request.onload = function() {

            // decode the data
            context.decodeAudioData(request.response, function(buffer) {
                // when the audio is decoded play the sound
                playSound(buffer);
            }, onError);
        }
        request.send();
    }


    function playSound(buffer) {
        sourceNode.buffer = buffer;
        sourceNode.start(0);
    }

    // log if an error occurs
    function onError(e) {
        console.log(e);
    }

    // when the javascript node is called
    // we use information from the analyzer node
    // to draw the volume
    javascriptNode.onaudioprocess = function() {

        // get the average for the first channel
        var array =  new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(array);

        drawSpectrum(array);

    }



    function drawSpectrum(array) {
        var data = [];
        for ( var x = 0; x < (array.length); x++ ){
            var value = array[x];
            var bucket = Math.floor(value / 255 * preview.MATRIX_HEIGHT)
            var col = [];
            data.push(col);
            for(var y=0; y < preview.MATRIX_HEIGHT; y++){
                var color = '#000000';
                if (y < bucket){
                    //TODO move color to cache
                    color = makeGradientColor({r:255,g:0,b:0}, {r:255,g:255,b:0}, y/20)
                }
                col[preview.MATRIX_HEIGHT-1 - y] = color;
            }
        }
        ws.send(JSON.stringify({
            'type': 'action',
            'action': 'draw_matrix',
            'params': {'data': data}
        }));
    };


  });
