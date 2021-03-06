'use strict';

/**
 * @ngdoc directive
 * @name lightsApp.directive:audioPlayer
 * @description
 * # audioPlayer
 */

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

Dropzone.autoDiscover = false;

angular.module('lightsApp')
  .directive('audioPlayer', function ($window, com) {
    return {
      template: '<div><form class="dropzone" id="audio-dropzone"></form><p>{{filename}}</p></div>',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {



         /* Test audio api */
      /* http://www.smartjava.org/examples/webaudio/example3.html */

    // create the audio context (chrome only for now)
    if (! $window.AudioContext) {
        if (! $window.webkitAudioContext) {
            $window.alert('no audiocontext found');
            return;
        }
        window.AudioContext = window.webkitAudioContext;
    }
    var myDropzone = new $window.Dropzone(element.find('form')[0], {
        url: "/file/post",
        parallelUploads: 1,
        dictDefaultMessage: 'Drop file to play or click and browse..',
        acceptedFiles: '.mp3,.ogg,.mp4,.webm,.m4a',
        accept: function(file) {

            if(javascriptNode){
                removeAudioNodes();
            }
            setupAudioNodes(URL.createObjectURL(file));
            scope.$apply(function(){
                scope.filename = file.name;
            });
            myDropzone.removeFile(file);
        }

    });
    myDropzone.on("error", function(file) {
        myDropzone.removeFile(file);
    });

    var context = new $window.AudioContext();
    var sourceNode;
    var analyser;
    var javascriptNode;

    function setupAudioNodes(src) {

        // setup a javascript node
        javascriptNode = context.createScriptProcessor(2048, 1, 1);
        // connect to destination, else it isn't called
        javascriptNode.connect(context.destination);
        // when the javascript node is called
        // we use information from the analyzer node
        // to draw the volume
        javascriptNode.onaudioprocess = function() {

            // get the average for the first channel
            var array =  new Uint8Array(analyser.frequencyBinCount);
            analyser.getByteFrequencyData(array);

            drawSpectrum(array);

        };

        // setup a analyzer
        analyser = context.createAnalyser();
        analyser.smoothingTimeConstant = 0.3;
        analyser.fftSize = Math.max(32, Math.pow( 2, Math.ceil( Math.log( com.config.MATRIX_WIDTH * 2 ) / Math.log( 2 ) ) ));


        var audio = document.createElement('audio');
        audio.setAttribute('src', src);
        audio.setAttribute('controls', '');
        audio.setAttribute('crossorigin', 'anonymous');
        element[0].appendChild(audio);
        sourceNode = context.createMediaElementSource(audio);


        // create a buffer source node
        //sourceNode = context.createBufferSource();

        sourceNode.onended = removeAudioNodes;
        sourceNode.connect(analyser);
        analyser.connect(javascriptNode);
        sourceNode.connect(context.destination);
        sourceNode.mediaElement.play();
    }

    function removeAudioNodes(){
        javascriptNode.disconnect(context.destination);
        analyser.disconnect(javascriptNode);
        sourceNode.disconnect(context.destination);
        sourceNode.mediaElement.pause();
        sourceNode.mediaElement.remove();
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
        };
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


    function drawSpectrum(array) {
        var data = [];
        for ( var x = 0; x < (array.length); x++ ){
            var value = array[x];
            var bucket = Math.floor(value / 255 * com.config.MATRIX_HEIGHT);
            var col = [];
            data.push(col);
            for(var y=0; y < com.config.MATRIX_HEIGHT; y++){
                var color = '#000000';
                if (y < bucket){
                    //TODO move color to cache
                    color = makeGradientColor({r:255,g:0,b:0}, {r:255,g:255,b:0}, y/20);
                }
                col[com.config.MATRIX_HEIGHT-1 - y] = color;
            }
        }
        com.send(JSON.stringify({
            'type': 'action',
            'action': 'draw_matrix',
            'params': {'data': data}
        }));
    }


    element.on('$destroy', function() {
        // Do cleanup work
        removeAudioNodes();
    });


      }
    };
  });
