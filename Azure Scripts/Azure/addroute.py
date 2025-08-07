print ("This will create Azure CLI scripts to add routes on a routing table")
print ("Powered by me")
rtname = input("Please choose your RT name: ")
rgname = input ("Your RT is located on which Resource Group: ")
#routetype = input("Write VirtualAppliance or VnetLocal")
#inputtype = input("If you want to manually input routes write manual else write auto: ")
nxhop = input("Write your next hop on x.x.x.x/mask format")
output=open("output.txt","w")

with open('test.txt') as f:
    lines = f.read().splitlines()
    a = (len(lines))
    rulename=input("Put rule name: ")
    count=0
    for i in range(a):
        
        count=count+1
        count2=str(count)
        output.write('az network route-table route create -g '+rgname+' --route-table-name '+rtname+' -n '+rulename+count2+' --next-hop-type VirtualAppliance --address-prefix '+lines[i]+' --next-hop-ip-address '+nxhop+'\n')
