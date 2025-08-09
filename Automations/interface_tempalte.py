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
                                                                                                                         
     INTERFACE CREATION                                                                                                                    

""")

#Variables
username = input ("Enter Username: ")
password = input ("Enter Password: ")
coid = input ("Enter COID: ")
coid=coid.lower()

base_url = "https://100.70.0.20/restapi/v10.2/Network/EthernetInterfaces"


target_templates = []
counter=0

while counter<2:
    user_input = input("Enter a template (or 'quit' to stop): ")
    
    if user_input.lower() == "quit":
        break
    
    target_templates.append(user_input)
    
    counter = counter+1
    
############This Creates the HA interface####################

for x in target_templates:
    url = f"{base_url}?location=template&template="+x+"&name=ethernet1/1"
    
    payload = {
        "entry": {
            "@name": "ethernet1/1",
            "@template": x,
            "@vsys": "vsys1",
            "ha": {

            }
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

    print(f"Template: {x}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")
    
############This Creates the Public interface####################

    
for y in target_templates:
    url = f"{base_url}?location=template&template="+y+"&name=ethernet1/2"
    
    payload = {
        "entry": {
            "@name": "ethernet1/2",
            "@template": y,
            "@vsys": "vsys1",
            "layer3": {
                "dhcp-client":{
                    "enable": "yes",
                    "create-default-route": "no"
                    },
                 "adjust-tcp-mss": {
                    "enable":"yes",
                    "ipv4-mss-adjustment":140
                    }
                  },
            "comment":coid+"-external"
            

            
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

    print(f"Template: {y}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")


############This Creates the Private interface####################
    
for z in target_templates:
    url = f"{base_url}?location=template&template="+z+"&name=ethernet1/3"
    
    payload = {
        "entry": {
            "@name": "ethernet1/3",
            "@template": z,
            "@vsys": "vsys1",
            "layer3": {
                "dhcp-client":{
                    "enable": "yes",
                    "create-default-route": "no"
                    },
                 "adjust-tcp-mss": {
                    "enable":"yes",
                    "ipv4-mss-adjustment":140
                    }
                   },
            "comment":coid+"-internal"
            

            
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

    print(f"Template: {z}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")