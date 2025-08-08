locals {
  coid           = var.company_coid
  environment    = var.company_env
  location       = var.company_location
  location_short = var.company_location_short
  function       = "hub"
  shared_space_prefix = var.shared_space_prefix

  size = var.size
  zone1 = var.zone1
  zone2 = var.zone2
  psk = var.psk
  version=var.version

  hub_address_space         = var.hub_address
  virtual_wan_address_space = var.vwan_address
}