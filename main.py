# adapted from https://stackoverflow.com/questions/18923321/making-a-clock-in-kivy
# adapted from https://github.com/akrog100/Meza/blob/master/main.py
import os
#comment this line if you have issues testing locally
#this is for the app to run on the pi
os.environ['KIVY_GL_BACKEND'] = 'gl'
from kivy.app import App
import json
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout
from math import cos, sin, pi
from kivy.clock import Clock
from functools import partial
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.core.audio import SoundLoader
import time
import datetime
import subprocess
# from lights import RGB
# from lights import Lights

Builder.load_file('alarmClock.kv');
Builder.load_file('alarmScreen.kv');
Builder.load_file('lights.kv');
Builder.load_file('noise.kv')

# dayColor = RGB(255, 255, 255) #Create a day RGB object (default color white light)
# nightColor = RGB(255, 0, 0) #Create a night RGB object (default color red light)
# myLights = Lights(dayColor, 0.1, 0, 0) #Create a light object

alarm_hour = 0;
alarm_minute = 0
sleep_hour = 0;
sleep_minute = 0;
alarm_changed = 0
wait_next_sminute = 0
wait_next_minute = 0
col = [0,0,1,1]
#clr_picker = ColorPicker()
#parent.add_widget(colorpicker)
storeAlarm = JsonStore('alarm.json')
storeSleep = JsonStore('sleep.json')
kv = '''
#:import math math

[ClockNumber@Label]:
    text: str(ctx.i)
    pos_hint: {"center_x": 0.5+0.42*math.sin(math.pi/6*(ctx.i-12)), "center_y": 0.5+0.42*math.cos(math.pi/6*(ctx.i-12))}
    font_size: self.height/16
'''
Builder.load_string(kv)

class HomeScreen(Screen):
    pass

class AlarmScreen(Screen):
    pass

class LightScreen(Screen):
    pass

class NoiseScreen(Screen):
    pass

class LightButton(Button):
   pass

class SelectedColorEllipse(Widget):
    selected_color = ListProperty(col)

class ColPcker(ColorPicker):
    pass

class Ex40(Widget):
    selected_color = ListProperty(col)
    def select_ColPckr(self, *args):
        ColPopup().open()
    def on_touch_down(self,touch):
        if touch.x < 100 and touch.y < 100:
            return super(Ex40, self).on_touch_down(touch)

class Ticks(Widget):
    def __init__(self, **kwargs):
        super(Ticks, self).__init__(**kwargs)
        self.bind(pos=self.update_clock)
        self.bind(size=self.update_clock)
        Clock.schedule_interval(self.update_clock, 1)
        Clock.schedule_interval(self.checkAlarm, 1)
        Clock.schedule_interval(self.checkSleep, 1)

    def checkAlarm(self, *args):
        global alarm_hour
        global alarm_minute
        now = datetime.datetime.now()
        alarmDateTime = datetime.datetime(now.year, now.month, now.day, alarm_hour, alarm_minute, 0)
        alarmDeltaThirty = alarmDateTime - datetime.timedelta(minutes=30)
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
        if(wait_next_minute!=0 and local_minute!=alarm_minute):
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

        elif((local_hour == alarm_hour and local_minute == alarm_minute) and wait_next_minute == 0):
            self.alarm_func()
            # myLights.setColor(dayColor)
            wait_next_minute = 1

    def checkSleep(self, *args):
        global sleep_hour
        global sleep_minute
        now = datetime.datetime.now()

        sleepDateTime = datetime.datetime(now.year, now.month, now.day, sleep_hour, sleep_minute, 0)
        sleepDeltaThirty = sleepDateTime - datetime.timedelta(minutes=30)
        local_shour = int(now.hour)
        local_sminute = int(now.minute)
        global wait_next_sminute

        # redDistance = nightColor.getRed() - dayColor.getRed() #final - initial
        # greenDistance = nightColor.getGreen() - dayColor.getGreen() #final - inital
        # blueDistance = nightColor.getBlue() - dayColor.getBlue() #final - initial
        # red = 0
        # green = 0
        # blue = 0

        if(wait_next_sminute!=0 and local_sminute!=sleep_minute):
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

        elif((local_shour == sleep_hour and local_sminute == sleep_minute) and wait_next_sminute == 0):
            self.sleep_func()
            # myLights.setColor(nightColor)
            wait_next_sminute = 1

    def alarm_func(self, *args):
        content = Button(text= 'dismiss')
        popup = Popup(title='alarm popup',
    content=content,
        size_hint=(None, None), size=(400, 400), auto_dismiss=False)
        popup.open()
        sound = SoundLoader.load('alarm.wav')
        if sound:
            sound.play()
            content.bind(on_press=lambda *args: sound.stop())
            content.bind(on_press=popup.dismiss)

    def sleep_func(self, *args):
        content = Button(text= 'dismiss')
        sleep_popup = Popup(title='sleep popup',
    content=content,
        size_hint=(None, None), size=(400, 400))
        sleep_popup.open()

    def update_clock(self, *args):
        self.canvas.clear()
        with self.canvas:
            clocktime = datetime.datetime.now()
            Color(0.2, 0.5, 0.2)
            Line(points=[self.center_x, self.center_y, self.center_x+0.8*self.r*sin(pi/30*clocktime.second), self.center_y+0.8*self.r*cos(pi/30*clocktime.second)], width=1, cap="round")
            Color(0.3, 0.6, 0.3)
            Line(points=[self.center_x, self.center_y, self.center_x+0.7*self.r*sin(pi/30*clocktime.minute), self.center_y+0.7*self.r*cos(pi/30*clocktime.minute)], width=2, cap="round")
            Color(0.4, 0.7, 0.4)
            th = clocktime.hour*60 + clocktime.minute
            Line(points=[self.center_x, self.center_y, self.center_x+0.5*self.r*sin(pi/360*th), self.center_y+0.5*self.r*cos(pi/360*th)], width=3, cap="round")

class SetAlarmPopup(Button):
    def __init__(self, **kwargs):
        super(SetAlarmPopup, self).__init__(**kwargs)
        self.text = "Set Alarm"
        self.size_hint=(.2,.2);
        self.pos_hint={'x':.2, 'y':.2}

    def dismissAlarmPopup(self, instance, button1, button2, button3):
        global alarm_hour
        global alarm_minute

        if(button1.text != "Select Hour" and button2.text != "Select Minute"):
            alarm_hour = int(button1.text)
            alarm_minute = int(button2.text)
            currentDay = time.strftime("%A")
            storeAlarm.put(currentDay, alarm_hour = alarm_hour, alarm_minute = alarm_minute)

        instance.dismiss()

class SetSleepPopup(Button):
    def __init__(self, **kwargs):
        super(SetSleepPopup, self).__init__(**kwargs)
        self.text = "Set Sleep Alarm"
        self.size_hint=(.2,.2);
        self.pos_hint={'x':.6, 'y':.2}

    def dismissSleepPopup(self, instance, button1, button2, button4):
        global sleep_hour
        global sleep_minute

        if(button1.text != "Select Hour" and button2.text != "Select Minute"):
            sleep_hour = int(button1.text)
            sleep_minute = int(button2.text)
            currentDay = time.strftime("%A")
            storeSleep.put(currentDay, sleep_hour = sleep_hour, sleep_minute = sleep_minute)

        instance.dismiss()

class SetAlarmButton(Button):
    def __init__(self, **kwargs):
        super(SetAlarmButton, self).__init__(**kwargs)
        #schedule this button to continually look to update it's text to reflect the current alarm
        Clock.schedule_interval(self.updateAlarm, 1)
        Clock.schedule_interval(self.updateSleep, 1)


    def on_press(self):
        Clock.schedule_once(self.alarmPopup)

    def alarmPopup(self, *args):
        box = FloatLayout()
        hourbutton = Button(text='Select Hour', size_hint=(.2,.2),
                            pos_hint={'x':.2, 'y':.5})
        hourdropdown = DropDown()
        for i in range(24):
            if(i<10):
                btn=Button(text = '0%r' % i, size_hint_y=None, height =70)
            else:
                btn=Button(text = '%r' % i, size_hint_y=None, height =70)
            btn.bind(on_release=lambda btn: hourdropdown.select(btn.text))
            hourdropdown.add_widget(btn)
        hourbutton.bind(on_release=hourdropdown.open)
        hourdropdown.bind(on_select=lambda instance, x: setattr(hourbutton, 'text', x))
        box.add_widget(hourbutton)
        box.add_widget(hourdropdown)
        minutebutton = Button(text='Select Minute', size_hint=(.2,.2),
                            pos_hint={'x':.6, 'y':.5})
        minutedropdown = DropDown()
        for i in range(60):
            if(i<10):
                btn=Button(text = '0%r' % i, size_hint_y=None, height =70)
            else:
                btn=Button(text = '%r' % i, size_hint_y=None, height =70)
            btn.bind(on_release=lambda btn: minutedropdown.select(btn.text))
            minutedropdown.add_widget(btn)
        minutebutton.bind(on_release=minutedropdown.open)
        minutedropdown.bind(on_select=lambda instance, x: setattr(minutebutton, 'text', x))
        box.add_widget(minutebutton)
        box.add_widget(minutedropdown)

        #button to dismiss alarm selector and set alarm once user has chosen alarm
        dismissButton1 = SetAlarmPopup()
        dismissButton2 = SetSleepPopup()
        box.add_widget(dismissButton1)
        box.add_widget(dismissButton2)

        currentDay = time.strftime("%A")
        alarmPopup = Popup(title='Set Your Alarm for {}:'.format(currentDay), content=box, size_hint=(.8, .8))
        dismissButton1.bind(on_press=partial(dismissButton1.dismissAlarmPopup, alarmPopup, hourbutton, minutebutton))
        dismissButton2.bind(on_press=partial(dismissButton2.dismissSleepPopup, alarmPopup, hourbutton, minutebutton))
        alarmPopup.open()

    def updateSleep(self, *args):
        global sleep_hour
        global sleep_minute
        currentDay = time.strftime("%A")
        self.valign = 'middle'
        self.halign = 'center'
        if(storeSleep.exists(currentDay)):
            sleep_hour = storeSleep.get(currentDay)['sleep_hour']
            sleep_minute = storeSleep.get(currentDay)['sleep_minute']
        #default state of alarm button before any alarms are set
        if(sleep_hour == 0 and sleep_minute == 0):
            self.text = "    Set sleep time\n sleep time not Set".format(sleep_hour, sleep_minute)

        #text formatting to properly display the current alarm
        else:
            if(sleep_hour < 10 and sleep_minute < 10):
                self.text = "Set sleep time\n sleep time set to: 0{}:0{}".format(sleep_hour, sleep_minute)
            elif(sleep_minute < 10):
                self.text = "Set sleep time\n sleep time set to: {}:0{}".format(sleep_hour, sleep_minute)
            elif(sleep_hour < 10):
                self.text = "Set sleep time\n sleep time set to: 0{}:{}".format(sleep_hour, sleep_minute)
            else:
                self.text = "Set sleep time\n sleep time set to: {}:{}".format(sleep_hour, sleep_minute)
    def updateAlarm(self, *args):
        global alarm_hour
        global alarm_minute
        currentDay = time.strftime("%A")
        self.valign = 'middle'
        self.halign = 'center'
        if storeAlarm.exists(currentDay):
            alarm_hour = storeAlarm.get(currentDay)['alarm_hour']
            alarm_minute = storeAlarm.get(currentDay)['alarm_minute']

        #default state of alarm button before any alarms are set
        if(alarm_hour == 0 and alarm_minute == 0):
            self.text = "    Set Alarm\n Alarm Not Set".format(alarm_hour, alarm_minute)

        #text formatting to properly display the current alarm
        else:
            if(alarm_hour < 10 and alarm_minute < 10):
                self.text = "Set Alarm\n alarm set to: 0{}:0{}".format(alarm_hour, alarm_minute)
            elif(alarm_minute < 10):
                self.text = "Set Alarm\n alarm set to: {}:0{}".format(alarm_hour, alarm_minute)
            elif(alarm_hour < 10):
                self.text = "Set Alarm\n alarm set to: 0{}:{}".format(alarm_hour, alarm_minute)
            else:
                self.text = "Set Alarm\n alarm set to: {}:{}".format(alarm_hour, alarm_minute)

class WhiteNoise(Button):
    def __init__(self, **kwargs):
        super(WhiteNoise, self).__init__(**kwargs)
        self.text = "play"
    def on_press(self):
        noise1 = SoundLoader.load('alarm.wav')
        self.bind(on_press=lambda *args: sound.play())


sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(AlarmScreen(name='alarm'))
sm.add_widget(LightScreen(name='lights'))
sm.add_widget(NoiseScreen(name='noise'))

#sce = SelectedColorEllipse()
#sce.selected_color = self.selected_color
#sce.center = touch.pos
#self.add_widget(sce)

class MyClockApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MyClockApp().run()
