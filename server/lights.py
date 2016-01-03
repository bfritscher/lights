# -*- coding: utf-8 -*-
import time
import random
import abc
from neopixel import *

# LED strip configuration:
LED_COUNT = 280      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
MATRIX_HEIGHT = 20
MATRIX_WIDTH = 14


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


def show():
    strip.show()
    # notify listeners
    for l in listeners:
        l(strip.getPixels())


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
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)


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

def drawPixel(x, y, color):
    strip.setPixelColor(x * MATRIX_HEIGHT + (y if x % 2 != 0 else MATRIX_HEIGHT - y - 1), color)


# Define functions which animate LEDs in various ways.
def colorWipe(color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
                show()
                time.sleep(wait_ms/1000.0)

def theaterChase(color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
                for q in range(3):
                        for i in range(0, strip.numPixels(), 3):
                                strip.setPixelColor(i+q, color)
                        show()
                        time.sleep(wait_ms/1000.0)
                        for i in range(0, strip.numPixels(), 3):
                                strip.setPixelColor(i+q, 0)

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
                for i in range(strip.numPixels()):
                        strip.setPixelColor(i, wheel((i+j) & 255))
                show()
                time.sleep(wait_ms/1000.0)


def rainbowCycle(wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
                for i in range(strip.numPixels()):
                        strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
                show()
                time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
                for q in range(3):
                        for i in range(0, strip.numPixels(), 3):
                                strip.setPixelColor(i+q, wheel((i+j) % 255))
                        show()
                        time.sleep(wait_ms/1000.0)
                        for i in range(0, strip.numPixels(), 3):
                                strip.setPixelColor(i+q, 0)


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class BaseAnim(object):
    def __init__(self, kwargs):
        self.isRunning = False
        self.kwargs = kwargs

    def start(self):
        self.isRunning = True
        self._anim()
        self.stop()

    def stop(self):
        self.isRunning = False

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
            a = ScrollTextAnim({'text': u'T: %s°C  H: %s%%' % data})
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
        rect(0, 0, 14, 20, Color(0, 0, 0), 1, Color(255, 0, 0))

        self._balls = [
            Ball(7, 10 , 1, 1, Color(0, 255, 0)),
            Ball(8, 10 , 1, -1, Color(0, 0, 255))
          ]

        while self.isRunning:
            [b.hide() for b in self._balls]
            [b.move() for b in self._balls]
            show()
            time.sleep(200/1000.0)

    def launch_random(self, kwargs):
        self._balls.append(Ball(random.randint(1, MATRIX_WIDTH - 2),
                                random.randint(1, MATRIX_HEIGHT - 2),
                                1, 1, Color(random.randint(10, 255),
                                            random.randint(10, 255),
                                            random.randint(10, 255))))

    def launch_at(self, kwargs):
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

    def draw_at(self, kwargs):
        # TODO check x, y limits
        hex_color = kwargs.get('color', '#FF0000')
        color = Color(*hex_to_rgb(hex_color))
        drawPixel(kwargs['x'], kwargs['y'], color)



class AudioAnim(BaseAnim):
    def _anim(self):
        clear()
        show()
        while self.isRunning:
            time.sleep(500/1000.0)

    def draw_matrix(self, kwargs):
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

    def datagramReceived(self, data, (host, port)):
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
                    strip.setPixelColorRGB(x, r, g, b)
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

