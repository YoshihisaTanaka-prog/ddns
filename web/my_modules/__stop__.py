from os import _exit
from threading import Thread
from time import sleep

from .__base__ import BaseType, Handler, post_method_dict

def stop_unit():
  sleep(2)
  _exit(1)

def stop(_:BaseType, handler:Handler):
  Thread(target=stop_unit).start()
  return "OK"
  

post_method_dict.set_method("/stop", BaseType, stop)