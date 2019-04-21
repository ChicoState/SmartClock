import datetime

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


class alarm:
    def __init__():
        self.color
        self.fireHour
        self.fireMinute
        self.fireSecond

class networkConfig:
    pass
    #stuff here

class weatherReport:
    pass
    #Even more stuff here
