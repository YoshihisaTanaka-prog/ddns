from os import environ as env

import socket

ip_address = socket.gethostbyname(socket.gethostname())

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
  sender.bind((ip_address, 68))
  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as listener:
    listener.bind(("0.0.0.0", 67))
    print(f"DHCP server is Running on {ip_address}:{67}")
    while True:
      data, addr = listener.recvfrom(512)
      print(f"Received: {data}")
      # server.sendto(data, addr)