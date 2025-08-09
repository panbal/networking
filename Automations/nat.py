   #######Source NAT TO INTERNET ###########
   
   POLICY_NAME = 'source-nat-to-internet'
   if cloud == 'aws':
    INTERFACE_CS='ethernet1/2'
   else:
    INTERFACE_CS='ethernet1/1'
   SOURCE_ZONE = coid.lower()+'-internal'
   DEST_ZONE = coid.lower()+'-external'
   
   # XML template
   policy_xml_template = """
   <entry name="{policy_name}">
       <from><member>{source_zone}</member></from>
       <to><member>{destination_zone}</member></to>
       <source><member>any</member></source>
       <destination><member>any</member></destination>
       <service><any></service>
       <source-translation>
        <dynamic-ip-and-port>
            <interface-address><interface>{interface_cs}</interface></interface-address>
        </dynamic-ip-and-port>
       </source-translation>
   </entry>
   """
   
   
   # Construct the XML payload
   policy_xml = policy_xml_template.format(
       policy_name=POLICY_NAME,
       source_zone=SOURCE_ZONE,
       destination_zone=DEST_ZONE,
       action=ACTION,
       sec_profile=SEC_PROFILE,
       interface_cs=INTERFACE_CS
   )
   
   # URL for the API request
   url = f'https://{PANORAMA_IP}/api/?type=config&action=set&xpath=/config/devices/entry/device-group/entry[@name="{DEVICE_GROUP}"]/pre-rulebase/nat/rules&key={API_KEY}'
   
   # Headers for the request
   headers = {'Content-Type': 'application/x-www-form-urlencoded'}
   
   # Data for the request
   data = {'element': policy_xml}
   
   # Send the POST request
   response = requests.post(url, headers=headers, data=data, verify=False)
   
   # Print the response
   print(response.status_code)
   print(response.text)