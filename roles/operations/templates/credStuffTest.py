import requests
import collections
credDict = collections.OrderedDict()
requests.packages.urllib3.disable_warnings()
url = "https://{{ bigip_mgmt_vip_ip }}/mgmt/shared/authn/login"
credDict['superuser'] = 'superpass'
credDict['superduser'] = 'supedrpass'
credDict['supderuser'] = 'superpadss'
credDict['superduser'] = 'supderpass'
credDict['admin'] = 'admin'
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