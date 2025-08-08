#----------------------------------------------------------------------------------------------------------------------
# on-premise S2S
#----------------------------------------------------------------------------------------------------------------------

resource "aws_customer_gateway" "on-premise" {
  bgp_asn                                       = 65000
  ip_address                                    = var.il_external
  type                                          = "ipsec.1"

  tags = {
    Name                                        = join("", [var.coid, "-", var.aws_region, "-on-premise-CGW"])
  }
  }

# Create on-premise VPN pointing to TGW

resource "aws_vpn_connection" "on-premise" {
  transit_gateway_id                            = aws_ec2_transit_gateway.main_tgw.id
  customer_gateway_id                           = aws_customer_gateway.on-premise.id
  type                                          = "ipsec.1"
  static_routes_only                            = true
  tags = {
    Name                                        = join("", [var.coid, "-", var.aws_region, "-on-premise-ipsec"])
  }
}

#Get the ID of the newly created (auto) VPN TGW attachment

data "aws_ec2_transit_gateway_vpn_attachment" "on_prem_attach" {
  depends_on                                    = [aws_vpn_connection.on-premise, aws_ec2_transit_gateway.main_tgw]
  transit_gateway_id                            = aws_ec2_transit_gateway.main_tgw.id
  vpn_connection_id                             = aws_vpn_connection.on-premise.id
}

#Give name Tag to VPN TGW attachment

resource "aws_ec2_tag" "tag_vpn_attach" {
  resource_id                                   = data.aws_ec2_transit_gateway_vpn_attachment.on_prem_attach.id
  key                                           = "Name"
  value                                         = join("", [var.coid, "-", var.aws_region, "-on-premise_VPN"])
}