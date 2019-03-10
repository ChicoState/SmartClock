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

class Timer:
    pass

class Lights:

    def __init__(self, numPixels, color, brightness, sleep, wake):
        self.numPixels = numPixels #Number of neopixels in the array.
        self.color = color #Color of the Pixels. Accepts an RGB value. So 255, 0, 0 for red.
        self.brightness = brightness #Brightness of the pixels. Max brightness is 3, Min is 0
        self.sleep = sleep #Time user wants to sleep so the lights change from day to night time mode.
        self.wake = wake #Time user wants to wake so the lights change from night to day time mode.
        self.pixelPin = board.D18
        self.pixelOrder = neopixel.RGB
        self.pixels = neopixel.NeoPixel(self.pixelPin, self.numPixels)
        self.pixels.brightness = self.brightness
        self.pixels.fill((self.color.getRed(), self.color.getGreen(), self.color.getBlue()))


    #Public functions. Setters to interface with the UI to set new values.
    def setColor(self):
        self.pixels.fill((self.color.getRed(), self.color.getGreen(), self.color.getBlue()))

    def setBrightness(self, newBrightness):
        self.brightness = newBrightness

    def setSleep(self, newTime):
        self.sleep = newTime

    def setWake(self, newTime):
        self.wake = newTime

    #Public functions. Getters to get values for current values of the pixels.
    def getColor(self):
        return self.color

    def getBrightness(self):
        return self.brightness

    def getSleep(self):
        return self.sleep

    def  getWake(self):
        return self.wake

    