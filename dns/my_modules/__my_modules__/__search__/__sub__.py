from threading import Thread
from my_modules.__my_modules__.__my_exit__ import add_before_tasks

from typing import TypeVar
T = TypeVar("T")

def create_async_func(task_function:T) -> T:
  def f(*args, **kwargs):
    thread = Thread(target=task_function, args=args, kwargs=kwargs)
    add_before_tasks(thread.join)
    thread.start()
  return f