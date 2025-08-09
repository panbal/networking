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
                                                                                                                         
     Address and Groups Objects                                                                                                                    

""")

#Variables
username = input ("Enter Username: ")
password = input ("Enter Password: ")
prvsubnet = input ("Enter Private Subnet with mask /x: ")
pubsubnet = input ("Enter Public Subnet with mask /x: ")
coid = input ("Enter COID: ")
coid = coid.upper()
dg_parent=coid

counter1=0
pubintip=[]
while counter1<2:
    user_input_1 = input("Enter the IP of the Public Interface (or 'quit' to stop): ")
    
    if user_input_1.lower() == "quit":
        break
    
    pubintip.append(user_input_1)
    
    counter1 = counter1+1
    
spoke=[]
    
while True:
    user_input_1 = input("Enter Spoke Subnet (or 'quit' to stop): ")
    
    if user_input_1.lower() == "quit":
        break
    
    spoke.append(user_input_1)
    



#### CREATE COID INTERFACE NETWORKS ###

        #### Create The Address Objects ####

prvpure = prvsubnet.rpartition('/')[0]
prvmask = prvsubnet.rpartition('/')[2]
pubpure = pubsubnet.rpartition('/')[0]
pubmask = pubsubnet.rpartition('/')[2]
prvname = "n."+prvpure+"_"+prvmask
pubname = "n."+pubpure+"_"+pubmask

print ( prvname)
    

base_url = "https://100.70.0.20/restapi/v10.2/Objects/Addresses"
    
url = f"{base_url}?location=device-group&device-group="+dg_parent+"&name="+prvname

payload = {
    "entry": {
        "@name": prvname,
        "@template": dg_parent,
        "ip-netmask" : prvsubnet
        }
       }
       
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

print(f"Template: {dg_parent}")
print(f"Response Code: {response.status_code}")
print(f"Response Content: {response.content.decode('utf-8')}")
    
url = f"{base_url}?location=device-group&device-group="+dg_parent+"&name="+pubname

payload = {
    "entry": {
        "@name": pubname,
        "@template": dg_parent,
        "ip-netmask" : pubsubnet
        }
       }
       
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

print(f"Template: {dg_parent}")
print(f"Response Code: {response.status_code}")
print(f"Response Content: {response.content.decode('utf-8')}")


            ### Create the COID INTERFACE NETWORK Group ####


base_url = "https://100.70.0.20/restapi/v10.2/Objects/AddressGroups"

url = f"{base_url}?location=device-group&device-group="+dg_parent+"&name="+coid+"_INTERFACE_NETWORKS"

payload = {
    "entry": {
        "@name": coid+"_INTERFACE_NETWORKS",
        "@template": dg_parent,
        "static" : {
            "member" : [
                prvname,
                pubname
                ]
               }
        }
       }
       
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

print(f"Template: {dg_parent}")
print(f"Response Code: {response.status_code}")
print(f"Response Content: {response.content.decode('utf-8')}")

base_url = "https://100.70.0.20/restapi/v10.2/Objects/Addresses"
public_interfaces=[]
for x in pubintip:
    xpure = x.rpartition('/')[0]
    xmask = x.rpartition('/')[2]
    xname = "s."+xpure+"_"+xmask
    url = f"{base_url}?location=device-group&device-group="+dg_parent+"&name="+xname
    
    payload = {
        "entry": {
            "@name": xname,
            "@template": dg_parent,
            "ip-netmask" : x
            }
        }
        
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)
    public_interfaces.append(xname)
    print(f"Template: {x}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")       
    
base_url = "https://100.70.0.20/restapi/v10.2/Objects/AddressGroups"

url = f"{base_url}?location=device-group&device-group="+dg_parent+"&name="+coid+"_PUBLIC_INTERFACES"

payload = {
    "entry": {
        "@name": coid+"_PUBLIC_INTERFACES",
        "@template": dg_parent,
        "static" : {
            "member" : [
                public_interfaces[0],
                public_interfaces[1]
                ]
               }
        }
       }
       
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

print(f"Template: {dg_parent}")
print(f"Response Code: {response.status_code}")
print(f"Response Content: {response.content.decode('utf-8')}")

base_url = "https://100.70.0.20/restapi/v10.2/Objects/Addresses"
spoke_networks=[]
for x in spoke:
    xpure = x.rpartition('/')[0]
    xmask = x.rpartition('/')[2]
    xname = "s."+xpure+"_"+xmask
    url = f"{base_url}?location=device-group&device-group="+dg_parent+"&name="+xname
    
    payload = {
        "entry": {
            "@name": xname,
            "@template": dg_parent,
            "ip-netmask" : x
            }
        }
        
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)
    spoke_networks.append(xname)
    print(f"Template: {x}")
    print(f"Response Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")
    
base_url = "https://100.70.0.20/restapi/v10.2/Objects/AddressGroups"   
url = f"{base_url}?location=device-group&device-group="+dg_parent+"&name="+coid+"_CLOUD_NETWORKS"

payload = {
    "entry": {
        "@name": coid+"_CLOUD_NETWORKS",
        "@template": dg_parent,
        "static": {
            "member": []
        }
    }
}

for interface in spoke_networks:
    payload["entry"]["static"]["member"].append(interface)

headers = {
    "Content-Type": "application/json"
}
response = requests.post(url, json=payload, headers=headers, auth=(username, password), verify=False)

print(f"Template: {dg_parent}")
print(f"Response Code: {response.status_code}")
print(f"Response Content: {response.content.decode('utf-8')}")
        