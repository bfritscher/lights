'use strict';

angular.module('lightsApp')
  .directive('snowflake', function ($rootScope, com) {
    return {
      template: `<svg width="1000px" height="1000px" viewBox="0 0 2000 2000">
        <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur id="gauss" stdDeviation="10 10" result="glow"/>
          <feMerge><feMergeNode in="glow"/><feMergeNode in="glow"/><feMergeNode in="glow"/></feMerge>
        </filter>
      </svg>`,
      replace: true,
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
          const width = 34;
          const height = 116
          const svg = Snap(element[0]);
          let id = 0;
          const leds = [];

          function createLed(node, x, y, id) {
            const g = node.g().attr({
                transform: `translate(${x}, ${y})`
            })
            g.rect(0, 0, width, height).attr({
                class: 'strip'
            })
            g.text(5, 15, String(id));
            leds[id] = g.rect((width - width/2)/2, (height - width/2)/2, width/2, width/2).attr({
                filter: 'url(#glow)'
            });
          }

          function createStrip(node, x, y, length, deg=0, cx=0, cy=0, reverse=false) {
            pattern(node, (g) => {
                var i=0;
                if (reverse) {
                    for(i=length-1; i >= 0; i--) {
                        createLed(g, 0, (length-1-i) * height, id + i);
                    }
                } else {
                    for(i=0; i < length; i++) {
                        createLed(g, 0, i * height, id + i);
                    }
                }
                id += length;
            }, x, y, deg, cx, cy);
          }


         function pattern(node, func, x, y, deg=0, cx=0, cy=0) {
            const g = node.g().attr({
                transform: `translate(${x}, ${y}), rotate(${deg}, ${cx}, ${cy})`
            });
            func(g);
          }




          let x = 1000;
          let y = 1000;
          // debug center point
          //svg.circle(x, y, 10);

          const d = (g) => {
            const x = 0;
            const y = ((5 * height) + 3.8*width) * Math.cos(Snap.rad(60));
            createStrip(g, x, y, 2, 0);
            createStrip(g, x + width + width/2, y + (2 * height) + width, 3, -60, 0, 0);
            createStrip(g, x + width, y + (2 * height) + (2 * width), 3, -60, 0, 0, true);
            createStrip(g, x, y + height*3-width, 3, 0);
            createStrip(g, x - width, y + height*3-width, 3, 0, 0, 0, true);
            createStrip(g, x - 2*width, y + (2 * height) + (2 * width), 3, 60, width, 0);
            createStrip(g, x - 2.5*width, y + (2 * height) + width, 3, 60, width, 0, true);
            createStrip(g, x - width, y, 2, 0, 0, 0, true);
            createStrip(g, x - 2*width, y, 2, 60, width, 0);
            createStrip(g, x - 2*height - 0.8*width, y + 2*height * Math.cos(Snap.rad(60)) -0.8*width, 2, 180);
          };

          pattern(svg, d, x, y);
          pattern(svg, d, x , y , 60);
          pattern(svg, d, x , y , 120);
          pattern(svg, d, x , y , 180);
          pattern(svg, d, x , y , 240);
          pattern(svg, d, x , y , 300);


          const b = (g) => {
            const x = ((2 * height) + width/2) * Math.sin(Snap.rad(60));
            const y = ((2 * height) + 2*width) * Math.cos(Snap.rad(60));
            createStrip(g, x, y, 2, 0);
            createStrip(g, x , y + (2 * height), 2, 120);
          };
          pattern(svg, b, x , y , 60);
          pattern(svg, b, x , y , 120);
          pattern(svg, b, x , y , 180);
          pattern(svg, b, x , y , 240);
          pattern(svg, b, x , y , 300);
          pattern(svg, b, x, y);



        element.on('$destroy', function() {

        });

        $rootScope.$on('ledata', (event, data) => {
            data.forEach((val, index) => {
                if (index < leds.length) {
                    leds[index].attr({
                        fill: RGBToHex.apply(this, intToRGB(val))
                    });
                }
            })
        });


      }
    };
  });
