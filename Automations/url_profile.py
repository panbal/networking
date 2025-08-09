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
                                                                                                                         
     URL Profile                                                                                                                   

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

########### URL Custom Profile Creation ###########


base_url = "https://100.70.0.20/restapi/v10.2/Objects/CustomURLCategories"

for curl in target_templates:
   url = f"{base_url}?location=device-group&device-group="+curl+"&name="+coid+"_EXTERNAL_URL_FILTER"
    
   payload = {
       "entry": {
           "@name": coid+"_EXTERNAL_URL_FILTER",
           "@template": curl,
           "list":{
               "member": [
                    "company.com"
                    ]
                   },
           "type":"URL List"
           }
          }
          
   headers = {
      "Content-Type": "application/json"
   }

   response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

   print(f"Template: {curl}")
   print(f"Response Code: {response.status_code}")
   print(f"Response Content: {response.content.decode('utf-8')}")
   
###### URL Security Profile #####

base_url = "https://100.70.0.20/restapi/v10.2/Objects/URLFilteringSecurityProfiles"

for url in target_templates:
   url = f"{base_url}?location=device-group&device-group="+url+"&name="+coid+"_DEF_CONTENT_CATEGORY"
    
   payload = {
       "entry": {
           "@name": coid+"_DEF_CONTENT_CATEGORY",
           "@template": url,
           "local-inline-cat": "yes",
           "cloud-inline-cat": "no",
           "allow": {
            "member": [
                coid+"_EXTERNAL_URL_FILTER"
                ]
               },
           "block": {
            "member": [
                "MSP_BLOCK_URL_FILTER_LIST",
                "abortion",
                "adult",
                "command-and-control",
                "cryptocurrency",
                "extremism",
                "gambling",
                "hacking",
                "high-risk",
                "malware",
                "nudity",
                "phishing",
                "questionable",
                "ransomware",
                "sex-education"
                ]
               },
           "alert": {
            "member": [
                "medium-risk",
                "newly-registered-domain",
                "parked",
                "peer-to-peer",
                "proxy-avoidance-and-anonymizers",
                "real-time-detection",
                "shareware-and-freeware",
                "unknown"
                ]
               },
           "credential-enforcement": {
            "mode": {
                "disabled":{}
                },
            "log-severity": "medium",
            "allow": {
                "member": [
                    coid+"_EXTERNAL_URL_FILTER"
                    ]
                   },
            "block": {
                "member": [
                    "MSP_BLOCK_URL_FILTER_LIST",
                    "abortion",
                    "adult",
                    "command-and-control",
                    "cryptocurrency",
                    "extremism",
                    "gambling",
                    "hacking",
                    "high-risk",
                    "malware",
                    "nudity",
                    "phishing",
                    "questionable",
                    "ransomware",
                    "sex-education"
                    ]
              }
             }
            }
           }
                
                

          
   headers = {
      "Content-Type": "application/json"
   }

   response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

   print(f"Template: {url}")
   print(f"Response Code: {response.status_code}")
   print(f"Response Content: {response.content.decode('utf-8')}")