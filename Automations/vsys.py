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
                                                                                                                         
     Add Interfaces to Virtual System                                                                                                                    

""")

#Variables
username = input ("Enter Username: ")
password = input ("Enter Password: ")


base_url = "https://100.70.0.20/restapi/v10.2/Device/VirtualSystems"

target_templates = []
counter=0

while counter<2:
    user_input = input("Enter a template (or 'quit' to stop): ")
    
    if user_input.lower() == "quit":
        break
    
    target_templates.append(user_input)
    
    counter = counter+1
    
for x in target_templates:
    url = f"{base_url}?location=template&template="+x+"&name=vsys1"
    
    payload = {
        "entry": {
            "@name": "vsys1",
            "@template": x,
            "import": {
                "network":{
                    "interface":{
                        "member": [
                            "ethernet1/2",
                            "ethernet1/3",

                            ]
                           }
                          }
                         }
                        }
                       }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.put(url, json=payload, headers=headers, auth=(username, password), verify=False)

    print(f"Template: {x}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")