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
                                                                                                                         
     Vulnerability Profile                                                                                                                   

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

########### Vulnerability Profile ###########

base_url = "https://100.70.0.20/restapi/v10.2/Objects/VulnerabilityProtectionSecurityProfiles"

for vuln in target_templates:
   url = f"{base_url}?location=device-group&device-group="+vuln+"&name="+coid+"-VP"
    
   payload = {
       "entry": {
           "@name": coid+"-VP",
           "@template": vuln,
           "rules": {
                "entry": [
                    {
                        "@name":"simple-client-critical",
                        "threat-name":"any",
                        "host":"client",
                        "category":"any",
                        "packet-capture": "extended-capture",
                        "severity": {
                            "member": [
                                "critical"
                                ]
                               },
                        "cve": {
                            "member": [
                                "any"
                                ]
                               },
                        "vendor-id": {
                            "member": [
                                "any"
                                ]
                               },                               
                        "action": {
                            "drop" :{}
                            },
                        },
                        
                    {
                        "@name":"simple-client-high",
                        "threat-name":"any",
                        "host":"client",
                        "category":"any",
                        "packet-capture": "extended-capture",
                        "severity": {
                            "member": [
                                "high"
                                ]
                               },
                        "cve": {
                            "member": [
                                "any"
                                ]
                               },
                        "vendor-id": {
                            "member": [
                                "any"
                                ]
                               },                               
                        "action": {
                            "drop" :{}
                            },
                        },
                    {
                        "@name":"simple-client-medium",
                        "threat-name":"any",
                        "host":"client",
                        "category":"any",
                        "packet-capture": "single-packet",
                        "severity": {
                            "member": [
                                "medium"
                                ]
                               },
                        "cve": {
                            "member": [
                                "any"
                                ]
                               },
                        "vendor-id": {
                            "member": [
                                "any"
                                ]
                               },                               
                        "action": {
                            "default" :{}
                            },
                        },
                     {
                        "@name":"simple-server-critical",
                        "threat-name":"any",
                        "host":"server",
                        "category":"any",
                        "packet-capture": "extended-capture",
                        "severity": {
                            "member": [
                                "critical"
                                ]
                               },
                        "cve": {
                            "member": [
                                "any"
                                ]
                               },
                        "vendor-id": {
                            "member": [
                                "any"
                                ]
                               },                               
                        "action": {
                            "drop" :{}
                            },
                        },                       
                     {
                        "@name":"simple-server-high",
                        "threat-name":"any",
                        "host":"server",
                        "category":"any",
                        "packet-capture": "extended-capture",
                        "severity": {
                            "member": [
                                "high"
                                ]
                               },
                        "cve": {
                            "member": [
                                "any"
                                ]
                               },
                        "vendor-id": {
                            "member": [
                                "any"
                                ]
                               },                               
                        "action": {
                            "drop" :{}
                            },
                        },
                     {
                        "@name":"simple-server-medium",
                        "threat-name":"any",
                        "host":"server",
                        "category":"any",
                        "packet-capture": "single-packet",
                        "severity": {
                            "member": [
                                "medium"
                                ]
                               },
                        "cve": {
                            "member": [
                                "any"
                                ]
                               },
                        "vendor-id": {
                            "member": [
                                "any"
                                ]
                               },                               
                        "action": {
                            "default" :{}
                            },
                        }
                       ]
                     }
                    }
                   }
   headers = {
       "Content-Type": "application/json"
   }

   response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

   print(f"Template: {vuln}")
   print(f"Response Code: {response.status_code}")
   print(f"Response Content: {response.content.decode('utf-8')}")