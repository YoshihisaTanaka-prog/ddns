import socket

from my_modules import MyDHCP, erase_data, search_from_client_data, search_from_ip, set_data

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  server.bind(("0.0.0.0", 67))
  print(f"DHCP server is Running on {socket.gethostbyname(socket.gethostname())}:{67}")
  while True:
    data, _ = server.recvfrom(512)
    print(f"Received: {data}")
    my_dhcp = MyDHCP(data)
    message_type = my_dhcp.get_message_type()
    if message_type == 1:  # DISCOVER
      pass
    if message_type in (3, 8):  # REQUEST or INFORM
      pass
    if message_type == 7:  # RELEASE
      pass
    server.sendto(my_dhcp.to_bytes(), ("255.255.255.255", 68))