import unittest
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from controller import MyClockApp
class dismisssleepTestCase(unittest.TestCase):
	def setUp(self):
		from controller import SetAlarmPopup

	def test_alarmHour(self):
		from controller import SetAlarmPopup
		from model import alarmModel
		myAlarm = alarmModel()
		alarm = SetAlarmPopup()
		four = Button(text = '04')
		fortyFive = Button(text = '45')
		alarmPopup = Popup()
		alarm.dismissAlarmPopup(alarmPopup, four, fortyFive, 0)
		self.assertEqual(myAlarm.getWakeHour(), 4)

	def test_alarmMin(self):
		from controller import SetAlarmPopup
		from model import alarmModel
		myAlarm = alarmModel()
		alarm = SetAlarmPopup()
		four = Button(text = '04')
		fortyFive = Button(text = '45')
		alarmPopup = Popup()
		alarm.dismissAlarmPopup(alarmPopup, four, fortyFive, 0)
		self.assertEqual(myAlarm.getWakeMin(), 45)

	def test_sleepHour(self):
		from controller import SetSleepPopup
		from model import alarmModel
		myAlarm = alarmModel()
		sleep = SetSleepPopup()
		four = Button(text = '04')
		fortyFive = Button(text = '45')
		sleepPopup = Popup()
		sleep.dismissSleepPopup(sleepPopup, four, fortyFive, 0)
		self.assertEqual(myAlarm.getSleepHour(), 4)

	def test_sleepMin(self):
		from controller import SetSleepPopup
		from model import alarmModel
		myAlarm = alarmModel()
		sleep = SetSleepPopup()
		four = Button(text = '04')
		fortyFive = Button(text = '45')
		sleepPopup = Popup()
		sleep.dismissSleepPopup(sleepPopup, four, fortyFive, 0)
		self.assertEqual(myAlarm.getSleepMin(), 45)

if __name__ == '__main__':
	unittest.main()
