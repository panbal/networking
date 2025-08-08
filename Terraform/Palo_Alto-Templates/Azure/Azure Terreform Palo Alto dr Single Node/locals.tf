locals {
  coid           = var.company_coid
  environment    = var.company_env
  location       = var.company_location
  location_short = var.company_location_short
  function       = "hub"

  hub_address_space         = var.hub_address
  virtual_wan_address_space = var.vwan_address
  local_prd_vwan            = var.prd_vwan_name_id
  local_prd_vwa_rg          = var.prd_vwan_rg
}