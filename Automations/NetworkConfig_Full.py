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
                                                                                                                         
     Network Setup - Full                                                                                                                   

""")

#Variables

username = input ("Enter Username: ")
password = input ("Enter Password: ")
coid = input ("Enter COID: ")
gwprivate = input ("Enter Private Gateway: ")
gwpublic = input ("Enter Public Gateway: ")

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

coid=coid.lower()
    
########### Interface Creation ###########

base_url = "https://100.70.0.20/restapi/v10.2/Network/EthernetInterfaces"

    ########## HA Interface - AWS ############
 
 
for int1 in target_templates:
   url = f"{base_url}?location=template&template="+int1+"&name=ethernet1/1"
    
   payload = {
       "entry": {
           "@name": "ethernet1/1",
           "@template": int1,
           "@vsys": "vsys1",
           "ha": {

           }
       }
   }

   headers = {
       "Content-Type": "application/json"
   }

   response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

   print(f"Template: {int1}")
   print(f"Response Code: {response.status_code}")
   print(f"Response Content: {response.content.decode('utf-8')}")


    ########## Public Interface - AWS ############
    
for int2 in target_templates:
    url = f"{base_url}?location=template&template="+int2+"&name=ethernet1/2"
    
    payload = {
        "entry": {
            "@name": "ethernet1/2",
            "@template": int2,
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

    print(f"Template: {int2}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")
    
    ########## Private Interface - AWS ############
    
for int3 in target_templates:
   url = f"{base_url}?location=template&template="+int3+"&name=ethernet1/3"
    
   payload = {
       "entry": {
           "@name": "ethernet1/3",
           "@template": int3,
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

   print(f"Template: {int3}")
   print(f"Response Code: {response.status_code}")
   print(f"Response Content: {response.content.decode('utf-8')}")
    
####### Importing Interfaces in the vsys1 #############


base_url = "https://100.70.0.20/restapi/v10.2/Device/VirtualSystems"

#We use PUT as vsys1 already exists

for vsys in target_templates:
    url = f"{base_url}?location=template&template="+vsys+"&name=vsys1"
    
    payload = {
        "entry": {
            "@name": "vsys1",
            "@template": vsys,
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

    print(f"Template: {vsys}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")
    
    
 ######## Security Zone Creation ###########
 
        #### Create Zones and assign the proper Interfaces #####
        
        
for zone1 in target_templates:

    payload1 = json.dumps({
     "entry": {
       "@name": coid+"-internal",
       "@location": "template",
       "@template": zone1,
       "@vsys": "vsys1",
       "network": {
         "layer3": {
           "member":["ethernet1/3"]
         },
         "log-setting": "none"
       }
     }
   })

    url = ("https://100.70.0.20/restapi/v10.2/Network/Zones?location=template&template="+zone1+"&vsys=vsys1&name="+coid+"-internal")
    headers = {
      'Content-Type': 'application/json',
      'X-PAN-KEY': 'LUFRPT1icU8wL3RsU0JUZERqS2JpMnBGQ1JxbWdVMmc9a2I5NmQ5ay9tVCs4QVFQcW1ZNGV2REErN3dzVW9yVE1CQUdYbXRKdXM1NnNzdXIraDFQY2R1UWxnSDZkQnZWdg=='
    }
    
    response1 = requests.request("POST", url, headers=headers, data=payload1, verify=False)
    
    print(zone1,"\n",response1.text,"\n")
    
for zone2 in target_templates:

    payload2 = json.dumps({
      "entry": {
        "@name": coid+"-external",
        "@location": "template",
        "@template": zone2,
        "@vsys": "vsys1",
        "network": {
          "layer3": {
            "member":["ethernet1/2"]
          },
          "log-setting": "none"
        }
      }
    })

    url = ("https://100.70.0.20/restapi/v10.2/Network/Zones?location=template&template="+zone2+"&vsys=vsys1&name="+coid+"-external")
    headers = {
      'Content-Type': 'application/json',
      'X-PAN-KEY': 'LUFRPT1icU8wL3RsU0JUZERqS2JpMnBGQ1JxbWdVMmc9a2I5NmQ5ay9tVCs4QVFQcW1ZNGV2REErN3dzVW9yVE1CQUdYbXRKdXM1NnNzdXIraDFQY2R1UWxnSDZkQnZWdg=='
    }
    

    response2 = requests.request("POST", url, headers=headers, data=payload2, verify=False)

    print(zone2,"\n",response2.text,"\n")
    
    
#### VR Creation - AWS ######

base_url = "https://100.70.0.20/restapi/v10.2/Network/VirtualRouters"

        ### Create the VR and add Interfaces and routes
        
for route in target_templates:
    url = f"{base_url}?location=template&template="+route+"&name=default"

    payload = {
        "entry": {
            "@name": "default",
            "@template": route,
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

    print(f"Template: {route}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")
