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
  .controller('PreviewCtrl', function (com) {

      var preview = this;

      this.columnSpace = 40;
      this.rowSpace =  10;

      preview.com = com;

      preview.colorPickerOptions = {
        preferredFormat: 'hex',
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


      this.nextAnimation = function(){
          com.send(JSON.stringify({
              'type': 'next'
          }));
      };

      this.removeAnimation = function(id){
          com.send(JSON.stringify({
              'type': 'remove',
              'id': id
          }));
      };

      this.addAnimation = function(force){
          var paramsList = preview.com.config.ANIMATIONS[preview.selectedAnimationKey].params || [];
          var params = {};
          paramsList.forEach(function(p) {
                if (p.name) {
                    params[p.name] = p.default;
                }
          });
          com.send(JSON.stringify({
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

          com.send(JSON.stringify({
              'type': 'action',
              'action': param.action,
              'params': params
          }));
      };

      this.getPixelPos = function(x, y) {
          return x * preview.com.config.MATRIX_HEIGHT + (x % 2 !== 0 ? y : preview.com.config.MATRIX_HEIGHT - y-1);
      };

      this.getPixelColor = function (x, y) {
          if (preview.com.config.matrixData) {
            var c = preview.com.config.matrixData[preview.getPixelPos(x, y)];
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
        var param = getParam(preview.com.config.ANIMATIONS[preview.com.config.queue[0].name].params, 'type', 'xyclick');
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
        var param = getParam(preview.com.config.ANIMATIONS[preview.com.config.queue[0].name].params, 'type', 'xyover');
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

      this.liveParam = function (param){
          if (param.live) {
              this.sendAction(param);
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

  });
