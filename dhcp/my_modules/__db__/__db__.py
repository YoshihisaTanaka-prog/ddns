from requests import post as post_unit

from my_modules.__client_data__.client_data import ClientData

def post(path, json:dict|None=None) -> dict:
  response = post_unit("http://rails:3000/dhcp/" + path, json={"host": json}, headers={"Content-Type": "application/json"})
  if response.status_code == 200:
    return response.json()
  else:
    sent_exception = response.json()["exception"]
    raise BaseException(f"\nstatus {response.status_code}\n{sent_exception}")

def erase_data(client_data:ClientData):
  post("erase", client_data.__dict__)

def search_from_client_data(client_data:ClientData):
  return post("search-from-client-data", client_data.__dict__)

def search_from_ip(ip_address:str):
  return post("search-from-ip", {"ip_address": ip_address})

def set_data(client_data:ClientData, hostname:str, ip_address:str, ttl:int|None=None):
  param_dict = client_data.__dict__
  param_dict["hostname"] = hostname
  param_dict["ip_address"] = ip_address
  param_dict["ttl"] = ttl
  post("set", param_dict)