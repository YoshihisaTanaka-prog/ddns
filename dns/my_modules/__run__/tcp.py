# from dnslib import DNSRecord, QTYPE
import socket, struct

from my_modules import *
from .__on_get_response__ import on_get_response

def run():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    docker_ip_address = socket.gethostbyname(socket.gethostname())
    server.bind(("0.0.0.0", 53))
    server.listen()
    print(f"DNS server (TCP) is Running on {docker_ip_address}:{53}")
    conn, _ = server.accept()
    with conn:
      while True:
        data = conn.recv(1024)
        if not data:
          break
        else:
          length = struct.unpack("!H",bytes(data[:2]))[0]
          while len(data) - 2 < length:
            data += conn.recv(1024)
          request = converter.request(data[2:])
          search.from_global(request.h, request.q, on_get_response, conn)
