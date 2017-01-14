from umqtt.simple import MQTTClient
from config import MQTT_BROKER
import time
import json
import uos
import math

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
  t = time.localtime()
  s = t[5]
  m = t[4]
  h = int((t[3] + 1) % 12)
  r = s % 2.5

  sf.paint(off)

  # hours
  segments = [[], [100, 101], [102, 103],
              [126, 127], [128, 129],
              [152, 153], [154, 155],
              [22, 23],    [24, 25],
              [48, 49],   [50, 51],
              [74, 75], [76, 77]]

  [setPixelsColor(segments[i], wheel(255/12.0 * ((i+6) % 12))) for i in range(h+1)]

  # minutes
  m10 = int(m % 10)
  m6 = int((int(m/10) + 3) % 6)
  if m10 == 0:
    sf.trees[m6].trunk.paint(w)
  else:
    segments = [[],[0,21],[1,20],[14,19],[15,18],[16,17],[30,31],[29,32],[28,33],[34,39]]
    [setPixelsColor(map(lambda x: ( m6 * 26 + x ) % 156, segments[i]),  wheel(255 / 6.0 * m6)) for i in range(m10+1)]

  # secondes
  led = math.ceil(s/2.5)
  if led >= 24:
    led = 0
  if r == 0:
    color = 128
  else:
    color = int(r/2.5 * 128)

  [setPixelColor(((i + 12) % 24) + 156, [int(x/2) for x in wheel(255 / 24.0 * ((i+12) % 24))]) for i in range(led)]
  setPixelColor(((led + 12) % 24) + 156, Color(color, color, color))
  show()
  wait(200)

main()
