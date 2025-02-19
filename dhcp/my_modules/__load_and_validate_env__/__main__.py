from os import getenv
from json import loads as json_parse

def validate():
  router_ip = getenv("ROUTER_IP")
  if router_ip == None:
    raise TypeError("Environment variable ROUTER_IP is not set")
  network_ip = getenv("NETWORK_IP")
  if network_ip == None:
    raise TypeError("Environment variable NETWORK_IP is not set")
  subnet_mask = getenv("SUBNET_MASK")
  if subnet_mask == None:
    raise TypeError("Environment variable SUBNET_MASK is not set")
  soa_data_json = getenv("SOA_DATA")
  if soa_data_json == None:
    raise TypeError("Environment variable SOA_DATA is not set")
  soa_data = json_parse(soa_data_json)
  return soa_data["minimum"], getenv("DOMAIN_SUFFIX", ""), getenv("HOST_NAME", ""), network_ip, router_ip, subnet_mask
  
DEFAULT_TTL, DOMAIN_SUFFIX, HOST_NAME, NETWORK_IP, ROUTER_IP, SUBNET_MASK = validate()