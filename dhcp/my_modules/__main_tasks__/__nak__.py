from .__imports__ import MyDHCP

def nak(dhcp_data:MyDHCP) -> bytes:
  print("called nak", ":".join([num.to_bytes(1).hex() for num in dhcp_data.client_hard_address]))
  return dhcp_data.set_mode(6).to_bytes()