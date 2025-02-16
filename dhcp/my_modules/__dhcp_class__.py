from os import getenv

from .__client_data__.client_data import ClientData

ROUTER_IP = getenv("ROUTER_IP")
SUBNET_MASK = getenv("SUBNET_MASK")
if None in (ROUTER_IP, SUBNET_MASK):
  raise Exception("Required environment variable is not set.")
DOMAIN_SUFFIX = getenv("DOMAIN_SUFFIX", "")
HOST_NAME = getenv("HOST_NAME", "")

def to_ip(data: bytes) -> str:
  return f"{int.from_bytes(data[0:1])}.{int.from_bytes(data[1:2])}.{int.from_bytes(data[2:3])}.{int.from_bytes(data[3:4])}"

def from_ip(ip_address: str) -> bytes:
  return bytes([int(n) for n in ip_address.split('.')])

class MyDHCPOptions(dict[int, bytes]):
  def __init__(self, data: bytes):
    super().__init__()
    self.set(1, from_ip(SUBNET_MASK))
    self.set(6, from_ip(ROUTER_IP))
    if DOMAIN_SUFFIX != None:
      self.set(15, DOMAIN_SUFFIX.encode())
    self.set(53, data[2].to_bytes(1))
    self.set(66, from_ip(ROUTER_IP))
    index = 3
    code = data[index]
    while code != 255:
      length = data[index+1]
      if code not in (1, 6, 15, 53, 55, 66):
        value = data[index+2:index+length+2]
        self.set(code, value)
      index += length+2
      code = data[index]

  def set(self, code: int, value: bytes|bytearray|str):
    if code > 0 and code < 256 and code not in (1, 6, 15, 53, 55, 66):
      if isinstance(value, str):
        self[code] = value.encode()
      elif isinstance(value, bytes):
        self[code] = value
      else:
        self[code] = bytes(value)
        
  def to_bytes(self) -> bytes:
    return_value = bytearray([53,1,self[53][0]])
    for code in range(1, 255):
      if code == 53:
        continue
      value = self.get(code)
      if value != None:
        return_value += bytes([code, len(value)])
        return_value += value
    return bytes(return_value) + b"\xff"

class MyDHCP:
  def __init__(self, data:bytes):
    self.init_data = data[0:12]
    self.client_ip = to_ip(data[12:16])
    self.your_ip = to_ip(data[16:20])
    self.server_ip = ROUTER_IP
    self.client_hard_address = data[28:44]
    self.server_name = ""
    if (DOMAIN_SUFFIX != "") and (HOST_NAME != ""):
      self.server_name = f"{HOST_NAME}.{DOMAIN_SUFFIX}"
    self.options = MyDHCPOptions(data[240:])
    dic = self.__dict__
    print(dic)
    
  def set_option(self, code: int, value: bytes|bytearray|str) -> MyDHCP:
    self.options.set(code, value)
    return self
  
  def get_message_type(self) -> int:
    return self.options[53][0]
  
  def to_bytes(self) -> bytes:
    zero = 0
    data = self.init_data
    data += from_ip(self.client_ip)
    data += from_ip(self.your_ip)
    data += from_ip(self.server_ip)
    data += zero.to_bytes(4)
    data += self.client_hard_address
    data += self.server_name.encode()
    length1 = len(data)
    data += zero.to_bytes(236 - length1)
    data += b"\x63\x82\x53\x63"
    data += self.options.to_bytes()
    length2 = len(data)
    if length2 < 300:
      data += zero.to_bytes(300 - length2)
    return bytes(data)
  
  def get_client_data(self) -> ClientData:
    op61 = self.options.get(61)
    if op61 == None:
      return ClientData(self.client_hard_address.hex())
    else:
      return ClientData(self.client_hard_address.hex(), op61.hex())
