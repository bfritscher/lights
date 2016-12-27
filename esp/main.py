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

animation = "sf.color(w)"

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

main()
