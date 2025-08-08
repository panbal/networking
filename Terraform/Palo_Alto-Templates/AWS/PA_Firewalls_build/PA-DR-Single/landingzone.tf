#----------------------------------------------------------------------------------------------------------------------
# Network - HUB
#----------------------------------------------------------------------------------------------------------------------

module "palo-dr" {
  source = "./modules/palo-dr"

  coid           = local.coid
  environment    = local.environment
  location_short = local.location_short
  instance_type  = local.instance_type

  #Subnet creation form VPC CIDR - Option 5 means /28 subnets

  hub_address_space         = local.hub_address_space
  mgmt_space_prefix         = [cidrsubnet(local.hub_address_space[0], 5, 0)]
  public_space_prefix       = [cidrsubnet(local.hub_address_space[0], 5, 8)]
  private_space_prefix      = [cidrsubnet(local.hub_address_space[0], 5, 1)]
  ha2_space_prefix          = [cidrsubnet(local.hub_address_space[0], 5, 2)]
  tgw_space_prefix          = [cidrsubnet(local.hub_address_space[0], 5, 3)]
  aws_region                = local.aws_region
  aws_availability_zone     = local.aws_availability_zone

}