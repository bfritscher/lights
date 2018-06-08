from umqtt.simple import MQTTClient
from config import MQTT_BROKER
import time
import json
import uos
import math
import machine, neopixel

LED_COUNT = 10
r = 99
g = 31
b = 6

np = neopixel.NeoPixel(machine.Pin(4), LED_COUNT)

def c_brightness(c, brightness):
    return max(0, min(c * brightness / 100, 255))

class LED_light(object):
    def __init__(self, pos):
        self.time = 0
        self.pos = pos

    def update(self, delta):
        self.time = self.time - delta
        if self.time <= 0:
            self.random_mode()
            self.random_duration()

    def set_brightness(self, brightness):
        setPixelColor(self.pos, Color(c_brightness(r, brightness), c_brightness(g, brightness), c_brightness(b, brightness)))


    def random_mode(self):
        # Probability Random LED Brightness
        # 50% 77% – 80% (its barely noticeable)
        # 30% 80% – 100% (very noticeable, sim. air flicker)
        # 5% 50% – 80% (very noticeable, blown out flame)
        # 5% 40% – 50% (very noticeable, blown out flame)
        # 10% 30% – 40% (very noticeable, blown out flame)
        brightness = 0
        r = randint(0, 100)
        if r < 50:
            brightness = randint(77, 80)
        elif r < 80:
            brightness = randint(80, 100)
        elif r < 85:
            brightness = randint(50, 80)
        elif r < 90:
            brightness = randint(40, 50)
        else:
            brightness = randint(30, 40)
        self.set_brightness(brightness)


    def random_duration(self):
        # Probability Random Time
        # 90% 20 ms
        #  3% 20 – 30 ms
        #  3% 10 – 20 ms
        #  4% 0 – 10 ms
        r = randint(0, 100)
        if r < 90:
            self.time = 20
        elif r < 93:
            self.time = randint(20, 30)
        elif r < 96:
            self.time = randint(10, 20)
        else:
            self.time = randint(0, 10)

candles = [LED_light(i) for i in range(LED_COUNT)]

def candle():
    start = time.ticks_ms()
    while time.ticks_ms() - start < 2000:
        now = time.ticks_ms()
        [l.update(now) for l in candles]
        show()
        wait(2)

def show():
   np.write()


def Color(r, g, b):
    return (int(r), int(g), int(b))

def setPixelColor(i, color):
    np[i] = color

def setPixelsColor(leds, color):
    [setPixelColor(i, color) for i in leds]

w = Color(255, 255, 255)
off = Color(0, 0, 0)

def wait(ms):
   time.sleep(ms/1000.0)

def randint(min, max):
    return min + int(int.from_bytes(uos.urandom(2), 10) / 65536.0 * (max - min + 1))

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

def rainbow(wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
                for i in range(LED_COUNT):
                        setPixelColor(i, wheel((i+j) & 255))
                show()
                time.sleep(wait_ms/1000.0)

def fade(start_color, stop_color, steps, current_step):
    dr = (start_color[0] - stop_color[0]) / float(steps)
    dg = (start_color[1] - stop_color[1]) / float(steps)
    db = (start_color[2] - stop_color[2]) / float(steps)
    return Color(start_color[0] - (dr * current_step), start_color[1] - (dg * current_step), start_color[2] - (db * current_step))

animation = ""

def sub_cb(topic, msg):
    global animation, r, g, b
    try:
        if msg.startswith(b"rgb,") :
            rgb = msg.split(b",")
            r = int(rgb[1])
            g = int(rgb[2])
            b = int(rgb[3])
        else:
            animation = json.loads(msg)
    except Exception as e:
        print(topic, msg, e)


last_anim = time.ticks_ms()

c = MQTTClient("umqtt_client", MQTT_BROKER)
c.set_callback(sub_cb)


def play_animation():
    global animation, last_anim
    try:
        if animation == "":
            candle()
        else:
            exec(animation, globals(), locals())

    except Exception as e:
        print(e)
        c.publish(b"lights/candle/error", b"%s" % json.dumps(e))
        animation = "setPixelsColor(range(LED_COUNT), Color(255, 0, 0))\nshow()\nwait(300)\nsetPixelsColor(range(LED_COUNT), Color(0, 0, 0))\nshow()\nwait(300)\n"
    delta = time.ticks_ms() - last_anim
    if delta < 500:
        time.sleep((500 - delta) / 1000.0)
    last_anim = time.ticks_ms()

def main():
    c.connect()
    c.subscribe(b"lights/candle")
    while True:
        c.check_msg()
        play_animation()

    c.disconnect()

main()
