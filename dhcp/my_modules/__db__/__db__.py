from requests import post as post_unit

from my_modules.__dhcp_class__.__sub_class__ import ClientData, RequestData

def post(path, json:dict|None=None):
  print
  response = post_unit("http://localhost:3000/dhcp/" + path, json={"host": json}, headers={"Content-Type": "application/json"})
  if response.status_code == 200:
    print("posted:", path, response.json())
    return response.json()
  else:
    sent_exception = response.json()["exception"]
    raise BaseException(f"\nstatus {response.status_code}\n{sent_exception}")

def erase_data(client_data:ClientData):
  post("erase", client_data.__dict__)

def search_data(arg:ClientData|str)->dict|str|None:
  """
  When type(arg) == str, the value must be IPv4.
  In this case, the type of the return value will be dict|None.
  If the input Ipv4 address exists in database, the return value will be the client infomation dict, and if not so, the return value will be None.
  
  When type(arg) == ClientData,
  if such a device exists, the return value will be the IPv4 address of the device that has the input client data,
  otherwise the return value will be None.
  """
  if isinstance(arg, ClientData):
    return post("search-from-client-data", arg.__dict__)
  elif isinstance(arg, str):
    return post("search-from-ip", {"ip_address": arg})

def set_data(client_data:ClientData, request_data:RequestData):
  if request_data.ip_address == None:
    raise TypeError("Value of request_data.ip_address is requiered")
  post("set", {**client_data.__dict__, **request_data.__dict__})
  print(f"db.set_data()\n  {client_data}\n  {request_data}")