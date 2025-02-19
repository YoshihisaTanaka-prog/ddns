from threading import Thread

from my_modules import run_tcp, run_udp, exit

try:
  thread1 = Thread(target=run_tcp, daemon=True)
  thread2 = Thread(target=run_udp, daemon=True)
  thread1.start()
  thread2.start()
  thread1.join()
  thread2.join()
except:
  exit()