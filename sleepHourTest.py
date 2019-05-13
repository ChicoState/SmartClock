import unittest
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from controller import MyClockApp
class dismisssleepTestCase(unittest.TestCase):
	def setUp(self):
		from controller import SetSleepPopup

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

if __name__ == '__main__':
	unittest.main()
