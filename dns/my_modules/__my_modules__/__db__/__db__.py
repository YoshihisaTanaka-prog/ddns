from requests import post as post_unit
from dnslib import DNSRecord, DNSLabel, RR, DNSQuestion
from my_modules import converter

def post(path, json:dict|None=None) -> dict:
  response = post_unit("http://rails:3000/dns/" + path, json=json, headers={"Content-Type": "application/json"})
  if response.status_code == 200:
    return response.json()
  else:
    raise Exception(f"Error fetching settings: {response.text}")

def get_my_soa(domain_label: DNSLabel|None=None) -> RR|None:
  auth_response = post_unit("http://rails:3000/get-settings/soa", headers={"Content-Type": "application/json"})
  if auth_response.status_code == 200:
    return converter.auth(auth_response.json(), domain_label)
  else:
    raise Exception(f"Error fetching SOA record: {auth_response.text}")

def search_local(header, question, new_domain_label: DNSLabel) -> DNSRecord:
  record = DNSRecord(header=header, questions=[question]).reply()
  record.add_auth(*get_my_soa(new_domain_label))
  path = None
  data = {}
  if new_domain_label.matchSuffix("in-addr.arpa"):
    path = "search-host"
    data["ipv4"] = new_domain_label.idna()
  else:
    path = "search-ipv4"
    data["hostname"] = ".".join([unit.decode("idna") for unit in new_domain_label.label[:-3]])
  response_dict = post(path, data)
  if response_dict["answer"] == None:
    record.header.set_rcode(3)
  return record

def search_cache(header, question:DNSQuestion) -> DNSRecord|None:
  record = DNSRecord(header=header, questions=[question]).reply()
  response_dict = post("search-cache", converter.get_cache_params(question))
  if response_dict == None:
    return None
  else:
    return record

def set_cache(record: DNSRecord) -> None:
  print(record)