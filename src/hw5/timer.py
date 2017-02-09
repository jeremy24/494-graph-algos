from __future__ import print_function

from time import time as time

class TimerException(Exception):
    def __init__(self, value):
        self.message = value
    def __str__(self):
        return repr(self.message)

class Timer:
    _uoms = [["ms",.001],["s",1],["m",60]]
    @property
    def uoms(self):
        return self._uoms
    def __init__(self, units="s", prec=4):
        
        self.start = time()
        try:
            self.prec = int(prec)
        except ValueError as valEr:
            print("Invalid prec given, using default.")
            self.prec = 4
        try:
            if self.valid_unit(str(units).strip(" ")):
                for pair in self.uoms:
                    if pair[0] == str(units):
                        self.unitIndex = self.uoms.index(pair)
                        break
            else:
                print("Invalid units given")
                self.unitIndex = 1
        except Exception as ex:
            print("error assigning unitIndex", ex)
            self.unitIndex = 1
    def valid_unit(self, unit):
        try:
            for pair in self.uoms:
                if pair[0] == unit:
                    return True
            return False
        except Exception as ex:
            print("Valid units throw: ", ex)
            return False
    def clock(self, format_output=True):
        ret = ""
        try:
            print(float(time() - self.start), float(self.uoms[self.unitIndex][1]))
            ret = float(time() - self.start) / float(self.uoms[self.unitIndex][1])
            print(self.prec)
            ret = round(ret, self.prec)
            self.start = time()
            if format_output:
                return str(ret) + " " + str(self.uoms[self.unitIndex][0])
            return str(ret)        
        except Exception as ex:
            print(ex)
            return ret