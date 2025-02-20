import socket

from .__main_task__ import main_task
from .__my_modules__ import add_before_tasks, exit, is_running

def run():
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
      add_before_tasks(server.close)
      server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      server.bind(("0.0.0.0", 53))
      print(f"DNS server (UDP) is Running on {socket.gethostbyname(socket.gethostname())}:{53}")

      while is_running():
        data, addr = server.recvfrom(512)
        main_task(data, server, addr)
  except:
    exit()