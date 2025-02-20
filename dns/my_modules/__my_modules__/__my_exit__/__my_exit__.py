from traceback import print_exc
from threading import RLock, Thread
from os import  _exit
from time import sleep
from typing import TypeVar
T = TypeVar("T")

FuncType = TypeVar("() -> None ")

lock = RLock()

class Exit:
  before_tasks:list[Thread] = []
  is_running = True
  did_call = False
  def add_before_tasks(self, *before_tasks:FuncType):
    with lock:
      Exit.before_tasks += before_tasks
    
  def exit(self):
    print("called exit")
    if Exit.did_call == False:
      Exit.did_call = True
      with lock:
        Exit.is_running = False
        try:
          for task in Exit.before_tasks:
            task()
        finally:
          print_exc(15)
          _exit(1)
    
exit_instance = Exit()
add_before_tasks = exit_instance.add_before_tasks
exit = exit_instance.exit
def is_running():
  with lock:
    return exit_instance.is_running
