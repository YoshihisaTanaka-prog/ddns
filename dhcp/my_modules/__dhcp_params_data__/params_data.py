from dataclasses import dataclass

@dataclass
class ClientData:
  mac_address: str
  client_id: str|None = None