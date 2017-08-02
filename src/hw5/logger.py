from __future__ import print_function

import logging
import sys
import pip
import os


def install(package):
    try:
        pip.main(["install", package])
    except Exception as ex:
        raise "Unable to install " + package + ex 

try:
    install("colorlog")
    import colorlog
except Exception as ex:
    raise ex


def mk_logger(have_colorlog):
        log = logging.getLogger() # root logger
        log.setLevel(logging.DEBUG)
        format      = '%(asctime)s - %(levelname)-8s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        if have_colorlog and os.isatty(2):
            cformat = '%(log_color)s' + format
            f = colorlog.ColoredFormatter(cformat, date_format,
                log_colors = { 'DEBUG'   : 'reset',       'INFO' : 'reset',
                                'WARNING' : 'bold_yellow', 'ERROR': 'bold_red',
                                'CRITICAL': 'bold_red' })
        else:
            f = logging.Formatter(format, date_format)
        ch = logging.StreamHandler()
        ch.setFormatter(f)
        log.addHandler(ch)
        return logging.getLogger(__name__)





class LogException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class Logger():
    _level = "debug"
    _levels = ["debug", "info", "warn", "error"]
    # colors = { "debug": "blue", "info": "green", "warning": "yellow", "error": "red"}
    def __init__(self, module):
        self.module = str(module)
        self.have_colorlog = True     
        self.logger = mk_logger(True)
    @property
    def level(self):
        return self._level
    @property
    def levels(self):
        return self._levels
    @level.setter
    def level(self, val):
        if val in self.levels():
            self._level = val
    @property 
    def form(self, *args):
        msg = ""
        try:
            for arg in args:
                print (arg)
                # msg += " " + arg
            # return msg
        except Exception as ex:
            print("Error concattng args!  " + ex.message)
        finally:
            return msg

    def debug(self, *args):
        self.logger.debug("a")
        self.logger.debug(args)


a = Logger("test")
a.debug("blah", "blah")

    

