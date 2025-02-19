from os import environ as env
from requests import post as post_unit
from dnslib import DNSRecord, DNSLabel, RR, DNSQuestion, CLASS, QTYPE

from my_modules.__my_modules__ import converter
from my_modules.__my_modules__.__my_exit__ import exit

LOCAL_DOMAIN_SUFFIX = env.get('LOCAL_DOMAIN_SUFFIX')

def post(path, json:dict|None=None):
  response = post_unit("http://rails:3000/dns/" + path, json=json, headers={"Content-Type": "application/json"})
  if response.status_code == 200:
    return response.json()
  else:
    try:
      sent_exception = response.json()["exception"]
      raise BaseException(f"\nstatus {response.status_code}\n{sent_exception}")
    except:
      exit()

def get_my_soa_dict() -> dict:
  auth_response = post_unit("http://rails:3000/get-settings/soa", headers={"Content-Type": "application/json"})
  if auth_response.status_code == 200:
    return auth_response.json()
  else:
    try:
      raise Exception(f"Error fetching SOA record: {auth_response.text}")
    except:
      exit()

def to_soas(dic:dict):
  return converter.auth(dic)

def search_local(header, question, new_domain_label: DNSLabel) -> DNSRecord:
  record = DNSRecord(header=header, questions=[question]).reply()
  my_soa_dic = get_my_soa_dict()
  my_soas = to_soas(my_soa_dic)
  record.add_auth(*my_soas)
  if new_domain_label.matchSuffix("in-addr.arpa"):
    response = post("search-host", {"ip_domain": new_domain_label.idna()})
    if response == None:
      record.header.set_rcode(3)
    else:
      zone = f"{new_domain_label.idna()} {my_soa_dic["minimum"]} {CLASS.forward[question.qclass]} PTR {response}.{LOCAL_DOMAIN_SUFFIX}"
      record.add_answer(*RR.fromZone(zone))
  else:
    host_names = [unit.decode("idna") for unit in new_domain_label.label[:-2]]
    host_name = ""
    if len(host_names) > 0:
      if (host_names[0] == "www") and (host_names[-1] == "com"):
        host_name = ".".join(host_names[1:-1])
      else:
        host_name = ".".join(host_names)
    response = post("search-ip", {"hostname": host_name})
    if response == None:
      record.header.set_rcode(3)
    elif question.qtype == 6:
      zone = f"{host_name}.{LOCAL_DOMAIN_SUFFIX} {my_soa_dic["minimum"]}"
      record.add_answer(*RR.fromZone(zone))
    elif question.qtype in (28, 65):
      record.header.set_rcode(3)
    else:
      zone = f"{host_name}.{LOCAL_DOMAIN_SUFFIX} {my_soa_dic["minimum"]} {CLASS.forward[question.qclass]} {QTYPE.forward[question.qtype]} {response}"
      print(zone)
      record.add_answer(*RR.fromZone(zone))
  return record

def search_cache(header, question:DNSQuestion) -> DNSRecord|None:
  response= post("search-cache", converter.get_cache_params(question))
  if response == None:
    return None
  else:
    record = DNSRecord(header=header, questions=[question])
    return converter.answer_recode(record, response)

def set_cache(record: DNSRecord) -> None:
  post("set", converter.set_cache_params(record))