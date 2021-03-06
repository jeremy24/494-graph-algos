from __future__ import print_function

import time



class TimerException(Exception):
    def __init__(self, value):
        self.message = value
    def __str__(self):
        return repr(self.message)

class Timer:
    uoms = ["s","ms","m"]

    def __init__(self, units="s", prec=4):
        self.start = time.time()
        self.prec = int(x=prec)
        if self.valid_unit(units):
            self.units = str(units)
        else:
            raise TimerException("Invalid unit massed to Timer contstructor")
            self.units = "s"

    def valid_unit(self, unit):
        return (unit in self.uoms)

    def reset(self):
        self.start = time.time()

    def output(self):
        return str(round(self.delta(), self.prec) ) + " " + self.units

    def delta(self):
        diff = float(time.time() - self.start)
        if self.units == "s":
            return diff
        elif self.units == "m":
            return diff / 60
        elif self.units == "ms":
            return diff * 1000
