from .__imports__ import MyDHCP, erase_data

def release(dhcp_data:MyDHCP):
  erase_data(dhcp_data.get_client_data())