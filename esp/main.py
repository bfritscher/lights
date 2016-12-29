from umqtt.simple import MQTTClient
from config import MQTT_BROKER
import time
import json
import machine
import uos

from snowflake_esp import *
sf = Snowflake(0)
sf.test()

w = Color(255, 255, 255)
off = Color(0, 0, 0)

def wait(ms):
   time.sleep(ms/1000.0)

def randint(min, max):
    return min + int(int.from_bytes(uos.urandom(2)) / 65536.0 * (max - min + 1))

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def fade(start_color, stop_color, steps, current_step):
    dr = (start_color[0] - stop_color[0]) / float(steps)
    dg = (start_color[1] - stop_color[1]) / float(steps)
    db = (start_color[2] - stop_color[2]) / float(steps)
    return Color(start_color[0] - (dr * current_step), start_color[1] - (dg * current_step), start_color[2] - (db * current_step))

animation = ""

def sub_cb(topic, msg):
    global animation
    try:
        animation = json.loads(msg)
        print((topic, msg))
    except:
        pass


last_anim = time.ticks_ms()

c = MQTTClient("umqtt_client", MQTT_BROKER)
c.set_callback(sub_cb)


def play_animation():
    global animation, last_anim
    try:
        if animation == "":
            default_animation()
        else:
            exec(animation, globals(), locals())

    except Exception as e:
        print(e)
        c.publish(b"lights/snowflake/error", b"%s" % json.dumps(e))
        animation = "sf.color(Color(255, 0, 0))"
    delta = time.ticks_ms() - last_anim
    if delta < 500:
        time.sleep((500 - delta) / 1000.0)
    last_anim = time.ticks_ms()

def main():
    c.connect()
    c.subscribe(b"lights/snowflake")
    while True:
            c.check_msg()
            play_animation()

    c.disconnect()


def default_animation():
  # on/off snake + wheel trunk and leaf
  sf.paint(off)
  for i in range(156):
    setPixelColor(i, w)
    show()
    wait(20)

  for i in range(180):
    setPixelColor(i, off)
    show()
    wait(20)
    if i > 0 and i % 22 == 0:
      sf.trees[int((i-22)/26)].trunk.bottom.paint(w)
    if i > 0 and i % 23 == 0:
      sf.trees[int((i-23)/26)].trunk.top.paint(w)

  for i in range(6):
    sf.trees[i].leaf.left.color(w)
    sf.trees[i].leaf.right.color(w)

  for i in range(6):
    sf.trees[i].leaf.left.color(off)
    sf.trees[i].leaf.right.color(off)

  for i in range(6):
    sf.trees[i].trunk.color(off)

  sf.star.color(w)
  wait(1000)
  sf.star.color(off)

  # big and small star with snowflake transition
  for i in range(4):
    y = Color(255, 220, 0)
    sf.paint(off)
    sf.star.color(y)
    wait(1000)

    sf.star.paint(off)
    sf.trees.color(w)
    wait(1000)

    sf.trees.trunk.paint(off)
    sf.trees.leaf.color(y)
    wait(1000)

  # rotate trunk fade
  for i in range(4):
    sf.star.paint(w)
    for i in range(6):
        sf.trees[i].trunk.paint(w)
        sf.trees[i-1 % 6].trunk.paint(fade(w, off, 3, 1))
        sf.trees[i-2 % 6].trunk.paint(fade(w, off, 3, 2))
        sf.trees[i-3 % 6].trunk.paint(fade(w, off, 3, 3))
        show()
        wait(100)

  # color start expand out
  sf.color(off)
  def setPixelsColor(leds, color):
    [setPixelColor(i, color) for i in leds]

  def setTreesPixelsColor(leds, color):
    [setPixelsColor(map(lambda x: i * 26 + x , leds), w) for i in range(6)]
    show()
    wait(100)


  def star(color):
    sf.star.color(color)
    setTreesPixelsColor([0,21], w)
    setTreesPixelsColor([1,20], w)
    setTreesPixelsColor([2,7,13,8,14,19], w)
    setTreesPixelsColor([3,6,9,12,15,18], w)
    setTreesPixelsColor([4,5,10,11,16,17], w)
    wait(1000)
    sf.trees.color(off)

  for i in range(3):
    star(Color(255,220,0))
    star(Color(255,0,0))
    star(Color(0,255,0))

  # Fade Red/Green/Blue

  sf.color(Color(0,0,255))
  for i in range(21):
      sf.color(fade(Color(0,0,255), Color(0,255,0), 20, i))

  sf.color(Color(0,255,0))
  for i in range(21):
    sf.color(fade(Color(0,255,0), Color(255,0,0), 20, i))

  sf.color(Color(255,0,0))
  for i in range(21):
    sf.color(fade(Color(255,0,0), Color(0,0,255), 20, i))


  # red green snake folowing rotating
  for i in range(156):
    setPixelColor(i, Color(255, 0, 0))
    setPixelColor((78+i) % 156, Color(0, 255, 0))
    setPixelColor(i % 24 + 156, Color(255, 255, 0 ))
    setPixelColor((12 +i) % 24 + 156, Color(0, 0, 0))

    wait(70)
    show()


  # red green alternate blinking lighter colors
  colors = [Color(198, 0, 0), Color(50, 168, 0)]
  for n in range(20):
    for i in range(180):
      setPixelColor(i, colors[i%2])
    show()
    colors = list(reversed(colors))
    wait(250)


  # rainbow snake

  sf.color(off)
  for i in range(156):
    setPixelColor(i, wheel(255 / 156.0 * i))
    wait(30)
    show()

  wait(200)
  sf.star.inner.color(Color(255, 255, 255))
  wait(2000)

  # spin colored trees
  sf.paint(off)
  sf.star.paint(Color(100,100,100))
  for n in range(10):
    for i in range(6):
      sf.trees[i-1].paint(off)
      sf.trees[i].paint(wheel(255/6.0*i))
      show()
      wait(80)

main()
