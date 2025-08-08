#----------------------------------------------------------------------------------------------------------------------
# VM-Series - MGMT
#----------------------------------------------------------------------------------------------------------------------

# Public IP Address:
resource "azurerm_public_ip" "management00" {
  name                = "nic-management00-pip"
  location            = var.resource_group_compute.location
  resource_group_name = var.resource_group_compute.name
  allocation_method   = "Static"
  sku                 = "Standard"
}


# Network Interface:
resource "azurerm_network_interface" "management00" {
  name                 = "nic-management00"
  location             = var.resource_group_compute.location
  resource_group_name  = var.resource_group_compute.name
  enable_ip_forwarding = false

  ip_configuration {
    name                          = "ipconfig00"
    subnet_id                     = azurerm_subnet.management00.id
    private_ip_address_allocation = "Static"
    private_ip_address            = cidrhost(var.hub_address_space[0], 4)
    public_ip_address_id          = azurerm_public_ip.management00.id
  }
}


# Network Security Group:
resource "azurerm_network_security_group" "management00" {
  name                = "nsg-management00"
  location            = var.resource_group_compute.location
  resource_group_name = var.resource_group_compute.name

  security_rule {
    name                       = "Deny_ALL"
    priority                   = 1000
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "0.0.0.0/0"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "default-access-inbound"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefixes    = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "52.147.201.44/32", "207.223.34.132"]
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "Allow-To-DNS"
    priority                   = 100
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "53"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }


  security_rule {
    name                       = "Allow-To-Mail"
    priority                   = 200
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "25"
    source_address_prefix      = "*"
    destination_address_prefix = "10.159.94.203/32"
  }

  security_rule {
    name                       = "Allow-To-LDAP"
    priority                   = 250
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "389"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "Allow-To-Panorama"
    priority                   = 300
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "100.70.0.20/32"
  }

    security_rule {
    name                       = "Allow-To-TACACS"
    priority                   = 350
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefixes = ["100.70.1.6", "100.71.78.4"]
  }

  security_rule {
    name                       = "Allow-To-Syslog"
    priority                   = 400
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "13004"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "Block-Private-Ranges"
    priority                   = 1000
    direction                  = "Outbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefixes = ["10.0.0.0/8","192.168.0.0/16","172.16.0.0/12"]
  }
}

resource "azurerm_network_interface_security_group_association" "management00" {
  network_interface_id      = azurerm_network_interface.management00.id
  network_security_group_id = azurerm_network_security_group.management00.id
}


#----------------------------------------------------------------------------------------------------------------------
# VM-Series - Ethernet0/1 Interface (Untrust)
#----------------------------------------------------------------------------------------------------------------------

# Public IP Address
resource "azurerm_public_ip" "ethernet00_0_1" {
  name                = "nic-ethernet00_0_1-pip"
  location            = var.resource_group_compute.location
  resource_group_name = var.resource_group_compute.name
  allocation_method   = "Static"
  sku                 = "Standard"
}


# Network Interface
resource "azurerm_network_interface" "ethernet00_0_1" {
  name                          = "nic-ethernet00_0_1"
  location                      = var.resource_group_compute.location
  resource_group_name           = var.resource_group_compute.name
  enable_ip_forwarding          = true
  enable_accelerated_networking = true

  ip_configuration {
    name                          = "ipconfig1"
    subnet_id                     = azurerm_subnet.public00.id
    private_ip_address_allocation = "Static"
    private_ip_address            = cidrhost(var.hub_address_space[0], 52)
    public_ip_address_id          = azurerm_public_ip.ethernet00_0_1.id
  }
}


resource "azurerm_network_security_group" "data" {
  name                = "data-nsg-allow-all"
  location            = var.resource_group_compute.location
  resource_group_name = var.resource_group_compute.name

  security_rule {
    name                       = "data-inbound"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "data-outbound"
    priority                   = 1000
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_network_interface_security_group_association" "ethernet00_0_1" {
  network_interface_id      = azurerm_network_interface.ethernet00_0_1.id
  network_security_group_id = azurerm_network_security_group.data.id
}


#----------------------------------------------------------------------------------------------------------------------
# VM-Series - Ethernet0/2 Interface (Trust)
#----------------------------------------------------------------------------------------------------------------------

# Network Interface
resource "azurerm_network_interface" "ethernet00_0_2" {
  name                          = "nic-ethernet00_0_2"
  location                      = var.resource_group_compute.location
  resource_group_name           = var.resource_group_compute.name
  enable_ip_forwarding          = true
  enable_accelerated_networking = true


  ip_configuration {
    name                          = "ipconfig1"
    subnet_id                     = azurerm_subnet.private00.id
    private_ip_address_allocation = "Static"
    private_ip_address            = cidrhost(var.hub_address_space[0], 36)
  }
}

resource "azurerm_network_interface_security_group_association" "ethernet00_0_2" {
  network_interface_id      = azurerm_network_interface.ethernet00_0_2.id
  network_security_group_id = azurerm_network_security_group.data.id
}

#----------------------------------------------------------------------------------------------------------------------
# VM-Series - Ethernet0/3 Interface (HA)
#----------------------------------------------------------------------------------------------------------------------

# Network Interface
resource "azurerm_network_interface" "ethernet00_0_3" {
  name                          = "nic-ethernet00_0_3"
  location                      = var.resource_group_compute.location
  resource_group_name           = var.resource_group_compute.name
  enable_ip_forwarding          = true
  enable_accelerated_networking = true

  ip_configuration {
    name                          = "ipconfig1"
    subnet_id                     = azurerm_subnet.ha200.id
    private_ip_address_allocation = "Static"
    private_ip_address            = cidrhost(var.hub_address_space[0], 20)
  }
}


#----------------------------------------------------------------------------------------------------------------------
# VM-Series - Virtual Machine
#----------------------------------------------------------------------------------------------------------------------

resource "azurerm_marketplace_agreement" "palo" {
  publisher = "paloaltonetworks"
  offer     = "vmseries-flex"
  plan      = "byol"
}

resource "azurerm_linux_virtual_machine" "vmseries00" {
  # Resource Group & Location:
  location            = var.resource_group_compute.location
  resource_group_name = var.resource_group_compute.name

  name = "${var.coid}az${var.location_short}pa00"

  

  # Instance
  size = "Standard_DS3_v2"

  # Username and Password Authentication:
  disable_password_authentication = false
  admin_username                  = var.admin_username
  admin_password                  = var.admin_password

  # Network Interfaces:
  network_interface_ids = [
    azurerm_network_interface.management00.id,
    azurerm_network_interface.ethernet00_0_1.id,
    azurerm_network_interface.ethernet00_0_2.id,
    azurerm_network_interface.ethernet00_0_3.id,
  ]

  plan {
    name      = "byol"
    publisher = "paloaltonetworks"
    product   = "vmseries-flex"
  }

  source_image_reference {
    publisher = "paloaltonetworks"
    offer     = "vmseries-flex"
    sku       = "byol"
    version   = "latest"
    #command = "az vm image terms accept --publisher paloaltonetworks --offer vmseries-flex --plan byol"
  }

  os_disk {
    name                 = "${var.coid}az${var.location_short}pa00-osdisk"
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  tags = {
    company_type = "Network Device"
    company_coid = var.coid
    company_apid = "NTWK"
    company_env  = var.environment
    company_desc = "Palo Alto Firewall"
    company_status = "newbuild"
  }
}
