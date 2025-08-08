#----------------------------------------------------------------------------------------------------------------------
# Loadbalancer
#----------------------------------------------------------------------------------------------------------------------

resource "azurerm_public_ip" "ingress_pip" {
  name                = "ingress-lb-pip"
  location            = var.resource_group_networking.location
  resource_group_name = var.resource_group_networking.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_lb" "ingress" {
  location            = var.resource_group_networking.location
  resource_group_name = var.resource_group_networking.name
  name                = "ingress-lb"
  sku                 = "Standard"
  
  frontend_ip_configuration {
    name                 = "PublicIPAddress"
    public_ip_address_id = azurerm_public_ip.ingress_pip.id
  }
}

resource "azurerm_lb_backend_address_pool" "ingress_backend_address_pool" {
  name            = "vmseries_ethernet0_1"
  loadbalancer_id = azurerm_lb.ingress.id
}

resource "azurerm_lb_probe" "ingress_probe" {
  name                = "TCP-443"
  loadbalancer_id     = azurerm_lb.ingress.id
  port                = 443
  protocol            = "Tcp"
  #request_path        = "/php/login.php"
  interval_in_seconds = 5
  #number_of_probes    = 2
}

resource "azurerm_lb_rule" "tcp" {
  count                          = length(var.inbound_tcp_ports)
  name                           = "tcp-${element(var.inbound_tcp_ports, count.index)}"
  loadbalancer_id                = azurerm_lb.ingress.id
  protocol                       = "Tcp"
  frontend_port                  = element(var.inbound_tcp_ports, count.index)
  backend_port                   = element(var.inbound_tcp_ports, count.index)
  frontend_ip_configuration_name = "PublicIPAddress"
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.ingress_backend_address_pool.id]
  probe_id                       = azurerm_lb_probe.ingress_probe.id
  enable_floating_ip             = false
  disable_outbound_snat          = true
  enable_tcp_reset               = false
  load_distribution              = "SourceIPProtocol"
}

resource "azurerm_lb_rule" "udp" {
  count                          = length(var.inbound_udp_ports)
  name                           = "udp-${element(var.inbound_udp_ports, count.index)}"
  loadbalancer_id                = azurerm_lb.ingress.id
  protocol                       = "Udp"
  frontend_port                  = element(var.inbound_udp_ports, count.index)
  backend_port                   = element(var.inbound_udp_ports, count.index)
  frontend_ip_configuration_name = "PublicIPAddress"
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.ingress_backend_address_pool.id]
  probe_id                       = azurerm_lb_probe.ingress_probe.id
  enable_floating_ip             = false
  disable_outbound_snat          = true
  enable_tcp_reset               = false
  load_distribution              = "SourceIPProtocol"
}

resource "azurerm_network_interface_backend_address_pool_association" "ethernet00_0_1" {
  network_interface_id    = azurerm_network_interface.ethernet00_0_1.id
  ip_configuration_name   = "ipconfig1"
  backend_address_pool_id = azurerm_lb_backend_address_pool.ingress_backend_address_pool.id
}

resource "azurerm_network_interface_backend_address_pool_association" "ethernet01_0_1" {
  network_interface_id    = azurerm_network_interface.ethernet01_0_1.id
  ip_configuration_name   = "ipconfig1"
  backend_address_pool_id = azurerm_lb_backend_address_pool.ingress_backend_address_pool.id
}


resource "azurerm_lb" "egress" {
  location            = var.resource_group_networking.location
  resource_group_name = var.resource_group_networking.name
  name                = "egress-lb"
  sku                 = "Standard"

  frontend_ip_configuration {
    name      = "LoadBalancerIP"
    subnet_id = azurerm_subnet.loadbalancer00.id
  }
}

resource "azurerm_lb_probe" "egress_probe" {
  name                = "TCP-443"
  loadbalancer_id     = azurerm_lb.egress.id
  port                = 443
  protocol            = "Tcp"
  interval_in_seconds = 5
}

resource "azurerm_lb_backend_address_pool" "egress_backend_address_pool" {
  name            = "ethernet0_2"
  loadbalancer_id = azurerm_lb.egress.id
}

resource "azurerm_lb_rule" "allports" {
  name                           = "all-ports"
  loadbalancer_id                = azurerm_lb.egress.id
  protocol                       = "All"
  frontend_port                  = 0
  backend_port                   = 0
  frontend_ip_configuration_name = "LoadBalancerIP"
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.egress_backend_address_pool.id]
  probe_id                       = azurerm_lb_probe.egress_probe.id
  enable_floating_ip             = false
}

resource "azurerm_network_interface_backend_address_pool_association" "ethernet00_0_2" {
  network_interface_id    = azurerm_network_interface.ethernet00_0_2.id
  ip_configuration_name   = "ipconfig1"
  backend_address_pool_id = azurerm_lb_backend_address_pool.egress_backend_address_pool.id
}

resource "azurerm_network_interface_backend_address_pool_association" "ethernet01_0_2" {
  network_interface_id    = azurerm_network_interface.ethernet01_0_2.id
  ip_configuration_name   = "ipconfig1"
  backend_address_pool_id = azurerm_lb_backend_address_pool.egress_backend_address_pool.id
}