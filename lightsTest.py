from lights import RGB
from lights import Lights
import time

dayColor = RGB(255, 255, 255) #Create a day RGB object (default color white light)
nightColor = RGB(255, 0, 0) #Create a night RGB object (default color red light)

myLights = Lights(dayColor, 0.1) #Create a light object

time.sleep(3)

myLights.setColor(nightColor)


