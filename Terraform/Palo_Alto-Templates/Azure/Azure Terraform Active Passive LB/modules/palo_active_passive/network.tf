#----------------------------------------------------------------------------------------------------------------------
# Network
#----------------------------------------------------------------------------------------------------------------------

resource "azurerm_virtual_network" "vnet00" {
  name                = "${var.coid}-${var.location}-hubnetwork-vnet-00"
  location            = var.resource_group_networking.location
  resource_group_name = var.resource_group_networking.name
  address_space       = var.hub_address_space
}

# Create Subnets

resource "azurerm_subnet" "shared00" {
  name                 = "${var.coid}-${var.location}-shared-subnet-00"
  virtual_network_name = azurerm_virtual_network.vnet00.name
  resource_group_name  = var.resource_group_networking.name
  address_prefixes     = var.shared_space_prefix
}
resource "azurerm_subnet" "management00" {
  name                 = "${var.coid}-${var.location}-mgmt-subnet-00"
  virtual_network_name = azurerm_virtual_network.vnet00.name
  resource_group_name  = var.resource_group_networking.name
  address_prefixes     = var.mgmt_space_prefix
}

resource "azurerm_subnet" "ha200" {
  name                 = "${var.coid}-${var.location}-ha2-subnet-00"
  virtual_network_name = azurerm_virtual_network.vnet00.name
  resource_group_name  = var.resource_group_networking.name
  address_prefixes     = var.ha2_space_prefix
}

resource "azurerm_subnet" "private00" {
  name                 = "${var.coid}-${var.location}-private-subnet-00"
  virtual_network_name = azurerm_virtual_network.vnet00.name
  resource_group_name  = var.resource_group_networking.name
  address_prefixes     = var.private_space_prefix
}

resource "azurerm_subnet" "public00" {
  name                 = "${var.coid}-${var.location}-public-subnet-00"
  virtual_network_name = azurerm_virtual_network.vnet00.name
  resource_group_name  = var.resource_group_networking.name
  address_prefixes     = var.public_space_prefix
}

resource "azurerm_subnet" "loadbalancer00" {
  name                 = "${var.coid}-${var.location}-loadbalancer-subnet-00"
  virtual_network_name = azurerm_virtual_network.vnet00.name
  resource_group_name  = var.resource_group_networking.name
  address_prefixes     = var.lb_space_prefix
}

#----------------------------------------------------------------------------------------------------------------------
# Network - Azure Virtual WAN
#----------------------------------------------------------------------------------------------------------------------

# Creation of vWAN managed service
resource "azurerm_virtual_wan" "vwan" {
  name                           = "${var.coid}-${var.location}-hubnetwork-vwan-00"
  resource_group_name            = var.resource_group_networking.name
  location                       = var.resource_group_networking.location
  type                           = "Standard"
  allow_branch_to_branch_traffic = true
}

# Creation of vHUB in default location - For DR we need to add second HUB
resource "azurerm_virtual_hub" "hub" {
  name                = "${var.coid}-${var.location}-hubnetwork-hub-00"
  resource_group_name = var.resource_group_networking.name
  location            = var.resource_group_networking.location
  virtual_wan_id      = azurerm_virtual_wan.vwan.id
  address_prefix      = var.virtual_wan_address_space[0]
  hub_routing_preference = "ASPath"
}

resource "azurerm_vpn_gateway" "hub_gateway" {
  name                = "${var.coid}-${var.location}-hubnetwork-gateway-00"
  location            = var.resource_group_networking.location
  resource_group_name = var.resource_group_networking.name
  virtual_hub_id      = azurerm_virtual_hub.hub.id
}

# That creates a VPN site, including the VPN gateway. We can output the PSK/Peer IP in the future. 
resource "azurerm_vpn_site" "vwan_vpn" {
  name                = "on-premise_company"
  resource_group_name = var.resource_group_networking.name
  location            = var.resource_group_networking.location
  virtual_wan_id      = azurerm_virtual_wan.vwan.id

  # Networks on the peer side

  address_cidrs = ["10.159.94.0/23","100.70.0.0/15"]

  # This link is for on-premise
  link {
    name          = "link1"
    ip_address    = "PUBLIC IP"
    provider_name = "Verizon"
    speed_in_mbps = "100"
  }
}

# This is the vWAN peer to Firewall vnet - Required for traffic fitlering from External Connections. That ONLy works when we are within same Tenant.
resource "azurerm_virtual_hub_connection" "connection_hub" {
  name                      = "${var.coid}-${var.location}-hubnetwork-peer-00"
  virtual_hub_id            = azurerm_virtual_hub.hub.id
  remote_virtual_network_id = azurerm_virtual_network.vnet00.id
}

resource "azurerm_vpn_gateway_connection" "on-premise-link" {
  name               = "on-premise-S2S"
  vpn_gateway_id     = azurerm_vpn_gateway.hub_gateway.id
  remote_vpn_site_id = azurerm_vpn_site.vwan_vpn.id
 
  vpn_link {
    name             = "on-premise-S2S"
    vpn_site_link_id = azurerm_vpn_site.vwan_vpn.link[0].id
	  shared_key		 = var.psk
  }
}

#----------------------------------------------------------------------------------------------------------------------
# Routing - Shared Subnet
#----------------------------------------------------------------------------------------------------------------------

resource "azurerm_route_table" "sharedrt" {
  name                            = "${var.coid}-${var.location}-shared-rt-00"
  location                        = var.resource_group_networking.location
  resource_group_name             = var.resource_group_networking.name
  route {
    name                          = "Default"
    address_prefix                = "0.0.0.0/0"
    next_hop_type                 = "VirtualAppliance"
    next_hop_in_ip_address        =  azurerm_lb.egress.frontend_ip_configuration[0].private_ip_address
  }

  tags = {
    environment = "Production"
  }
}

resource "azurerm_subnet_route_table_association" "sharedrtassociate" {
  subnet_id                       = azurerm_subnet.shared00.id
  route_table_id                  = azurerm_route_table.sharedrt.id
}

#----------------------------------------------------------------------------------------------------------------------
# NAT Gateway
#----------------------------------------------------------------------------------------------------------------------

# NAT GW Public IP

resource "azurerm_public_ip" "ext_natgw_pip" {
  name                = "${var.coid}-${var.location}-natpip-00"
  location            = var.resource_group_networking.location
  resource_group_name = var.resource_group_networking.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# Build NAT Gateway

resource "azurerm_nat_gateway" "ext_natgw" {
  name                    = "${var.coid}-${var.location}-natgw-00"
  location                = var.resource_group_networking.location
  resource_group_name     = var.resource_group_networking.name
  sku_name                = "Standard"
  idle_timeout_in_minutes = 10
}

# Associate Public IP

resource "azurerm_nat_gateway_public_ip_association" "ext_natgwpip_associate" {
  nat_gateway_id       = azurerm_nat_gateway.ext_natgw.id
  public_ip_address_id = azurerm_public_ip.ext_natgw_pip.id
}

# Associate puplic subnets

resource "azurerm_subnet_nat_gateway_association" "ext_natgw_subnet" {
  subnet_id      = azurerm_subnet.public00.id
  nat_gateway_id = azurerm_nat_gateway.ext_natgw.id
}