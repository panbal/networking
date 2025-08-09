import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("""

  _   _ _________          ___  __  _______                                   _                        _   _             
 | \ | |__   __\ \        / / |/ / |__   __|                       /\        | |                      | | (_)            
 |  \| |  | |   \ \  /\  / /| ' /     | | ___  __ _ _ __ ___      /  \  _   _| |_ ___  _ __ ___   __ _| |_ _  ___  _ __  
 | . ` |  | |    \ \/  \/ / |  <      | |/ _ \/ _` | '_ ` _ \    / /\ \| | | | __/ _ \| '_ ` _ \ / _` | __| |/ _ \| '_ \ 
 | |\  |  | |     \  /\  /  | . \     | |  __/ (_| | | | | | |  / ____ \ |_| | || (_) | | | | | | (_| | |_| | (_) | | | |
 |_| \_|  |_|      \/  \/   |_|\_\    |_|\___|\__,_|_| |_| |_| /_/    \_\__,_|\__\___/|_| |_| |_|\__,_|\__|_|\___/|_| |_|
                                                                                                                         
     ZONE CREATION                                                                                                                    

""")
apikey = input("Put your API key: ")
coid = input("Put the COID: ")
coid = coid.lower()
counter=0
target_templates = []
while counter<2:
    user_input = input("Enter a template (or 'quit' to stop): ")
    
    if user_input.lower() == "quit":
        break
    
    target_templates.append(user_input)
    
    counter = counter+1


for x in target_templates:

    payload1 = json.dumps({
      "entry": {
        "@name": coid+"-internal",
        "@location": "template",
        "@template": x,
        "@vsys": "vsys1",
        "network": {
          "layer3": {
                
            "member":"ethernet1/3"
                },
          "log-setting": "none"
        }
      }
    })

    url = ("https://100.70.0.20/restapi/v10.2/Network/Zones?location=template&template="+x+"&vsys=vsys1&name="+coid+"-internal")
    headers = {
      'Content-Type': 'application/json',
      'X-PAN-KEY': 'LUFRPT1icU8wL3RsU0JUZERqS2JpMnBGQ1JxbWdVMmc9a2I5NmQ5ay9tVCs4QVFQcW1ZNGV2REErN3dzVW9yVE1CQUdYbXRKdXM1NnNzdXIraDFQY2R1UWxnSDZkQnZWdg=='
    }
    
    response1 = requests.request("POST", url, headers=headers, data=payload1, verify=False)
    
    print(x,"\n",response1.text,"\n")
    
for y in target_templates:

    payload2 = json.dumps({
      "entry": {
        "@name": coid+"-external",
        "@location": "template",
        "@template": x,
        "@vsys": "vsys1",
        "network": {
          "layer3": {
                
            "member":"ethernet1/2"
                },
          "log-setting": "none"
        }
      }
    })

    url = ("https://100.70.0.20/restapi/v10.2/Network/Zones?location=template&template="+x+"&vsys=vsys1&name="+coid+"-external")
    headers = {
      'Content-Type': 'application/json',
      'X-PAN-KEY': apikey
    }
    

    response2 = requests.request("POST", url, headers=headers, data=payload2, verify=False)

    print(x,"\n",response2.text,"\n")