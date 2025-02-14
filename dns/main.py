from threading import Thread
import socket

from my_modules import run_tcp, run_udp

thread1 = Thread(target=run_tcp)
thread2 = Thread(target=run_udp)
thread1.start()
thread2.start()
thread1.join()
thread2.join()