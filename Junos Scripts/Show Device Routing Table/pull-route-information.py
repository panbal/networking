from jnpr.junos import Device
from lxml import etree
from lxml import etree as ET

open("config-output.txt", "w")

def pullFromJuniper():
    with Device(user='test', host='10.2.1.1', password='test1234', port='22', normalize=True, terse=True) as dev:
        print('get rpc call from CLI command:')
        print (dev.display_xml_rpc('show route', format='text'))
        sw = dev.rpc.get_route_information({'format': 'text'}, table='inet.0')
        with open("config-output.txt", "a") as f:
            print(etree.tostring(sw, encoding='unicode'), file=f)
            print("\n", file=f)
            f.close()
        #print('json output:')
        #json_output = dev.rpc.get_route_information({'format': 'json'})
        #print(json_output)

pullFromJuniper()