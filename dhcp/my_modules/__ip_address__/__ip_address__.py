from dataclasses import dataclass
from random import randint

from my_modules.__load_and_validate_env__ import NETWORK_IP, SUBNET_MASK

@dataclass
class IpRangeUnit:
  begin:int
  end:int
  def get_random_item(self):
    if self.begin == self.end:
      return f"{self.begin}"
    else:
      return f"{randint(self.begin+1, self.end-1)}"
  def is_includes(self, num):
    if (num < self.begin) or (num > self.end):
      return False
    else:
      return True
  
class IpRange(tuple[IpRangeUnit]):
  def __new__(cls):
    network_ip = [int(item) for item in NETWORK_IP.split(".")]
    subnet_mask = [int(item) for item in SUBNET_MASK.split(".")]
    my_value:list[IpRangeUnit] = []
    for i in range(4):
      if subnet_mask[i] == 0:
        my_value.append(IpRangeUnit(0, 255))
      elif subnet_mask[i] == 255:
        my_value.append(IpRangeUnit(network_ip[i], network_ip[i]))
      else:
        subnet_mask_i = subnet_mask[i]
        criteria_byte = subnet_mask_i & network_ip[i]
        array = [num for num in range(1,255) if (subnet_mask_i & num) == criteria_byte]
        my_value.append(IpRangeUnit(array[0], array[-1]))
    return tuple.__new__(cls, my_value)
    
  def get_random_ip(self)->str:
    return ".".join([unit.get_random_item() for unit in self])
    
  def is_includes(self, ip_address:str|bytes) -> bool:
    if isinstance(ip_address, str):
      ip_array = [int(item) for item in ip_address.split(".")]
      if len(ip_array) == 4:
        for i in range(4):
          if self[i].is_includes(ip_array[i]) == False:
            return False
        return True
      else:
        raise TypeError(f"\"{ip_address}\" is not ip address")
    else:
      if len(ip_address) == 4:
        for i in range(4):
          if self[i].is_includes(ip_address[i]) == False:
            return False
        return True
      else:
        raise TypeError(f"\"{ip_address}\" is not ip address")
    
IP_RANGE = IpRange()