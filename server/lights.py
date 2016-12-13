# -*- coding: utf-8 -*-
import time
import random
import abc
from neopixel import *

# LED strip configuration:

LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
MATRIX_HEIGHT = 20
MATRIX_WIDTH = 14
LED_COUNT = MATRIX_HEIGHT * MATRIX_WIDTH # Number of LED pixels.

ALPHA_NUM = {
    u' ': [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0]],
    u':': [[0],[0],[0],[0],[1],[1],[1],[1],[0],[0],[0],[0],[1],[1],[1],[1],[0],[0],[0],[0]],
    u'.': [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[1],[1],[1],[1]],
    u'?': [[0,1,0],[0,1,0],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[0,0,1],[0,0,1],[0,0,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,0,0],[0,0,0],[0,0,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
    u'&': [[0,0,0],[0,1,0],[0,1,0],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,0],[0,1,0],[0,1,0],[1,1,1],[1,0,1],[1,0,1],[1,0,0],[1,1,0],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[0,1,1]],
    u'_': [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'-': [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    u'=': [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    u'+': [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    u'°': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    u'/': [[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0]],
    u'\\': [[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1]],
    u'>': [[1,0,0],[1,0,0],[1,0,0],[1,0,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0]],
    u'<': [[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,0,1],[0,0,1],[0,0,1],[0,0,1]],
    u'!': [[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[0],[0],[0],[0],[1],[1],[1],[1]],
    u'$':[[0,1,0],[0,1,0],[1,1,1],[1,1,1],[1,0,1],[1,0,0],[1,0,0],[1,0,0],[1,1,0],[1,1,1],[0,1,1],[0,1,1],[0,0,1],[0,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[0,1,0],[0,1,0]],
    u'#': [[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,1,1,0],[0,1,1,0],[0,1,1,0],[0,1,1,0]],
    u'%': [[1,1,0,0],[1,1,0,0],[1,1,0,1],[1,1,0,1],[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,1,1,0],[0,1,1,0],[0,1,0,0],[0,1,0,0],[0,1,0,0],[1,1,0,0],[1,0,0,0],[1,0,1,1],[1,0,1,1],[0,0,1,1],[0,0,1,1]],
    u'*': [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    u'0': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'1': [[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]],
    u'2': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,1,1],[0,0,1],[0,0,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1],[1,1,1],[1,1,0],[1,1,0],[1,0,0],[1,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'3': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'4': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1]],
    u'5': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'6': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'7': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1]],
    u'8': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'9': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1]],
    u'A': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1]],
    u'B': [[1,1,0],[1,1,0],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,0],[1,1,0]],
    u'C': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'D': [[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,0],[1,1,0],[1,1,0],[1,1,0]],
    u'E': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'F': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0]],
    u'G': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'H': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1]],
    u'I': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'J': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[1,1,0],[1,1,0],[1,1,0],[1,1,0]],
    u'K': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,0,1],[1,0,1],[1,0,1],[1,0,1]],
    u'L': [[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'M': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1]],
    u'N': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1]],
    u'O': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'P': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0]],
    u'Q': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,1],[0,0,1]],
    u'R': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,0,1],[1,0,1],[1,0,1],[1,0,1]],
    u'S': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'T': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
    u'U': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]],
    u'V': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
    u'W': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1]],
    u'X': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1]],
    u'Y': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
    u'Z': [[1,1,1],[1,1,1],[1,1,1],[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1],[1,1,1],[1,1,1],[1,1,1]]
    }

ALPHA_NUM['|'] = ALPHA_NUM['1']
ALPHA_NUM[';'] = ALPHA_NUM[':']
ALPHA_NUM[','] = ALPHA_NUM['.']
listeners = []

LOCAL_LED_CACHE = [0] * LED_COUNT

def show():
    strip.show()
    # notify listeners
    for l in listeners:
        l(LOCAL_LED_CACHE)


def setPixelColor(i, color):
    if i > -1 and i < LED_COUNT:
      LOCAL_LED_CACHE[i] = color
      strip.setPixelColor(i, color)

    # TODO handle error reporting to detect wrong Anim


def setPixelColorRGB(i, r, g, b):
    setPixelColor(i, Color(r, g, b))

def register_listener(listener):
    listeners.append(listener)


def init_strip():
    # Create NeoPixel object with appropriate configuration.
    s = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    s.begin()
    return s

strip = init_strip()


def clear():
  colorAll(Color(0,0,0))


def colorAll(color):
    for i in range(LED_COUNT):
        setPixelColor(i, color)


def rect(x, y, w, h, fill_color=None, border_size=0, border_color=None):
    for i in range(0, w):
        for j in range(0, h):
            color = fill_color
            if border_size and (i < border_size or i > w - border_size - 1 or j < border_size or j > h - border_size - 1):
                color = border_color
            if color:
                drawPixel(x + i, y + j, color)
    show()


def drawText(x, text, color):
    text = text.upper()
    for c in range(0, len(text)):
        a = ALPHA_NUM.get(text[c], ALPHA_NUM['?'])
        drawObj(x, 0, a, color)
        x = x + len(a[0]) + 1


def drawObj(x, y, obj, color):
    for i in range(0, len(obj[0])):
        for j in range(0, len(obj)):
            if (i + x) >= 0 and (j + y) >=0:
                drawPixel((i + x), (j + y), color if obj[j][i] == 1 else Color(0,0,0))

def xyToPosition(x, y):
    return x * MATRIX_HEIGHT + (y if x % 2 != 0 else MATRIX_HEIGHT - y - 1)

def drawPixel(x, y, color):
    setPixelColor(xyToPosition(x, y), color)


def getPixel(x, y):
    return LOCAL_LED_CACHE[xyToPosition(x, y)]

# Define functions which animate LEDs in various ways.
def colorWipe(color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(LED_COUNT):
                setPixelColor(i, color)
                show()
                time.sleep(wait_ms/1000.0)

def theaterChase(color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
                for q in range(3):
                        for i in range(0, LED_COUNT, 3):
                                setPixelColor(i+q, color)
                        show()
                        time.sleep(wait_ms/1000.0)
                        for i in range(0, LED_COUNT, 3):
                                setPixelColor(i+q, 0)

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


def rainbowCycle(wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
                for i in range(LED_COUNT):
                        setPixelColor(i, wheel(((i * 256 / LED_COUNT) + j) & 255))
                show()
                time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
                for q in range(3):
                        for i in range(0, LED_COUNT, 3):
                                setPixelColor(i+q, wheel((i+j) % 255))
                        show()
                        time.sleep(wait_ms/1000.0)
                        for i in range(0, LED_COUNT, 3):
                                setPixelColor(i+q, 0)


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class BaseAnim(object):
    def __init__(self, client_id, kwargs):
        self.isRunning = False
        self.kwargs = kwargs
        self.owner_id = client_id

    def start(self):
        self.isRunning = True
        self._anim()
        self.stop()

    def stop(self):
        self.isRunning = False

    def client_disconnected(self, client_id):
        pass

    @abc.abstractmethod
    def _anim(self):
        """Do animation until isRunning is False or anim ended"""
        return


class RectTestAnim(BaseAnim):
    def _anim(self):
        while self.isRunning:
            clear()
            rect(1, 1, 8, 10, Color(255,0,0))
            time.sleep(500/1000.0)
            clear()
            rect(1, 1, 8, 10, Color(255,0,0), 1, Color(0,255,0))
            time.sleep(500/1000.0)
            clear()
            rect(1, 1, 8, 10, Color(255,0,0), 3, Color(0,255,0))
            time.sleep(500/1000.0)
            clear()
            rect(1, 1, 8, 10, None, 3, Color(0,255,0))
            time.sleep(500/1000.0)
            clear()
            rect(0, 0, 13, 19, Color(255,0,0), 1, Color(0,255,0))
            time.sleep(500/1000.0)


class CountdownAnim(BaseAnim):

    def _anim(self):
        n =  self.kwargs.get('n', 10)
        while n > 0 and self.isRunning:
            colorAll(Color(0,0,0))
            drawText(6, str(n), Color(255,0,0))
            show()
            time.sleep(500 / 1000.0)
            theaterChase(Color(0,0,255), 10, 1)
            n = n - 1


class TestAnim(BaseAnim):

    def _anim(self):
        while self.isRunning:
            # Color wipe animations.
            colorWipe(Color(255, 0, 0))  # Red wipe
            colorWipe(Color(0, 255, 0))  # Blue wipe
            colorWipe(Color(0, 0, 255))  # Green wipe
            # Theater chase animations.
            theaterChase(Color(127, 127, 127))  # White theater chase
            theaterChase(Color(127,   0,   0))  # Red theater chase
            theaterChase(Color(  0,   0, 127))  # Blue theater chase
            # Rainbow animations.
            rainbow()
            rainbowCycle()
            theaterChaseRainbow()


class WaterDrop:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.stopped = False

    def move(self):
        if self.stopped:
            return
        ## need refactoring
        #hide
        drawPixel(self.x, self.y, Color(0, 0, 0))
        if getPixel(self.x, self.y + 1) == Color(0, 0, 0):
            self.y += 1
            if self.y == MATRIX_HEIGHT - 1:
                self.stopped = True
        else:
            #find empty pixel
            range_left = 1
            range_right = 1
            while not self.stopped:
                if self.x - range_left < 0 and self.x + range_right >= MATRIX_WIDTH:
                    self.stopped = True
                else:
                    if self.x - range_left >= 0:
                        if getPixel(self.x - range_left, self.y + 1) == Color(0, 0, 0):
                            self.y += 1
                            self.x -= range_left
                            self.stopped = True
                        else:
                            range_left += 1

                    if self.x + range_right < MATRIX_WIDTH:
                        if getPixel(self.x + range_right, self.y + 1) == Color(0, 0, 0):
                            self.y += 1
                            self.x += range_right
                            self.stopped = True
                        else:
                            range_right += 1
        drawPixel(self.x, self.y, self.color)


class WaterAnim(BaseAnim):
    def _anim(self):
        clear()
        self._drops = []
        i = 0
        while self.isRunning:
            if i == 4:
                self._drops.append(WaterDrop(10, 0, Color(0, 255, 0)))
                self._drops.append(WaterDrop(3, 0, Color(0, 0, 255)))
                i = 0

            [b.move() for b in self._drops]
            show()
            time.sleep(20/1000.0)
            i += 1


class BallUpDown:
    def __init__(self, n, v, color):
          self.n = n
          self.color = color
          self.v = v
          self.loop = 0

    def hide(self):
        setPixelColor(self.n, Color(0, 0, 0))

    def move(self):
        if(self.n < 0 and self.v < 0):
            self.v = 1
            self.loop +=1
        if(self.n > LED_COUNT and self.v > 0):
            self.v = -1

        self.n = self.n + self.v
        setPixelColor(self.n, self.color)


class UpDownAnim(BaseAnim):
    def _anim(self):
        clear()
        self._balls = [
              ]
        i = 0
        while self.isRunning:
            if i == 4:
                 self._balls.append(BallUpDown(0, 1,  Color(random.randint(10, 255),
                                            random.randint(10, 255),
                                            random.randint(10, 255))))
                 i = 0
            [self._balls.remove(b) for b in self._balls if b.loop == 1]
            [b.hide() for b in self._balls]
            [b.move() for b in self._balls]
            show()
            time.sleep(50/1000.0)
            i += 1


class ScrollTextAnim(BaseAnim):

    def _anim(self):
        text = self.kwargs.get('text', '0000')
        hex_color = self.kwargs.get('color', '#FF0000')
        color = Color(*hex_to_rgb(hex_color))
        loop = self.kwargs.get('loop', 1)
        scrolli = MATRIX_WIDTH
        text_length = reduce(lambda t, c: t + len(ALPHA_NUM.get(c, ALPHA_NUM['?'])[0]), text, 0)
        while self.isRunning and (loop == -1 or loop > 0):
            colorAll(Color(0,0,0))
            drawText(scrolli, text, color)
            show()
            time.sleep(500 / 1000.0)
            if scrolli < -text_length:
                loop -= 1
                scrolli = MATRIX_WIDTH
            else:
                scrolli -= 1

import datetime

class TimeAnim(BaseAnim):

    def _anim(self):
        scrolli = MATRIX_WIDTH
        text_length = reduce(lambda t, c: t + len(ALPHA_NUM.get(c, ALPHA_NUM['?'])[0]), '00:00', 0)
        while self.isRunning:
            today = datetime.datetime.now()
            clear()
            drawText(scrolli, today.strftime("%H:%M"), Color(0,255,0))
            show()
            time.sleep(500 / 1000.0)
            if scrolli < -text_length:
                scrolli = MATRIX_WIDTH
            else:
                scrolli -= 1


class SensorAnim(BaseAnim):

    def _anim(self):
        lastUpdate = 0
        while self.isRunning:
            data = None
            if time.time() - lastUpdate > 900:
                data = get_sensorist_data()
            a = ScrollTextAnim(self.owner_id, {'text': u'T: %s°C  H: %s%%' % data})
            a.start()


import urllib2, json, os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def get_sensorist_data():
    request = urllib2.Request("https://api.sensorist.com/v1/measurements?data_sources=15282,15283&type=latest")
    request.add_header("Authorization", "Basic %s" % os.environ.get("SENSORIST_AUTH"))
    result = urllib2.urlopen(request)
    j = json.load(result.fp)
    return (j["measurements"]["15282"]["value"], j["measurements"]["15283"]["value"])


class Ball:
    def __init__(self, x, y, vx, vy, color):
          self.x = x
          self.y = y
          self.vx = vx
          self.vy = vy
          self.color = color

    def hide(self):
        drawPixel(self.x, self.y, Color(0, 0, 0))

    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        if self.x > MATRIX_WIDTH - (2 + abs(self.vx)) or self.x < 1 + abs(self.vx):
            self.vx = -self.vx

        if self.y > MATRIX_HEIGHT - (2 + abs(self.vy)) or self.y < 1 + abs(self.vy):
            self.vy = -self.vy
        #show
        drawPixel(self.x, self.y, self.color)


class BallAnim(BaseAnim):

    def _anim(self):
        clear()
        rect(0, 0, MATRIX_WIDTH, MATRIX_HEIGHT, Color(0, 0, 0), 1, Color(255, 0, 0))

        self._balls = [
            Ball(7, 10 , 1, 1, Color(0, 255, 0)),
            Ball(8, 10 , 1, -1, Color(0, 0, 255))
          ]

        while self.isRunning:
            [b.hide() for b in self._balls]
            [b.move() for b in self._balls]
            show()
            time.sleep(200/1000.0)

    def launch_random(self, client_id, kwargs):
        self._balls.append(Ball(random.randint(1, MATRIX_WIDTH - 2),
                                random.randint(1, MATRIX_HEIGHT - 2),
                                1, 1, Color(random.randint(10, 255),
                                            random.randint(10, 255),
                                            random.randint(10, 255))))

    def launch_at(self, client_id, kwargs):
        # TODO check x, y limits
        self._balls.append(Ball(kwargs['x'],
                                kwargs['y'],
                                -1, -1, Color(random.randint(10, 255),
                                            random.randint(10, 255),
                                            random.randint(10, 255))))

class DrawboardAnim(BaseAnim):
    def _anim(self):
        clear()
        while self.isRunning:
            show()
            time.sleep(500/1000.0)

    def draw_at(self, client_id, kwargs):
        # TODO check x, y limits
        hex_color = kwargs.get('color', '#FF0000')
        color = Color(*hex_to_rgb(hex_color))
        drawPixel(kwargs['x'], kwargs['y'], color)


class ColorTestAnim(BaseAnim):
    r = 255
    g = 255
    b = 255
    fade = True
    fadeLevel = 1
    fadeIn = True
    speed = 30
    step = 10
    def _anim(self):
        clear()
        while self.isRunning:
            color = Color(self.r, self.g, self.b)
            if self.fade:
                if self.fadeIn:
                    self.fadeLevel = self.fadeLevel * max(1.1, self.step / 10)
                    if self.fadeLevel > 255:
                        self.fadeLevel = 256
                        self.fadeIn = False
                else:
                    self.fadeLevel = self.fadeLevel / max(1.1, self.step / 10)
                    if self.fadeLevel < 1:
                        self.fadeLevel = 1
                        self.fadeIn = True
                ratio = self.fadeLevel / 256.0
                color = Color(int(self.r * ratio), int(self.g * ratio), int(self.b * ratio))
            colorAll( color )
            show()
            time.sleep(self.speed/1000.0)

    def draw(self, client_id, kwargs):
        hex_color = kwargs.get('color', '#FFFFFF')
        self.speed  = kwargs.get('speed', 30)
        self.step  = kwargs.get('step', 10)
        self.fade  = bool(kwargs.get('fade', 1))
        self.r, self.g, self.b = hex_to_rgb(hex_color)


class Trail(object):
    def __init__(self, start, stop, color, length=10):
        self.trail = []
        self.start = start
        self.stop = stop
        self.r, self.g, self.b = color
        self.length = length

    def update(self):
        if len(self.trail) > 0:
            pos = self.trail[-1]
            if self.start > self.stop:
                if pos > self.stop - self.length:
                    self.trail.append(pos - 1)
                if len(self.trail) > self.length or pos < self.stop:
                    self.trail.pop(0)
            else:
                if pos < self.stop + self.length:
                    self.trail.append(pos + 1)
                if len(self.trail) > self.length or pos > self.stop:
                    self.trail.pop(0)
            self.render()
        else:
            # TODO: variable start height?
            if random.randint(0, 100) > 70:
                self.trail.append(self.start)

    def render(self):
        for idx, pos in enumerate(reversed(self.trail)):
            ratio =  min(1, max(0, (self.length -1.0 -idx) / (self.length -1.0) * 1.2 ))
            color = Color(int(self.r * ratio), int(self.g * ratio), int(self.b * ratio))
            if self.start < self.stop and pos <= self.stop:
                setPixelColor(pos, color)
            if self.stop < self.start and pos >= self.stop:
                setPixelColor(pos, color)



class RainAnim(BaseAnim):
    def _anim(self):
        clear()
        trails = [Trail(start * MATRIX_HEIGHT, start*MATRIX_HEIGHT + MATRIX_HEIGHT-1, (255, 255, 255)) if start % 2 == 1 else Trail(start * MATRIX_HEIGHT + MATRIX_HEIGHT-1, start*MATRIX_HEIGHT, (255, 255, 255)) for start in range(MATRIX_WIDTH)]
        while self.isRunning:
            [t.update() for t in trails]
            show()
            time.sleep(100 / 1000.0)



class SnowflakeAnim(BaseAnim):
    def _anim(self):
        clear()
        from snowflake import Snowflake
        sf = Snowflake(0)
        sf.test()



class AudioAnim(BaseAnim):
    def _anim(self):
        clear()
        show()
        while self.isRunning:
            time.sleep(500/1000.0)

    def client_disconnected(self, client_id):
        # Since only owner can stream we stop
        if self.owner_id == client_id:
            self.stop()

    def draw_matrix(self, client_id, kwargs):
        if client_id != self.owner_id:
            return
        clear()
        for x in range(0, MATRIX_WIDTH):
            for y in range(0, MATRIX_HEIGHT):
                drawPixel(x, y, Color(*hex_to_rgb(kwargs['data'][x][y])))
        show()

# https://github.com/bbx10/artnet-unicorn-hat/blob/master/artnet-server.py
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class ArtNet(DatagramProtocol):
    def __init__(self):
        self.render = False

    def datagramReceived(self, data, host, port):
        if self.render and ((len(data) > 18) and (data[0:8] == "Art-Net\x00")):
            rawbytes = map(ord, data)
            opcode = rawbytes[8] + (rawbytes[9] << 8)
            protocolVersion = (rawbytes[10] << 8) + rawbytes[11]
            if ((opcode == 0x5000) and (protocolVersion >= 14)):
                sequence = rawbytes[12]
                physical = rawbytes[13]
                sub_net = (rawbytes[14] & 0xF0) >> 4
                universe = rawbytes[14] & 0x0F
                net = rawbytes[15]
                rgb_length = (rawbytes[16] << 8) + rawbytes[17]
                # print "seq %d phy %d sub_net %d uni %d net %d len %d" % (sequence, physical, sub_net, universe, net, rgb_length)
                idx = 18
                x = (universe - 1) * 140
                while idx < 140*3 + 18:
                    r = rawbytes[idx]
                    idx += 1
                    g = rawbytes[idx]
                    idx += 1
                    b = rawbytes[idx]
                    idx += 1
                    setPixelColorRGB(x, r, g, b)
                    x += 1
                show()


import threading


class GlediatorAnim(BaseAnim):

    artNet = ArtNet()

    @staticmethod
    def start_reactor():
        reactor.listenUDP(6454, GlediatorAnim.artNet)
        reactor.run(installSignalHandlers=0)


    def _anim(self):
        if not reactor.running:
            thread = threading.Thread(target=GlediatorAnim.start_reactor)
            thread.daemon = True
            thread.start()
        GlediatorAnim.artNet.render = True
        while self.isRunning:
            time.sleep(50/1000.0)
        GlediatorAnim.artNet.render = False


# Main program logic follows:
if __name__ == '__main__':
    print 'Press Ctrl-C to quit.'
    anim = TestAnim()
    anim.start()


