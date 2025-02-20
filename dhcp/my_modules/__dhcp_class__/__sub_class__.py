from dataclasses import dataclass

@dataclass
class ClientData:
  mac_address: str
  client_id: str|None = None
  
  def is_mutch(self, dic:dict) -> bool:
    return (self.mac_address == dic.get("mac_address")) and (self.client_id == dic.get("client_id"))
  
@dataclass
class RequestData:
  hostname:str|None=None
  ip_address:str|None=None
  ttl:int|None=None
  
  @classmethod
  def from_bytes(cls, hostname:bytes|None, ip_address:str|None, ttl:bytes|None):
    new_instance = cls()
    if hostname != None:
      new_instance.hostname = hostname.decode()
    new_instance.ip_address = ip_address
    if ttl != None:
      new_instance.ttl = int.from_bytes(ttl)
    print(new_instance)
    return new_instance