# adapted from https://stackoverflow.com/questions/18923321/making-a-clock-in-kivy
# adapted from https://github.com/akrog100/Meza/blob/master/main.py
import os
#comment this line if you have issues testing locally
#this is for the app to run on the pi
#os.environ['KIVY_GL_BACKEND'] = 'gl'
from kivy.app import App
import json
from kivy.uix.widget import Widget
from kivy.uix.switch import Switch
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
from functools import partial
import time
import datetime
import subprocess
from model import clockModel
from model import alarmModel

Builder.load_file('clockHomeView.kv')
Builder.load_file('alarmScreen.kv')
Builder.load_file('lights.kv')
# Builder.load_file('noise.kv')
Builder.load_file('colorLights.kv')
Builder.load_file('settingScreen.kv')

myAlarm = alarmModel()
myAlarm.setWakeTime(5, 30)
myAlarm.setSleepTime(9, 0)

alarm_hour = 0;
alarm_minute = 0
sleep_hour = 0;
sleep_minute = 0;
alarm_changed = 0
wait_next_sminute = 0
wait_next_minute = 0
myColor = [0,0,1,1]
clr_picker = ColorPicker()
#parent.add_widget(colorpicker)

class HomeScreen(Screen):
    pass

class AlarmScreen(Screen):
    pass

class LightScreen(Screen):
    pass

class colorLights(Screen):
    pass

class LightButton(Button):
   pass

class ColPcker(ColorPicker):
    pass

class settingScreen(Screen):
    pass

class myColorPicker(Widget):
    selected_color = ListProperty(myColor)

    def on_touch_down(self, touch):
        if touch.x < 100 and touch.y < 100:
            return super(myColorPicker, self).on_touch_down(touch)

class WifiPopup(Button):
    def __init__(self, **kwargs):
        super(WifiPopup, self).__init__(**kwargs)
        self.text = "Set Wifi"
    def on_press(self):
        Clock.schedule_once(self.setWifi)
    def setWifi(self, *args):
        content = Button(text='Select Network', size_hint=(.2,.2),
                            pos_hint={'x':.2, 'y':.5})
        contentDown = DropDown()
        content.bind(on_release=contentDown.open)
        popup = Popup(title='network settings',
    content=content,
        size_hint=(None, None), size=(400, 400))
        popup.open()


#class to check cur time against alarm time and fire alarm
class wakeAlarmController(Widget):
    def __init__(self, **kwargs):
        super(wakeAlarmController, self).__init__(**kwargs)
        Clock.schedule_interval(partial(myAlarm.checkAlarm, self.alarm_func), 1)
        
    def alarm_func(self, *args):    
        content = Button(text= 'dismiss')
        popup = Popup(title='alarm popup', content=content, size_hint=(None, None), size=(400, 400), auto_dismiss=False)

        popup.open()
        sound = SoundLoader.load('sounds/alarm.wav')

        if sound:
            sound.play()
            content.bind(on_press=lambda *args: sound.stop())
            content.bind(on_press=popup.dismiss)

# class to check sleep time against current time and
# fire  popup - eventually should trigger lights
class FireSleep(Widget):
    def __init__(self, **kwargs):
        super(FireSleep, self).__init__(**kwargs)
        Clock.schedule_interval(partial(myAlarm.checkSleep, self.sleep_func), 1)

    def sleep_func(self, *args):
        content = Button(text= 'dismiss')
        sleep_popup = Popup(title='sleep popup', content=content, size_hint=(None, None), size=(400, 400))
        sleep_popup.open()

# Handles the interaction between the clockModel and the clock.kv File
class clockController(Widget):
    def __init__(self, **kwargs):
        super(clockController, self).__init__(**kwargs)
        self.bind(pos=self.updateDisplay)
        self.bind(size=self.updateDisplay)
        Clock.schedule_interval(self.updateDisplay, 1)

    def updateDisplay(self, *args):
        myModel = clockModel
        self.canvas.clear()
        with self.canvas:
            Color(0.2, 0.5, 0.2) #what colors are these???
            Line(points=[self.center_x, self.center_y, self.center_x+0.8*self.r*sin(pi/30*myModel.getCurrentSecond(self)), self.center_y+0.8*self.r*cos(pi/30*myModel.getCurrentSecond(self))], width=1, cap="round")
            Color(0.3, 0.6, 0.3)
            Line(points=[self.center_x, self.center_y, self.center_x+0.7*self.r*sin(pi/30*myModel.getCurrentMinute(self)), self.center_y+0.7*self.r*cos(pi/30*myModel.getCurrentMinute(self))], width=2, cap="round")
            Color(0.4, 0.7, 0.4)
            th = myModel.getCurrentHour(self)*25 + myModel.getCurrentMinute(self)
            Line(points=[self.center_x, self.center_y, self.center_x+0.5*self.r*sin(pi/360*th), self.center_y+0.5*self.r*cos(pi/360*th)], width=3, cap="round")


# popup with option to set alarm and logic to store alarm time
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
            myAlarm.setWakeTime(alarm_hour, alarm_minute)
        instance.dismiss()

# popup to store sleep time
class SetSleepPopup(Button):
    def __init__(self, **kwargs):
        super(SetSleepPopup, self).__init__(**kwargs)
        self.text = "Set Sleep time"
        self.size_hint=(.2,.2);
        self.pos_hint={'x':.6, 'y':.2}

    def dismissSleepPopup(self, instance, button1, button2, button4):
        global sleep_hour
        global sleep_minute
        if(button1.text != "Select Hour" and button2.text != "Select Minute"):
            sleep_hour = math.floor(int(button1.text))
            sleep_minute = math.floor(int(button2.text))
            myAlarm.setSleepTime(sleep_hour, sleep_minute)
        instance.dismiss()

# button used to select hour/min for either alarm
class SetTimeButton(Button):
    def __init__(self, **kwargs):
        super(SetTimeButton, self).__init__(**kwargs)
        self.text = "Set Alarm"
        Clock.schedule_interval(self.updateTimeDisplay, 1)

    def on_press(self):
        Clock.schedule_once(self.alarmPopup)
        
    def alarmPopup(self, *args):
        box = FloatLayout()
        hourbutton = Button(text='Select Hour', size_hint=(.2,.2), pos_hint={'x':.2, 'y':.5})
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
        minutebutton = Button(text='Select Minute', size_hint=(.2,.2), pos_hint={'x':.6, 'y':.5})
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

    def updateTimeDisplay(self, *args):
        alarm_hour = myAlarm.getWakeHour()
        alarm_minute = myAlarm.getWakeMin()
        sleep_hour = myAlarm.getSleepHour()
        sleep_minute = myAlarm.getSleepMin()

        #text formatting to properly display the current alarm
        if(sleep_hour < 10 and sleep_minute < 10):
            self.text = "Set sleep time\n sleep time set to: 0{}:0{}\n Set alarm time \n alarm time set to: 0{}:0{}".format(sleep_hour, sleep_minute, alarm_hour, alarm_minute)
        elif(sleep_minute < 10):
            self.text = "Set sleep time\n sleep time set to: {}:0{}\n Set alarm time \n alarm time set to: 0{}:0{}".format(sleep_hour, sleep_minute, alarm_hour, alarm_minute).format(sleep_hour, sleep_minute)
        elif(sleep_hour < 10):
            self.text = "Set sleep time\n sleep time set to: 0{}:{}\n Set alarm time \n alarm time set to: 0{}:0{}".format(sleep_hour, sleep_minute, alarm_hour, alarm_minute).format(sleep_hour, sleep_minute)
        else:
            self.text = "Set sleep time\n sleep time set to: {}:{} \n Set alarm time \n alarm time set to: {}:{}".format(sleep_hour, sleep_minute, alarm_hour, alarm_minute).format(sleep_hour, sleep_minute)

# button to start white noise sound
class WhiteNoise(Widget):
    def __init__(self, **kwargs):
        super(WhiteNoise, self).__init__(**kwargs)
        
        def callback(instance, value):
            if(value is True):
                noise1.play()
            elif(value is False):
                noise1.stop()
        self.text = "white noise"
        noise1 = SoundLoader.load('sounds/noise1.wav')
        noise1.loop = True
        switch = Switch()
        switch.bind(active = callback)
        self.add_widget(switch)


sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(AlarmScreen(name='alarm'))
sm.add_widget(LightScreen(name='lights'))
# sm.add_widget(NoiseScreen(name='noise'))
sm.add_widget(colorLights(name='colorLights'))
sm.add_widget(settingScreen(name='settingScreen'))

class MyClockApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MyClockApp().run()
