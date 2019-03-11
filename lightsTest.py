from lights import RGB
from lights import Lights
import time

colors = RGB(255, 255, 255) #Create an RGB object
myLights = Lights(12, colors, 0.1, 0, 0) #Create a light object

time.sleep(3)

colors.setRed(255)
colors.setGreen(0)
colors.setBlue(0)

myLights.setColor()

