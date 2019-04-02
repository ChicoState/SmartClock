import board
import neopixel

class RGB:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def setRed(self, red):
        self.red = red

    def setGreen(self, green):
        self.green = green

    def setBlue(self, blue):
        self.blue = blue

    def getRed(self):
        return self.red

    def getGreen(self):
        return self.green

    def getBlue(self):
        return self.blue

class Lights:
    def __init__(self, color, brightness):
        self.numPixels = 12 #Number of neopixels in the array.
        self.color = color #Color of the Pixels. Accepts an RGB value. So 255, 0, 0 for red.
        self.brightness = brightness #Brightness of the pixels. Max brightness is 3, Min is 0
        self.pixelPin = board.D18
        self.pixelOrder = neopixel.RGB
        self.pixels = neopixel.NeoPixel(self.pixelPin, self.numPixels)
        self.pixels.brightness = self.brightness
        self.pixels.fill((self.color.getRed(), self.color.getGreen(), self.color.getBlue()))

    #Public functions. Setters to interface with the UI to set new values.
    def setColor(self, color):
        self.color = color
        self.pixels.fill((self.color.getRed(), self.color.getGreen(), self.color.getBlue()))

    def setRGB(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        self.pixels.fil(red, green, blue)

    def setBrightness(self, newBrightness):
        self.brightness = newBrightness
        self.pixels.brightness = self.brightness

    #Public functions. Getters to get values for current values of the pixels.
    def getBrightness(self):
        return self.brightness

    