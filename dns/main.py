from threading import Thread
from time import sleep

from my_modules import run_tcp, run_udp, exit, add_before_tasks

def add_before_tasks_local(*args):
  sleep(1)
  Thread(target=add_before_tasks, args=args).start()
  

try:
  thread1 = Thread(target=run_tcp, daemon=True)
  thread2 = Thread(target=run_udp, daemon=True)
  thread1.start()
  thread2.start()
  thread1.join()
  thread2.join()
except:
  exit()