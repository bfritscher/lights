from umqtt.simple import MQTTClient
from config import MQTT_BROKER
import time
import json
import machine

from snowflake_esp import *
sf = Snowflake(0)
sf.test()

w = Color(255, 255, 255)
off = Color(0, 0, 0)

animation = "sf.color(w)"

def sub_cb(topic, msg):
    global animation
    try:
        animation = msg
        print((topic, msg))
    except:
        pass




def play_animation():
    global animation
    try:
        exec(animation, globals(), locals())
    except Exception as e:
        print(e)
        animation = "sf.color(Color(255, 0, 0))"
    time.sleep(500/1000.0)


def main():
    c = MQTTClient("umqtt_client", MQTT_BROKER)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(b"lights/snowflake")
    while True:
            c.check_msg()
            play_animation()

    c.disconnect()

main()
