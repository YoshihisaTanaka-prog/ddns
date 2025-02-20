from http.server import SimpleHTTPRequestHandler as Handler
from dataclasses import dataclass
from typing import TypeVar
import json

T = TypeVar("(params:BaseType, handler:Handler)->dict[str,Any]|(dict[str,Any], int) ")

class PostMethod:
  params_type:type
  method:callable
  def __init__(self, params_type, method):
    self.params_type = params_type
    self.method = method
      
  def invoke(self, handler):
    length = int(handler.headers["Content-Length"])
    params_json = handler.rfile.read(length).decode("utf-8")
    params_dict = json.loads(params_json)
    response_data = self.method(self.params_type(**params_dict), handler)
    if isinstance(response_data, tuple):
      handler.send_response(response_data[1])
      handler.send_header("Content-type", "application/json")
      handler.end_headers()
      handler.wfile.write(json.dumps(response_data[0]).encode())
    else:
      handler.send_response(200)
      handler.send_header("Content-type", "application/json")
      handler.end_headers()
      handler.wfile.write(json.dumps(response_data).encode())

class PostMethodDict(dict[str, PostMethod]):
  def __init__(self):
    super().__init__()
  
  def invoke(self, handler:Handler):
    pm = self.get(handler.path)
    if pm == None:
      handler.send_error(404, "Not Found")
    else:
      pm.invoke(handler)
    
  def set_method(self, path:str, params_type:type, method:T):
    self[path] = PostMethod(params_type, method)
    
post_method_dict = PostMethodDict()

@dataclass
class BaseType:
  def __init__(self, **kwargs):
    pass