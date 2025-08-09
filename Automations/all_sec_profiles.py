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
                                                                                                                         
     Security Profile Creation                                                                                                                  

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
   

########### WildFire Profile Creation ###########

base_url = "https://100.70.0.20/restapi/v10.2/Objects/WildFireAnalysisSecurityProfiles"

for wlf in target_templates:
   url = f"{base_url}?location=device-group&device-group="+wlf+"&name="+coid+"_WILDFIRE"
    
   payload = {
       "entry": {
           "@name": coid+"_WILDFIRE",
           "@template": wlf,
           "rules":{
            "entry": [
                {
                    "@name": "default",
                    "application": {
                        "member": [
                            "any"
                            ]
                           },
                    "file-type": {
                        "member": [
                            "any"
                            ]
                           },
                    "direction" : "both",
                    "analysis" : "public-cloud"
                    }
                   ]
                  }
                 }
                }
                    

          
   headers = {
      "Content-Type": "application/json"
   }

   response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

   print(f"Template: {wlf}")
   print(f"Response Code: {response.status_code}")
   print(f"Response Content: {response.content.decode('utf-8')}")
   
########### Security Profile Groups ###########


            #### INTERNAL SPG####
            
base_url = "https://100.70.0.20/restapi/v10.2/Objects/SecurityProfileGroups"

for sgroup1 in target_templates:
   url = f"{base_url}?location=device-group&device-group="+sgroup1+"&name="+coid+"_INTERNAL_SPG"
    
   payload = {
       "entry": {
           "@name": coid+"_INTERNAL_SPG",
           "@template": sgroup1,
           "spyware": {
            "member": [
                coid+"-ASP"
                ]
               },
           "vulnerability": {
            "member": [
                coid+"-VP"
                ]
               }
              }
             }
             
   headers = {
       "Content-Type": "application/json"
   }

   response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

   print(f"Template: {sgroup1}")
   print(f"Response Code: {response.status_code}")
   print(f"Response Content: {response.content.decode('utf-8')}")
            
            ### External IN SPG ###
            
for sgroup2 in target_templates:
   url = f"{base_url}?location=device-group&device-group="+sgroup2+"&name="+coid+"_EXTERNAL_IN_SPG"
    
   payload = {
       "entry": {
           "@name": coid+"_EXTERNAL_IN_SPG",
           "@template": sgroup2,
           "spyware": {
            "member": [
                coid+"-ASP"
                ]
               },
           "wildfire-analysis": {
            "member": [
                coid+"_WILDFIRE"
                ]
               },
           "vulnerability": {
            "member": [
                coid+"-VP"
                ]
               }
              }
             }
             
   headers = {
       "Content-Type": "application/json"
   }

   response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

   print(f"Template: {sgroup2}")
   print(f"Response Code: {response.status_code}")
   print(f"Response Content: {response.content.decode('utf-8')}")
            
            ### External OUT SPG ###
            
for sgroup3 in target_templates:
   url = f"{base_url}?location=device-group&device-group="+sgroup3+"&name="+coid+"_EXTERNAL_OUT_SPG"
    
   payload = {
       "entry": {
           "@name": coid+"_EXTERNAL_OUT_SPG",
           "@template": sgroup3,
           "spyware": {
            "member": [
                coid+"-ASP"
                ]
               },
           "wildfire-analysis": {
            "member": [
                coid+"_WILDFIRE"
                ]
               },
           "url-filtering": {
            "member": [
                coid+"_DEF_CONTENT_CATEGORY"
                ]
               },
           "vulnerability": {
            "member": [
                coid+"-VP"
                ]
               }
              }
             }
             
   headers = {
       "Content-Type": "application/json"
   }

   response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

   print(f"Template: {sgroup3}")
   print(f"Response Code: {response.status_code}")
   print(f"Response Content: {response.content.decode('utf-8')}")