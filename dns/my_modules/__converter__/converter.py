from os import environ as env
from copy import deepcopy as copy

from dnslib import DNSRecord, DNSHeader, DNSQuestion, DNSLabel

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

DNSQuestion()

class MyQuestion:
  def __init__(self, h:DNSHeader, q:DNSQuestion, is_local:bool):
    self.q = q
    self.h = h
    self.is_local = is_local
  @classmethod
  def get_local(cls, label: DNSLabel, header:DNSHeader, question: DNSQuestion):
    return cls(header, DNSQuestion(str(label), question.qtype, question.qclass), True)
  @classmethod
  def get_global(cls, header:DNSHeader, question: DNSQuestion):
    return cls(header, question, False)

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
    insert_label = []
    search_label = copy(LOCAL_DOMAIN_SUFFIX)
    while(len(search_label) > 0):
      if label.matchSuffix(search_label):
        new_label = DNSLabel(list(label.label)[:-len(search_label)] + insert_label + search_label)
        return MyQuestion.get_local(new_label, header, question)
      insert_label.append(search_label[0])
      search_label = search_label[1:]
    return MyQuestion.get_global(header, question)