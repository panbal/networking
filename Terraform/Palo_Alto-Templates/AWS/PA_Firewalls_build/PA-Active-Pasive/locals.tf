locals {
  coid                      = var.company_coid
  environment               = var.company_env
  location_short            = var.company_location_short
  aws_region                = var.aws_region
  instance_type             = var.instance_type
  aws_availability_zone     =var.aws_availability_zone

  hub_address_space         = var.hub_address
}