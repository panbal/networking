#----------------------------------------------------------------------------------------------------------------------
# VM-Series Palo Deployment
#----------------------------------------------------------------------------------------------------------------------

# Take the id of the AMI
data "aws_ami" "firewall" {
  most_recent                               = true
  owners                                    = ["aws-marketplace"]

  filter {
    name                                    = "name"
    values                                  = ["PA-VM-AWS-10.2.8-h5-7064e142-2859-40a4-ab62-8b0996b842e9*"]
  }
}

resource "aws_instance" "vm1" {
  ami                                       = data.aws_ami.firewall.id
  instance_type                             = var.instance_type
  availability_zone                         = var.aws_availability_zone
  key_name                                  = "firewall"
  private_ip                                = cidrhost(var.hub_address_space[0], 4)
  iam_instance_profile			            = aws_iam_instance_profile.ec2_profile.name
  subnet_id                                 = aws_subnet.MNG.id
  vpc_security_group_ids                    = [aws_security_group.MGMT_sg.id]
  disable_api_termination                   = false
  instance_initiated_shutdown_behavior      = "stop"
  ebs_optimized                             = true
  monitoring                                = false
  tags = {

    Name                                    = join ("", [var.coid, "-AWS", var.location_short, "PA01-A"])
    company_type                            = "network appliance"
    company_coid                            = var.coid
    company_apid                            = "PA"
    company_env                             = var.environment
    company_desc                            = "Palo Alto Virtual Firewall"
  }

  root_block_device {
    delete_on_termination                   = true
  }

}

resource "aws_instance" "vm2" {
  ami                                       = data.aws_ami.firewall.id
  instance_type                             = var.instance_type
  availability_zone                         = var.aws_availability_zone
  key_name                                  = "firewall"
  private_ip                                = cidrhost(var.hub_address_space[0], 5)
  iam_instance_profile			            = aws_iam_instance_profile.ec2_profile.name
  subnet_id                                 = aws_subnet.MNG.id
  vpc_security_group_ids                    = [aws_security_group.MGMT_sg.id]
  disable_api_termination                   = false
  instance_initiated_shutdown_behavior      = "stop"
  ebs_optimized                             = true
  monitoring                                = false
  depends_on                                = [aws_instance.vm1]
  tags = {

    Name                                    = join ("", [var.coid, "-AWS", var.location_short, "PA01-B"])
    company_type                            = "network appliance"
    company_coid                            = var.coid
    company_apid                            = "PA"
    company_env                             = var.environment
    company_desc                            = "Palo Alto Virtual Firewall"
  }

  root_block_device {
    delete_on_termination                   = true
  }
}

resource "aws_network_interface" "ha1" {
  subnet_id                                 = aws_subnet.ha.id
  private_ips                               = [cidrhost(var.hub_address_space[0], 36) ]
  security_groups                           = [aws_security_group.private_sg.id]
  depends_on                                = [aws_instance.vm1,aws_internet_gateway.main_igw,aws_ec2_transit_gateway.main_tgw,aws_eip.mng1]
  attachment {
    instance                                = aws_instance.vm1.id
	device_index                              = 1
  }
}

resource "aws_network_interface" "ha2" {
  subnet_id                                 = aws_subnet.ha.id
  private_ips                               = [cidrhost(var.hub_address_space[0], 37) ]
  security_groups                           = [aws_security_group.private_sg.id]
  depends_on                                = [aws_instance.vm1,aws_internet_gateway.main_igw,aws_ec2_transit_gateway.main_tgw,aws_eip.mng1]
  attachment {
    instance                                = aws_instance.vm2.id
	device_index                              = 1
  }
}


resource "aws_network_interface" "public1" {
  subnet_id                                 = aws_subnet.public.id
  private_ips                               = [cidrhost(var.hub_address_space[0], 132) ]
  security_groups                           = [aws_security_group.public_sg.id]
  depends_on                                = [aws_instance.vm1,aws_internet_gateway.main_igw,aws_ec2_transit_gateway.main_tgw,aws_eip.mng1,aws_network_interface.ha2]	  

  attachment {
    instance                                = aws_instance.vm1.id
    device_index                            = 2
  }
}

resource "aws_network_interface" "private1" {
  subnet_id                                 = aws_subnet.Private.id
  private_ips                               = [cidrhost(var.hub_address_space[0], 20) ]
  security_groups                           = [aws_security_group.private_sg.id]
  depends_on                                = [aws_instance.vm1,aws_internet_gateway.main_igw,aws_ec2_transit_gateway.main_tgw,aws_eip.mng1,aws_network_interface.public1]
  attachment {
    instance                                = aws_instance.vm1.id
	device_index                            = 3
  }
}