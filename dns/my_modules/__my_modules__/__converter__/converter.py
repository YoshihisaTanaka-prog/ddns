from os import environ as env
from copy import deepcopy as copy

from dnslib import DNSRecord, DNSHeader, DNSQuestion, DNSLabel, RR

LOCAL_DOMAIN_SUFFIX = list(DNSLabel(env.get('LOCAL_DOMAIN_SUFFIX')).label)
LOCAL_PTR_LABEL_BASE= [b"in-addr", b"arpa"]
LOCAL_PTR_LABELS = []
network_ip_array = [item for item in env["NETWORK_IP"].split(".")]
subnet_mask_array = [item for item in env["SUBNET_MASK"].split(".")]
for i in range(4):
  if subnet_mask_array[i] == "255":
    LOCAL_PTR_LABEL_BASE.insert(0, network_ip_array[i].encode())
  elif subnet_mask_array[i] == "0":
    LOCAL_PTR_LABELS.append(DNSLabel(LOCAL_PTR_LABEL_BASE))
    break
  else:
    mask_num = int(subnet_mask_array[i])
    target_num = mask_num & int(network_ip_array[i])
    for j in range(256):
      if (j & mask_num) == target_num:
        LOCAL_PTR_LABELS.append(DNSLabel([str(j).encode()] + LOCAL_PTR_LABEL_BASE))
    break

class MyQuestion:
  def __init__(self, h:DNSHeader, q:DNSQuestion, new_label, is_local:bool):
    self.q = q
    self.h = h
    self.new_label = new_label
    self.is_local = is_local
  @classmethod
  def get_local(cls, new_label: DNSLabel, header:DNSHeader, question: DNSQuestion):
    return cls(header, question, new_label, True)
  @classmethod
  def get_global(cls, header:DNSHeader, question: DNSQuestion):
    return cls(header, question, question.qname, False)

def request(data) -> MyQuestion:
  record = DNSRecord.parse(data)
  header = record.header
  question = record.questions[0]
  label = question.get_qname()
  if len(label.label) == 1:
    new_label = DNSLabel(list(label.label) + LOCAL_DOMAIN_SUFFIX)
    return MyQuestion.get_local(new_label, header, question)
  elif label.label[-2] == b"in-addr":
    for local_ptr_label in LOCAL_PTR_LABELS:
      if label.matchSuffix(local_ptr_label):
        return MyQuestion.get_local(label, header, question)
    return MyQuestion.get_global(header, question)
  else:
    if label.matchSuffix("search.local"):
      return MyQuestion.get_global(header, question)
    else:
      insert_label = []
      search_label = copy(LOCAL_DOMAIN_SUFFIX)
      while(len(search_label) > 0):
        if label.matchSuffix(search_label):
          new_label = DNSLabel(list(label.label)[:-len(search_label)] + insert_label + search_label)
          return MyQuestion.get_local(new_label, header, question)
        insert_label.append(search_label[0])
        search_label = search_label[1:]
      return MyQuestion.get_global(header, question)
  
def auth_rr(my_dict:dict, domain_label:DNSLabel=DNSLabel(LOCAL_DOMAIN_SUFFIX))->list[RR]:
  zone = f"{domain_label} {my_dict["minimum"]} IN SOA {my_dict['primary']} {my_dict['admin']} {my_dict['serial']} {my_dict['refresh']} {my_dict['retry']} {my_dict['expire']} {my_dict['minimum']}"
  return RR.fromZone(zone)

def get_cache_params(question: DNSQuestion)->dict:
  return_dict = {}
  return_dict["domain"] = question.get_qname().idna()
  return_dict["record_type"] = question.qtype
  return_dict["record_class"] = question.qclass
  return return_dict

def set_auth_params(auth_list:list[RR])->dict:
  return_list = []
  for auth in auth_list:
    item_dict = {}
    item_dict["primary"] = auth.rdata.mname.idna()
    item_dict["admin"] = auth.rdata.rname.idna()
    item_dict["value"] = auth.toZone()
    item_dict["ttl"] = auth.ttl
    return_list.append(item_dict)
  return return_list

def set_answer_params(answer_list:list[RR])->dict:
  return_list = []
  for answer in answer_list:
    splitted_zone = [item for item in answer.toZone().split(f" ") if item != ""]
    return_list.append({"value1": splitted_zone[0], "value2": f" ".join(splitted_zone[2:]), "ttl": answer.ttl})
  return return_list

def set_cache_params(recode: DNSRecord)->dict:
  return_dict = {}
  question_dict = {}
  question = recode.questions[0]
  question_dict["domain"] = question.get_qname().idna()
  question_dict["record_type"] = question.qtype
  question_dict["record_class"] = question.qclass
  return_dict["question"] = question_dict
  return_dict["s_o_as"] = set_auth_params(recode.auth)
  return_dict["zones"] = set_answer_params(recode.rr)
  return return_dict

def auth_rr_list(zones:list[str])->list[RR]:
  return_array = []
  for zone in zones:
    return_array.extend(RR.fromZone(zone))
  return return_array
  
def answer_rr_list(zones:list[str])->list[RR]:
  return_array = []
  try:
    for zone in zones:
      return_array.extend(RR.fromZone(zone))
  finally:
    return return_array

def answer_recode(record:DNSRecord, my_dict:dict)->DNSRecord:
  record.add_auth(*auth_rr_list(my_dict["s_o_as"]))
  record.add_answer(*answer_rr_list(my_dict["zones"]))
  return record