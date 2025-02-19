import struct, socket
from dnslib import DNSRecord

from my_modules.__my_modules__.__my_exit__ import add_before_tasks, exit

def from_global(header, question, callback, server_socket, addr):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    client.connect(("1.1.1.1", 53))
    packet = DNSRecord(header=header, questions=[question]).pack()
    client.sendall(struct.pack("!H",len(packet)) + packet)
    response = client.recv(1024)
    length = struct.unpack("!H",bytes(response[:2]))[0]
    while len(response) - 2 < length:
      response += client.recv(1024)
    callback(DNSRecord.parse(response[2:]), server_socket, addr)
    client.close()
  except:
    add_before_tasks(client.close)
    exit()