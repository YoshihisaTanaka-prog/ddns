import socket
from threading import Thread

from my_modules import MyDHCP, ack_for_inform, ack_for_request, offer, release

threads:list[Thread]=[]

# 2001:a7ff:ff47:101::1

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
  def send(data:bytes):
    server.sendto(data, ("255.255.255.255", 68))
  
  def core_task(data:bytes):
    print(f"Received data")
    my_dhcp = MyDHCP(data)
    message_type = my_dhcp.get_message_type()
    if message_type  == 1:  # DISCOVER
      send(offer(my_dhcp))
    if message_type == 3:  # REQUEST or INFORM
      send(ack_for_request(data))
    if message_type == 7:  # RELEASE
      release(my_dhcp)
    if message_type == 8:
      send(ack_for_inform(my_dhcp))
    
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  server.bind(("0.0.0.0", 67))
  print(f"DHCP server is Running on {socket.gethostbyname(socket.gethostname())}:{67}")
  while True:
    data, _ = server.recvfrom(512)
    threads.append(Thread(target=core_task, args=[data], daemon=True).start())
  
for thread in threads:
  thread.join()