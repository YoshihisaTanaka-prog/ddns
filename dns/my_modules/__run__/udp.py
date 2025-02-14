import socket

from my_modules import *
from .__on_get_response__ import on_get_response

def run():
  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    docker_ip_address = socket.gethostbyname(socket.gethostname())
    server.bind(("0.0.0.0", 53))
    print(f"DNS server (UDP) is Running on {docker_ip_address}:{53}")

    while True:
      data, addr = server.recvfrom(512)
      request = converter.request(data)
      search.from_global(request.h, request.q, on_get_response, server, addr)
      # server.sendto(data, addr)