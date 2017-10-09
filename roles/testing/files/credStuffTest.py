import requests

url = "https://10.128.10.122/mgmt/shared/authn/login"

payload = "{\n  \"username\": \"sdddfad\",\n  \"password\": \"sdf\",\n  \"loginProvidername\":\"tmos\"\n}\n"
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "a87e9e73-a4a6-a339-7c6a-97fde91fa140"
    }

response = requests.request("POST", url, data=payload, headers=headers, verify=False)

print(response.text)
