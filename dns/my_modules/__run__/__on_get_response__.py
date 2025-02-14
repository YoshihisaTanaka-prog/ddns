import struct
from dnslib import DNSRecord

def on_get_response(response:DNSRecord, server_socket, addr):
  if addr:
    server_socket.sendto(response.pack(), addr)
  else:
    packet = response.pack()
    server_socket.sendall(struct.pack("!H",len(packet)) + packet)