from os import _exit as exit
import traceback

from requests import post as post_unit
from dnslib import DNSRecord, DNSLabel, RR, DNSQuestion
from my_modules.__my_modules__ import converter

def post(path, json:dict|None=None):
  response = post_unit("http://rails:3000/dns/" + path, json=json, headers={"Content-Type": "application/json"})
  if response.status_code == 200:
    return response.json()
  else:
    try:
      sent_exception = response.json()["exception"]
      raise BaseException(f"\nstatus {response.status_code}\n{sent_exception}")
    except:
      traceback.print_exc()
      exit(1)

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
    data["ip_address"] = new_domain_label.idna()
  else:
    path = "search-ip"
    data["hostname"] = ".".join([unit.decode("idna") for unit in new_domain_label.label[:-3]])
  response = post(path, data)
  if response == None:
    record.header.set_rcode(3)
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