from my_modules.__load_and_validate_env__  import ROUTER_IP, SUBNET_MASK, DOMAIN_SUFFIX, HOST_NAME
from my_modules.__ip_address__ import IP_RANGE
from my_modules.__db__ import set_data
from .__sub_class__ import ClientData, RequestData

def to_ip(data: bytes) -> str:
  return f"{int.from_bytes(data[0:1])}.{int.from_bytes(data[1:2])}.{int.from_bytes(data[2:3])}.{int.from_bytes(data[3:4])}"

def from_ip(ip_address: str) -> bytes:
  return bytes([int(n) for n in ip_address.split('.')])

class MyDHCPOptions(dict[int, bytes]):
  def __init__(self, data: bytes):
    super().__init__()
    index = 0
    code = data[index]
    while code != 255:
      length = data[index+1]
      self[code] = data[index+2:index+length+2]
      if code == 55:
        print([num for num in data[index+2:index+length+2]])
      index += length+2
      code = data[index]
  
  def set_mode(self, mode):
    self[53] = mode.to_bytes()
    self[54] = from_ip(ROUTER_IP)
    self[1] = from_ip(SUBNET_MASK)
    self[2] = (9*3600).to_bytes(4, signed=True)
    # print("time offset", int.from_bytes(self[2], signed=True))
    self[3] = from_ip(ROUTER_IP)
    self[6] = from_ip(ROUTER_IP)
    if DOMAIN_SUFFIX != "":
      self[15] = DOMAIN_SUFFIX.encode()
      ba119 = bytearray([])
      for domain_suffix_item in DOMAIN_SUFFIX.split("."):
        ba119 += len(domain_suffix_item).to_bytes()
        ba119 += domain_suffix_item.encode()
      self[119] = ba119 + b"\x00"
    self[26] = (1500).to_bytes(2)
    self[28] = bytes([unit.end for unit in IP_RANGE])
    if self.get(50) != None:
      del self[50]
    self[66] = from_ip(ROUTER_IP)
    self[121] = b"\x00\xc0\xa8\x04\x01"
    self[249] = b"\x00\xc0\xa8\x04\x01"

  def set(self, code: int, value:bytes|bytearray|str|int|None):
    if code > 0 and code < 256:
      if value == None:
        del self[code]
      else:
        if isinstance(value, int):
          bit_len = value.bit_length()
          byte_len = (bit_len + 7) // 8
          self[code] = value.to_bytes(byte_len)
        elif isinstance(value, str):
          self[code] = value.encode() + b"\x00"
        elif isinstance(value, bytes):
          self[code] = value
        else:
          self[code] = bytes(value)
        
  def to_bytes(self) -> bytes:
    return_value = bytearray([53, 1, self[53][0]])
    for code in sorted(self.keys()):
      if code in [53, 55]:
        continue
      value = self[code]
      return_value += bytes([code, len(value)])
      return_value += value
    return bytes(return_value) + b"\xff"

class MyDHCP:
  @classmethod
  def create_for_ack(cls, data:bytes):
    new_instance = cls(data)
    print("MyDHCP.create_for_ack:", to_ip(data[20:24]))
    if to_ip(data[20:24]) in (ROUTER_IP, "0.0.0.0"):
      return (True, new_instance)
    else:
      return (False, new_instance)
    
  def __init__(self, data:bytes):
    self.init_data = b"\x02" + data[1:8] + bytes([0,0]) + data[10:12]
    self.client_ip = to_ip(data[12:16])
    self.your_ip = to_ip(data[16:20])
    self.server_ip = ROUTER_IP
    self.client_hard_address = data[28:44]
    self.server_name = HOST_NAME
    self.options = MyDHCPOptions(data[240:])
    self.display_me()
    
  def display_me(self):
    print(f"message type: {int.from_bytes(self.options.get(53))}\nxid: {self.init_data[4:8].hex()}\nmac address: {":".join([num.to_bytes(1).hex() for num in self.client_hard_address])}\noptions:")
    for key, value in self.options.items():
      print(f"  {key}: {value.hex()}")
    
  def get_option(self, code: int) -> bytes|None:
    return self.options.get(code)
  
  def get_ip_address_from_option(self, code:int) -> str|None:
    value = self.options.get(code)
    print(value)
    if value == None:
      return None
    elif len(value) == 4:
      return to_ip(value)
    
  def set_option(self, code:int, value:bytes|bytearray|str|int|None=None):
    self.options.set(code, value)
    return self
  
  def set_ip_to_option(self, code: int, ip_address:str):
    self.options.set(code, from_ip(ip_address))
    return self
  
  def set_mode(self, mode:int):
    if (mode > 0) and (mode < 9):
      self.options.set_mode(mode)
    return self
  
  def get_message_type(self) -> int:
    return self.get_option(53)[0]
  
  def to_bytes(self) -> bytes:
    data = bytearray(self.init_data)
    data.extend(from_ip(self.client_ip))
    data.extend(from_ip(self.your_ip))
    data.extend(from_ip(self.server_ip))
    data.extend((0).to_bytes(4))
    data.extend(self.client_hard_address)
    data.extend(self.server_name.encode())
    length1 = len(data)
    data.extend((0).to_bytes(236 - length1))
    data.extend(b"\x63\x82\x53\x63")
    data.extend(self.options.to_bytes())
    length2 = len(data)
    if length2 < 300:
      data.extend((0).to_bytes(300 - length2))
    return bytes(data)
  
  def get_client_data(self) -> ClientData:
    hard_ware_length = self.init_data[2]
    mac_address_text = ":".join([num.to_bytes(1).hex() for num in self.client_hard_address[0:hard_ware_length]])
    op61 = self.get_option(61)
    if op61 == None:
      return ClientData(mac_address_text)
    else:
      return ClientData(mac_address_text, op61.hex())
  
  def get_requested_data(self):
    op81 = self.get_option(81)
    allow_nums = [45, 46, 95] + [num for num in range(48, 58)] + [num for num in range(65, 91)] + [num for num in range(97, 123)]
    if op81 == None:
      op12 = self.get_option(12)
      if op12 == None:
        return RequestData.from_bytes(None, self.your_ip, self.get_option(51))
      else:
        host_name = bytes([num for num in op12 if num in allow_nums])
        return RequestData.from_bytes(host_name, self.your_ip, self.get_option(51))
    else:
      host_name = bytes([num for num in op81 if num in allow_nums])
      return RequestData.from_bytes(host_name, self.your_ip, self.get_option(51))
    
  def save(self):
    set_data(self.get_client_data(), self.get_requested_data())
    return self