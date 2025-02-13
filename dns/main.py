# from dnslib import DNSRecord, QTYPE
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
  server.bind(("0.0.0.0", 5353))
  server.listen()
  print("DNS server (tcp) is Running")
  conn, _ = server.accept()
  with conn:
    while True:
      data = conn.recv(1024)
      if not data:
        break
      print(f"Received: {data}")
      # conn.sendall(data)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
  server.bind(("0.0.0.0", 5353))
  print("DNS server (udp) is Running")

  while True:
    data, addr = server.recvfrom(512)
    print(f"Received: {data}")
    # server.sendto(data, addr)