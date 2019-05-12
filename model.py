import datetime
import time

from kivy.storage.jsonstore import JsonStore

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
        self.wait_next_minuteW = 0
        self.wait_next_sminute = 0

    def setWakeTime(self, hour, minute):
        self.storeAlarm.put("AlarmTime", alarm_hour = hour, alarm_minute = minute)

    def setSleepTime(self, hour, minute):
        self.storeAlarm.put("SleepTime", sleep_hour = hour, sleep_minute = minute)

    def getWakeHour(self):
        return self.storeAlarm.get("AlarmTime")['alarm_hour']

    def getWakeMin(self):
        return self.storeAlarm.get("AlarmTime")['alarm_minute']

    def getSleepHour(self):
        return self.storeAlarm.get("SleepTime")['sleep_hour']

    def getSleepMin(self):
        return self.storeAlarm.get("SleepTime")['sleep_minute']

    def checkSleep(self, callback, *args):
        now = datetime.datetime.now()
        sleepDateTime = datetime.datetime(now.year, now.month, now.day, self.getSleepHour(), self.getSleepMin(), 0) #Create a datetime object to calculate the 30 min before
        sleepDeltaThirty = sleepDateTime - datetime.timedelta(minutes=30) #To calculate to turn lights 30 min before
        local_shour = int(now.hour)
        local_sminute = int(now.minute)
        if(self.wait_next_sminute!=0 and local_sminute!=self.getSleepMin()):
            self.wait_next_sminute = 0
        elif((local_shour == self.getSleepHour() and local_sminute == self.getSleepMin()) and self.wait_next_sminute == 0):
            callback()
            self.wait_next_sminute = 1

    def checkAlarm(self, callback, *args):
        now = datetime.datetime.now()

        alarmDateTime = datetime.datetime(now.year, now.month, now.day, self.getWakeHour(), self.getWakeMin(), 0)#Create a datetime object to calculate the 30 min before
        alarmDeltaThirty = alarmDateTime - datetime.timedelta(minutes=30)#To calculate to turn lights 30 min before
        local_hour = int(now.hour)
        local_minute = int(now.minute)
        if(self.wait_next_minuteW != 0 and local_minute != self.getWakeMin()):
            self.wait_next_minuteW = 0
        elif((local_hour == self.getWakeHour() and local_minute == self.getWakeMin()) and self.wait_next_minuteW == 0):
            callback()
            self.wait_next_minuteW = 1
