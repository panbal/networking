import requests
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Replace these with actual values
coid=input("Put your COID: ")
prjnum=input("Put your PRJ NUM: ")
PANORAMA_IP = '100.70.0.20'
API_KEY = ''
DEVICE_GROUP = 'Auto-Azure'  # Replace with the actual device group name
POLICY_NAME = prjnum+'_'+coid+'_PING_ONLY'
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-internal'
APPLICATIONS = ['icmp', 'traceroute']
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <service><member>any</member></service>
    <from><member>{source_zone}</member></from>
    <to><member>{destination_zone}</member></to>
    <source><member>any</member></source>
    <destination><member>any</member></destination>
    <application>
        {applications}
    </application>
    <action>{action}</action>
    <description>Internal Ping to All</description>
    <tag><member>INTERNAL_POLICY</member></tag>
</entry>
"""

# Construct the applications XML
applications_xml = '\n'.join([f'<member>{app}</member>' for app in APPLICATIONS])

# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    applications=applications_xml,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)

#######INTERNET-TO-APP-BASED###########

POLICY_NAME = prjnum+'_'+coid+'_TO_INTERNET_APP_BASED'
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-external'
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <service><member>any</member></service>
    <from><member>{source_zone}</member></from>
    <to><member>{destination_zone}</member></to>
    <source><member>any</member></source>
    <destination><member>any</member></destination>
    <application><member>comp_INTERNET_SHARED_APP_GROUP</member></application>
    <action>{action}</action>
    <description>Internet APP Based</description>
    <tag><member>EXTERNAL_POLICY</member></tag>
    
</entry>
"""


# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)

#######INTERNET-SERVICE-BASED###########

POLICY_NAME = prjnum+'_'+coid+'_TO_INTERNET_SERVICE_BASED'
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-external'
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <service><member>comp_INTERNET_SHARED_SERVICE_GROUP</member></service>
    <from><member>{source_zone}</member></from>
    <to><member>{destination_zone}</member></to>
    <source><member>any</member></source>
    <destination><member>any</member></destination>
    <application><member>any</member></application>
    <action>{action}</action>
    <description>Internet Service Based</description>
    <tag><member>EXTERNAL_POLICY</member></tag>
    
</entry>
"""


# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)

#######INTERNET-URL-BASED###########

POLICY_NAME = prjnum+'_'+coid+'_TO_INTERNET_URL_BASED'
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-external'
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <from><member>{source_zone}</member></from>
    <to><member>{destination_zone}</member></to>
    <source><member>any</member></source>
    <destination><member>any</member></destination>
    <application><member>any</member></application>
    <service><member>any</member></service>
    <action>{action}</action>
    <category><member>MSP_ALLOW_URL_FILTER_LIST</member></category>
    <description>Internet URL Based</description>
    <tag><member>EXTERNAL_POLICY</member></tag>
    
</entry>
"""


# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)

#######INTERNET-COUNTRY-BASED###########

POLICY_NAME = prjnum+'_'+coid+'_TO_INTERNET_C_BASED'
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-external'
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <from><member>{source_zone}</member></from>
    <to><member>{destination_zone}</member></to>
    <source><member>any</member></source>
    <destination>
        <member>CA</member>
        <member>US</member>
    </destination>
    <application>
        <member>company_DEFAULT_TO_INTERNET</member>
        <member>company_LINUX_PACKAGE_INSTALL</member>       
    </application>
    <service><member>application-default</member></service>
    <action>{action}</action>
    <category><member>any</member></category>
    <description>Internet URL Based</description>
    <tag><member>EXTERNAL_POLICY</member></tag>
    
</entry>
"""


# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)

#######company-TO-COID###########

POLICY_NAME = prjnum+'_'+'company_TO_'+coid
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-internal'
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <from><member>{source_zone}</member></from>
    <to><member>{destination_zone}</member></to>
    <source><member>comp_MANAGEMENT_ADDRESS_GROUP</member></source>
    <destination><member>any</member></destination>
    <application><member>any</member></application>
    <service><member>any</member></service>
    <action>{action}</action>
    <category><member>any</member></category>
    <description>company to customer</description>
    <tag><member>MGMT_POLICY</member></tag>
    
</entry>
"""


# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)

#######COID-TO-company###########

POLICY_NAME = prjnum+'_'+coid+'_TO_company'
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-internal'
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <from><member>{source_zone}</member></from>
    <to><member>{destination_zone}</member></to>
    <source><member>any</member></source>
    <destination><member>comp_MANAGEMENT_ADDRESS_GROUP</member></destination>
    <application><member>any</member></application>
    <service><member>any</member></service>
    <action>{action}</action>
    <category><member>any</member></category>
    <description>company to customer</description>
    <tag><member>MGMT_POLICY</member></tag>
    
</entry>
"""


# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)


#######COID-TO-DEVO###########

POLICY_NAME = prjnum+'_'+coid+'_TO_DEVO'
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-internal'
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <from><member>{source_zone}</member></from>
    <to><member>{destination_zone}</member></to>
    <source><member>any</member></source>
    <destination><member>any</member></destination>
    <application><member>any</member></application>
    <service><member>DEVO_SEIM_SERVICE_GROUP</member></service>
    <action>{action}</action>
    <category><member>any</member></category>
    <description>COID to Devo</description>
    <tag><member>INTERNAL_POLICY</member></tag>
    
</entry>
"""


# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)


#######TO-LB###########

POLICY_NAME = prjnum+'_'+coid+'_LB_HEALTH_CHECK'
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-internal'
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <from><member>any</member></from>
    <to><member>any</member></to>
    <source><member>CLOUD_LB_HEALTH_CHECK_ADDRESS_GROUP</member></source>
    <destination><member>any</member></destination>
    <application>
        <member>ssl</member>
        <member>web-browsing</member>
    </application>
    <service><member>application-default</member></service>
    <action>{action}</action>
    <category><member>any</member></category>
    <description>LB-Health-Check</description>
    <tag><member>MGMT_POLICY</member></tag>
    
</entry>
"""


# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)

#######TO-LM###########

POLICY_NAME = prjnum+'_'+coid+'_TO_LM'
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-internal'
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <from><member>any</member></from>
    <to><member>any</member></to>
    <source><member>any</member></source>
    <destination><member>any</member></destination>
    <application><member>any</member></application>
    <service><member>application-default</member></service>
    <action>{action}</action>
    <category><member>any</member></category>
    <description>LB-Health-Check</description>
    <tag><member>INTERNAL_POLICY</member></tag>
    <disabled>yes</disabled>
    
</entry>
"""


# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)

#######TO-LM###########

POLICY_NAME = prjnum+'_'+coid+'_TO_COMMV'
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-internal'
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <from><member>any</member></from>
    <to><member>any</member></to>
    <source><member>any</member></source>
    <destination><member>any</member></destination>
    <application><member>any</member></application>
    <service><member>tcp-8403</member></service>
    <action>{action}</action>
    <category><member>any</member></category>
    <description>COID_TO_COMMV</description>
    <tag><member>INTERNAL_POLICY</member></tag>
    <disabled>yes</disabled>
    
</entry>
"""


# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)

#######REMOTE-TO-SAP###########

POLICY_NAME = prjnum+'_'+coid+'_REMOTE_TO_SAP'
SOURCE_ZONE = coid+'-internal'
DEST_ZONE = coid+'-internal'
ACTION = 'allow'

# XML template
policy_xml_template = """
<entry name="{policy_name}">
    <log-setting>DEFAULT_LOG_FORWARD</log-setting>
    <from><member>any</member></from>
    <to><member>any</member></to>
    <source><member>any</member></source>
    <destination><member>any</member></destination>
    <application><member>any</member></application>
    <service><member>SAP_ACCESS_PORT_GROUP</member></service>
    <action>{action}</action>
    <category><member>any</member></category>
    <description>REMOTE-TO-SAP</description>
    <tag><member>INTERNAL_POLICY</member></tag>
    <disabled>yes</disabled>
    
</entry>
"""


# Construct the XML payload
policy_xml = policy_xml_template.format(
    policy_name=POLICY_NAME,
    source_zone=SOURCE_ZONE,
    destination_zone=DEST_ZONE,
    action=ACTION
)

# URL for the API request
url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/security/rules&key={API_KEY}'

# Headers for the request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Data for the request
data = {'element': policy_xml}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

# Print the response
print(response.status_code)
print(response.text)