import struct
from .__my_modules__ import converter, db, searcher
from dnslib import DNSRecord, QTYPE

def send_response(response, server_socket, addr):
  if addr:
    server_socket.sendto(response.pack(), addr)
  else:
    packet = response.pack()
    server_socket.sendall(struct.pack("!H",len(packet)) + packet)
    
def on_get_response(response:DNSRecord, socket, addr):
  send_response(response, socket, addr)
  db.set_cache(response)

def main_task(data, socket, addr=None):
  request = converter.request(data)
  if addr == None:
    print("TCP: requested:", request.new_label.idna(), QTYPE.forward[request.q.qtype])
  else:
    print("UDP: requested:", request.new_label.idna(), QTYPE.forward[request.q.qtype])
  if request.is_local:
    result = db.search_local(request.h, request.q, request.new_label)
    send_response(result, socket, addr)
  else:
    result = db.search_cache(request.h, request.q)
    if result == None:
      searcher.from_global(request.h, request.q, on_get_response, socket, addr)
    else:
      send_response(result, socket, addr)
  
__all__ = ['main_task']