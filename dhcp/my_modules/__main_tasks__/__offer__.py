from .__imports__ import DEFAULT_TTL, MyDHCP, IP_RANGE, search_data, set_data

def create_ip(dhcp_data:MyDHCP) -> str:
  client_data = dhcp_data.get_client_data()
  saved_ip_address = search_data(client_data)["ip_v4"]
  if saved_ip_address == None:
    while True:
      new_ip = IP_RANGE.get_random_ip()
      if search_data(new_ip) == None:
        return new_ip
  else:
    return saved_ip_address

def offer(dhcp_data:MyDHCP) -> bytes:
  print("called offer")
  if dhcp_data.get_option(51) == None:
    dhcp_data.set_option(51, DEFAULT_TTL.to_bytes(4))
  print(dhcp_data.get_option(51).hex())
  requested_ip = dhcp_data.get_ip_address_from_option(50)
  print("requested ip:", requested_ip)
  if requested_ip == None:
    dhcp_data.your_ip = create_ip(dhcp_data)
    print("Condition 1 created and add new ip.")
  else:
    print("offer()", requested_ip)
    client_data = dhcp_data.get_client_data()
    if IP_RANGE.is_includes(requested_ip):
      saved_client_data = search_data(requested_ip)
      if saved_client_data == None:
        dhcp_data.your_ip = requested_ip
        print("Condition 2-1-1 added requested ip to DB.")
      else:
        if client_data.is_mutch(saved_client_data):
          dhcp_data.your_ip = requested_ip
          print("Condition 2-1-2-1 sent client data was mutched with data in DB,\nand updated ttl", requested_ip)
        else:
          print("Condition 2-1-2-2 duplicate IP:", requested_ip)
          dhcp_data.your_ip = create_ip(dhcp_data)
          print("updated ip in DB:", dhcp_data.your_ip)
    else:
      saved_ip = search_data(client_data)["ip_v4"]
      if saved_ip == None:
        dhcp_data.your_ip = create_ip(dhcp_data)
      else:
        dhcp_data.your_ip = saved_ip
      print("Condition 2-2 offered to:", dhcp_data.your_ip)
  return dhcp_data.save().set_mode(2).to_bytes()