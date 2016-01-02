# MOCK version for testing
# Adafruit NeoPixel library port to the rpi_ws281x library.
# Author: Tony DiCola (tony@tonydicola.com), Jeremy Garff (jer@jers.net)

def Color(red, green, blue):
  """Convert the provided red, green, blue color to a 24-bit color value.
  Each color component should be a value 0-255 where 0 is the lowest intensity
  and 255 is the highest intensity.
  """
  return (red << 16) | (green << 8) | blue


class Adafruit_NeoPixel(object):
  def __init__(self, num, pin, freq_hz=800000, dma=5, invert=False, brightness=255, channel=0):
    """Class to represent a NeoPixel/WS281x LED display.  Num should be the
    number of pixels in the display, and pin should be the GPIO pin connected
    to the display signal line (must be a PWM pin like 18!).  Optional
    parameters are freq, the frequency of the display signal in hertz (default
    800khz), dma, the DMA channel to use (default 5), invert, a boolean
    specifying if the signal line should be inverted (default False), and
    channel, the PWM channel to use (defaults to 0).
    """
    # Create ws2811_t structure and fill in parameters.
    self._num = num

    # Grab the led data array.
    self._led_data = [0] * num

  def __del__(self):
    pass

  def begin(self):
    """Initialize library, must be called once before other functions are
    called.
    """
    pass

  def show(self):
    """Update the display with the data from the LED buffer."""
    pass

  def setPixelColor(self, n, color):
    """Set LED at position n to the provided 24-bit color value (in RGB order).
    """
    if( n < self._num):
      self._led_data[n] = color

  def setPixelColorRGB(self, n, red, green, blue):
    """Set LED at position n to the provided red, green, and blue color.
    Each color component should be a value from 0 to 255 (where 0 is the
    lowest intensity and 255 is the highest intensity).
    """
    self.setPixelColor(n, Color(red, green, blue))

  def setBrightness(self, brightness):
    """Scale each LED in the buffer by the provided brightness.  A brightness
    of 0 is the darkest and 255 is the brightest.
    """
    pass

  def getPixels(self):
    """Return an object which allows access to the LED display data as if
    it were a sequence of 24-bit RGB values.
    """
    return self._led_data

  def numPixels(self):
    """Return the number of pixels in the display."""
    return self._num

  def getPixelColor(self, n):
    """Get the 24-bit RGB color value for the LED at position n."""
    return self._led_data[n]
