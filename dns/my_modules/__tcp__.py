# from dnslib import DNSRecord, QTYPE
import socket, struct

from .__main_task__ import main_task

def run():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 53))
    server.listen()
    print(f"DNS server (TCP) is Running on {socket.gethostbyname(socket.gethostname())}:{53}")
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
          main_task(data[2:], conn)
