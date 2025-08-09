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
                                                                                                                         
     AntiSpyware Profile                                                                                                                   

""")

#Variables

username = input ("Enter Username: ")
password = input ("Enter Password: ")
coid = input ("Enter COID: ")

#Take as input the template(s)
    
    #Make values to 0
target_templates = []
counter=0

    #Up to 2 templates - Take List target_template
while counter<2:
    user_input = input("Enter a template (or 'quit' to stop): ")
    
    if user_input.lower() == "quit":
        break
    
    target_templates.append(user_input)
    
    counter = counter+1
    
#Manipulate Data

coid=coid.upper()
name=coid+"ASP"

########### Antispyware Profile ###########

base_url = "https://100.70.0.20/restapi/v10.2/Objects/AntiSpywareSecurityProfiles"

for asp in target_templates:
   url = f"{base_url}?location=device-group&device-group="+asp+"&name="+coid+"-ASP"
    
   payload = {
       "entry": {
           "@name": coid+"-ASP",
           "@template": asp,
           "rules": {
                "entry": [
                    {
                        "@name":"simple-critical",
                        "threat-name":"any",
                        "category":"any",
                        "severity": {
                            "member": [
                                "critical"
                                ]
                               },
                        "action": {
                            "drop" :{}
                            },
                        "packet-capture": "extended-capture"
                        },
                        
                     {
                        "@name":"simple-high",
                        "threat-name":"any",
                        "category":"any",
                        "severity": {
                            "member": [
                                "high"
                                ]
                               },
                        "action": {
                            "drop" :{}
                            },
                        "packet-capture": "extended-capture"
                        },                     
                     {
                        "@name":"simple-medium",
                        "threat-name":"any",
                        "category":"any",
                        "severity": {
                            "member": [
                                "medium"
                                ]
                               },
                        "action": {
                            "default" :{}
                            },
                        "packet-capture": "single-packet"
                        },
                     {
                        "@name":"simple-low",
                        "threat-name":"any",
                        "category":"any",
                        "severity": {
                            "member": [
                                "low"
                                ]
                               },
                        "action": {
                            "alert" :{}
                            },
                        "packet-capture": "disable"
                        }                       
                       ]
                      },
                        
            "cloud-inline-analysis":"no",
            "botnet-domains": {
                "whitelist": {
                    "entry": [
                        {
                            "@name":"company.com"
                        },
                        {
                            "@name":"tanium.com"
                        }
                        ]
                       }
                      }
       }
   }

   headers = {
       "Content-Type": "application/json"
   }

   response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

   print(f"Template: {asp}")
   print(f"Response Code: {response.status_code}")
   print(f"Response Content: {response.content.decode('utf-8')}")