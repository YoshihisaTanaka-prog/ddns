import socket

from .__main_task__ import main_task

def run():
  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 53))
    docker_ip_address = socket.gethostbyname(socket.gethostname())
    print(f"DNS server (UDP) is Running on {docker_ip_address}:{53}")

    while True:
      data, addr = server.recvfrom(512)
      main_task(data, server, addr)