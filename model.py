import datetime
import time
# from lights import RGB
# from lights import Lights
from kivy.storage.jsonstore import JsonStore

# dayColor = RGB(255, 255, 255) #Create a day RGB object (default color white light)
# nightColor = RGB(255, 0, 0) #Create a night RGB object (default color red light)
# myLights = Lights(dayColor, 0.1, 0, 0) #Create a light object

class clockModel(datetime.datetime):
    def __new__(cls):
        pass

    def getCurrentHour(self):
        mytime = datetime.datetime.now()
        return mytime.hour

    def getCurrentMinute(self):
        mytime = datetime.datetime.now()
        return mytime.minute

    def getCurrentSecond(self):
        mytime = datetime.datetime.now()
        return mytime.second


class alarmModel:

    def __init__(self):
        self.storeAlarm = JsonStore('alarm.json')
        self.storeSleep = JsonStore('sleep.json')
    
    def setWakeTime(self, hour, minute):
        self.storeAlarm.put(time.strftime("%A"), alarm_hour = hour, alarm_minute = minute)

    def setSleepTime(self, hour, minute):
        self.storeSleep.put(time.strftime("%A"), sleep_hour = hour, sleep_minute = minute)

    def getWakeHour(self):
        return self.storeAlarm.get(time.strftime("%A"))['alarm_hour']

    def getWakeMin(self):
        return self.storeAlarm.get(time.strftime("%A"))['alarm_minute']

    def getSleepHour(self):
        return self.storeSleep.get(time.strftime("%A"))['sleep_hour']

    def getSleepMin(self):
        return self.storeSleep.get(time.strftime("%A"))['sleep_minute']

    def checkSleep(self, *args, callback):
        now = datetime.datetime.now()

        sleepDateTime = datetime.datetime(now.year, now.month, now.day, self.getSleepHour(), self.getSleepMin(), 0) #Create a datetime object to calculate the 30 min before
        sleepDeltaThirty = sleepDateTime - datetime.timedelta(minutes=30) #To calculate to turn lights 30 min before
        local_shour = int(now.hour)
        local_sminute = int(now.minute)
        global wait_next_sminute

        # redDistance = nightColor.getRed() - dayColor.getRed() #final - initial
        # greenDistance = nightColor.getGreen() - dayColor.getGreen() #final - inital
        # blueDistance = nightColor.getBlue() - dayColor.getBlue() #final - initial
        # red = 0
        # green = 0
        # blue = 0

        if(wait_next_sminute!=0 and local_sminute!=self.getSleepMin()):
            wait_next_sminute = 0

        # if(now > sleepDeltaThirty):
        #     if(redDistance > 0):
        #         red = dayColor + (redDistance/30)
        #     if(redDistance < 0):
        #         red = dayColor - (redDistance/30)

        #     if(greenDistance > 0):
        #         green = dayColor + (greenDistance/30)
        #     if(redDistance < 0):
        #         green = dayColor - (greenDistance/30)

        #     if(greenDistance > 0):
        #         blue = dayColor + (blueDistance/30)
        #     if(redDistance < 0):
        #         blue = dayColor - (blueDistance/30)

        #     myLights.setRGB(red, green, blue)

        elif((local_shour == self.getSleepHour() and local_sminute == self.getSleepMin()) and wait_next_sminute == 0):
            callback()
            # myLights.setColor(nightColor)
            wait_next_sminute = 1

    def checkAlarm(self, *args, callback):
        now = datetime.datetime.now()

        alarmDateTime = datetime.datetime(now.year, now.month, now.day, self.getWakeHour(), self.getWakeMin(), 0)#Create a datetime object to calculate the 30 min before
        alarmDeltaThirty = alarmDateTime - datetime.timedelta(minutes=30)#To calculate to turn lights 30 min before
        local_hour = int(now.hour)
        local_minute = int(now.minute)
        global wait_next_minute

        # redDistance = dayColor.getRed() - nightColor.getRed() #final - initial
        # greenDistance = dayColor.getGreen() - nightColor.getGreen() #final - inital
        # blueDistance = dayColor.getBlue() - nightColor.getBlue() #final - initial
        # red = 0
        # green = 0
        # blue = 0

        #logic to ensure alarm function only fires once when it is the alarm time
        if(wait_next_minute!=0 and local_minute != self.getWakeMin()):
            wait_next_minute = 0

        # if(now > alarmDeltaThirty):
        #     if(redDistance > 0):
        #         red = nightColor + (redDistance/30)
        #     if(redDistance < 0):
        #         red = nightColor - (redDistance/30)

        #     if(greenDistance > 0):
        #         green = nightColor + (greenDistance/30)
        #     if(redDistance < 0):
        #         green = nightColor - (greenDistance/30)

        #     if(greenDistance > 0):
        #         blue = nightColor + (blueDistance/30)
        #     if(redDistance < 0):
        #         blue = nightColor - (blueDistance/30)

        #     myLights.setRGB(red, green, blue)

        elif((local_hour == self.getWakeHour() and local_minute == self.getWakeMin()) and wait_next_minute == 0):
            callback()
            # myLights.setColor(dayColor)
            wait_next_minute = 1




class networkConfig:
    pass
    #stuff here

class weatherReport:
    pass
    #Even more stuff here
