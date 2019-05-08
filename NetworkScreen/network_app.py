import os
os.environ['KIVY_GL_BACKEND'] = 'gl'

import kivy
kivy.require('1.8.0')
from wifi import Cell,Scheme
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

network_ssid = ''

class ScreenOne(Screen):

    def __init__(self,**kwargs):
        super(ScreenOne,self).__init__(**kwargs)

        my_box1 = BoxLayout(orientation = 'vertical')
        my_label1 = Label(text = "Network Settings", front_size = '24dp')
        my_button1 = Button(text = "Scan",size_hint_y = None, size_y = 100)
        my_button1.bind(on_press = self.changer)
        my_box1.add_widget(my_label1)
        my_box1.add_widget(my_button1)
        self.add_widget(my_box1)

    def changer(self,*args):
        self.manager.current  = 'ScreenTwo'

class ScreenTwo(Screen):

    def __init__(self,**kwargs):
        super(ScreenTwo,self).__init__(**kwargs)


        my_box = BoxLayout(orientation = 'vertical',padding = [150,0])
        l = Label(text = "Available Networks")
        my_box.add_widget(l)
        my_show_list = self.netw_list()
        my_box.my_buttons = []
        for message in my_show_list:
            if message:
                button = Button(text = message)
                my_box.my_buttons.append(button)
                my_box.add_widget(button)
                button.bind(on_press = self.changer)
        self.add_widget(my_box)

    def scan(self):
        cells = Cell.all('wlan0')
        for cell in cells:
            cell.summary = 'SSID {}'.format(cell.ssid,cell)
            cell.summary = cell.summary
        return cells

    def netw_list(self):
        cells = self.scan()
        net_list = []
        for cell in cells:
            ssid = cell.ssid
            if ssid:
                net_list.append(ssid)
        return net_list

    def changer(self,*args):
        self.manager.current  = 'ScreenThree'

class ScreenThree(Screen):
    def __init__(self,**kwargs):
        super(ScreenThree,self).__init__(**kwargs)

        my_box = BoxLayout(orientation = 'vertical',padding = [150,0])
        l = Label(text = "Network Key")
        my_box.add_widget(l)
        key = TextInput(multiline = False)
        my_box.add_widget(key)
        button = Button(text = "Enter")
        button1= Button(text = "Return")
        button1.bind(on_press = self.changer)
        my_box.add_widget(button)
        my_box.add_widget(button1)
        self.add_widget(my_box)

    def changer(self,*args):
        self.manager.current = 'ScreenOne'
        


class TestApp(App):

        def build(self):
            my_screenmanager = ScreenManager()
            screen1 = ScreenOne(name = 'ScreenOne')
            screen2 = ScreenTwo(name = 'ScreenTwo')
            screen3 = ScreenThree(name = 'ScreenThree')
            my_screenmanager.add_widget(screen1)
            my_screenmanager.add_widget(screen2)
            my_screenmanager.add_widget(screen3)
            return my_screenmanager

if __name__ == '__main__':
    TestApp().run()


