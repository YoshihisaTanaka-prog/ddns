import socket
import struct
from dnslib import DNSRecord

def from_global(header, question, callback, server_socket, addr) -> DNSRecord:
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  client.bind(("0.0.0.0", 53535))
  client.connect(("1.1.1.1", 53))
  packet = DNSRecord(header=header, questions=[question]).pack()
  client.sendall(struct.pack("!H",len(packet)) + packet)
  response = client.recv(1024)
  length = struct.unpack("!H",bytes(response[:2]))[0]
  while len(response) - 2 < length:
    response += client.recv(1024)
  record = DNSRecord.parse(response[2:])
  callback(record, server_socket, addr)
  client.close()