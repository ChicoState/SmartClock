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

if __name__ == '__main__':
	unittest.main()
