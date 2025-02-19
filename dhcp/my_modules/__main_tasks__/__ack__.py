from .__imports__ import MyDHCP, IP_RANGE, search_data
from .__nak__ import nak

def ack_for_request(sent_data:bytes) -> bytes:
  print("called ack")
  judge, dhcp_data = MyDHCP.create_for_ack(sent_data)
  if judge:
    requested_ip = dhcp_data.get_ip_address_from_option(50)
    if requested_ip == None:
      print("Condition 1 non IP")
      return nak(dhcp_data)
    else:
      client_data = dhcp_data.get_client_data()
      saved_client_data = search_data(requested_ip)
      if saved_client_data == None:
        print("Condition 2-1 sent client data was not saved in DB")
        return nak(dhcp_data)
      else:
        if client_data.is_mutch(saved_client_data):
          dhcp_data.your_ip = requested_ip
          if saved_client_data["ip_address"] == requested_ip:
            print("Condition 2-2-1-1 sent client data was mutched with data in db")
            return dhcp_data.save().set_mode(5).to_bytes()
          else:
            print("Condition 2-2-1-2 sent client data was missmutched with data in db")
            return nak(dhcp_data)
        else:
          print("Condition 2-2-2 duplicate IP", requested_ip)
          return nak(dhcp_data)
  else:
    print("Request was not for this server")
    return nak(dhcp_data)

def ack_for_inform(dhcp_data:MyDHCP):
  dhcp_data.your_ip = "0.0.0.0"
  return dhcp_data.set_mode(5).to_bytes()