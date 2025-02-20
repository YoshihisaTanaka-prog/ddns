from socketserver import TCPServer
import os

from my_modules import post_method_dict, Handler

PORT = 8000
DIRECTORY = "public"

class CustomHandler(Handler):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=DIRECTORY, **kwargs)

  def do_GET(self):
    # `localhost:8000/` にアクセスされた場合、index.html を返す
    if self.path == "/":
      self.path = "/index.html"
    
    # `public` フォルダ内のファイルのみを許可
    requested_file = os.path.join(DIRECTORY, self.path.lstrip("/"))
    if not os.path.abspath(requested_file).startswith(os.path.abspath(DIRECTORY)):
      self.send_error(404, "Not Found")
      return
    
    super().do_GET()
    
  def do_POST(self):
    post_method_dict.invoke(self)

# サーバーを起動
with TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
  print(f"Serving at port {PORT}")
  httpd.serve_forever()
