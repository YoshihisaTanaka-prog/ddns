from traceback import print_exc
from sys import exit as _exit
from time import sleep
from typing import TypeVar
T = TypeVar("T")

FuncType = TypeVar("() -> None ")

class Exit:
  _before_tasks = []
  
  def add_before_tasks(self, *before_tasks:FuncType):
    Exit._before_tasks += before_tasks
    
  def exit(self):
    try:
      for task in Exit._before_tasks:
        task()
    except:
      pass
    finally:
      print_exc(15)
      sleep(1)
      _exit(1)
    
exit_instance = Exit()
add_before_tasks = exit_instance.add_before_tasks
exit = exit_instance.exit