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
                                                                                                                         
     VR CREATION                                                                                                                    

""")

#Variables
username = input ("Enter Username: ")
password = input ("Enter Password: ")
gwprivate = input ("Give the private subnet gateway: ")
gwpublic = input ("Give the public subnet gateway: ")

base_url = "https://100.70.0.20/restapi/v10.2/Network/VirtualRouters"

target_templates = []
counter=0

while counter<2:
    user_input = input("Enter a template (or 'quit' to stop): ")
    
    if user_input.lower() == "quit":
        break
    
    target_templates.append(user_input)
    
    counter = counter+1
    
for x in target_templates:
    url = f"{base_url}?location=template&template="+x+"&name=default"

    payload = {
        "entry": {
            "@name": "default",
            "@template": x,
            "@vsys": "vsys1",
            "interface": {
                "member": [
                "ethernet1/2",
                "ethernet1/3"
                ]
              },
            "routing-table": {
               "ip": { 
                "static-route": { 
                
                    "entry":   [
                        {
                            "@name": "Default",
                            "destination": "0.0.0.0/0",
                            "interface": "ethernet1/2",
                            "nexthop": {
                                "ip-address": gwpublic
                                },
                            "admin-dist": 10,
                            "metric": 10
                            },
                            
                      {
   
                            "@name": "RFC1918-a",
                            "destination": "192.168.0.0/16",
                            "interface": "ethernet1/3",
                            "nexthop": {
                                "ip-address": gwprivate
                                },
                            "admin-dist": 10,
                            "metric": 10
                              },
                              {
   
                            "@name": "RFC1918-b",
                            "destination": "172.16.0.0/12",
                            "interface": "ethernet1/3",
                            "nexthop": {
                                "ip-address": gwprivate
                                },
                            "admin-dist": 10,
                            "metric": 10
                              },
                              {
   
                            "@name": "RFC6598",
                            "destination": "100.70.0.0/15",
                            "interface": "ethernet1/3",
                            "nexthop": {
                                "ip-address": gwprivate
                                },
                            "admin-dist": 10,
                            "metric": 10
                              },
                              {
   
                            "@name": "RFC1918-c",
                            "destination": "100.70.0.0/15",
                            "interface": "ethernet1/3",
                            "nexthop": {
                                "ip-address": gwprivate
                                },
                            "admin-dist": 10,
                            "metric": 10
                              }
                            ]
                           
                         }
                      }
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