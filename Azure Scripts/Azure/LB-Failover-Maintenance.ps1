#describe the LB
$lb = Get-AzLoadBalancer -Name "lb-test-auto" -ResourceGroupName "lb-change"

#Describe The Rules
$rule1 = Get-AzLoadBalancerRuleConfig -LoadBalancer $lb -Name "to-back-vm-health"
$rule2 = Get-AzLoadBalancerRuleConfig -LoadBalancer $lb -Name "ip-2"

#Describe the Backend Pool - Single Pointing to Firewall
$BkPool = Get-AzLoadBalancerBackendAddressPool -ResourceGroupName "lb-change" -LoadBalancerName "lb-test-auto"  -Name "back-vm-2"

#Describe the Health Check - Single TCP pointing to Firewall
$MyHealthProbe = Get-AzLoadBalancerProbeConfig -LoadBalancer $lb -Name "back-vm-2"

#Get The Correct FrontEnd IP Configuration from the array - Filter based on Name property on a single index array
$frontendIpConfig1 = $lb.FrontendIpConfigurations | Where-Object { $_.Name -eq "new-lb-pip" }
$frontendIpConfig2 = $lb.FrontendIpConfigurations | Where-Object { $_.Name -eq "ip-2" }


#Logic For change on Portal
if ($rule1.BackendPort -eq 8080) {
    
#Change to 8081
	Write-Output "Changing Port to Maintenance"
	Set-AzLoadBalancerRuleConfig -LoadBalancer $lb -Name "to-back-vm-health" -Protocol Tcp -FrontendPort $rule1.FrontendPort -BackendPort 8081 -FrontendIPConfiguration $frontendIpConfig1[0] -BackendAddressPool $BkPool -Probe $MyHealthProbe -IdleTimeoutInMinutes 30 -DisableOutboundSNAT
	$status = "Portal - Maintenance Page"
}
else
{
	Write-Output "Changing Port to Production"
	Set-AzLoadBalancerRuleConfig -LoadBalancer $lb -Name "to-back-vm-health" -Protocol Tcp -FrontendPort $rule1.FrontendPort -BackendPort 8080 -FrontendIPConfiguration $frontendIpConfig1[0] -BackendAddressPool $BkPool -Probe $MyHealthProbe -IdleTimeoutInMinutes 30 -DisableOutboundSNAT
	$status = "Portal - Production"
}

#Logic for change to Calendar

if ($rule2.BackendPort -eq 8086) {
    
#Change to 8081
	Write-Output "Changing Port to Maintenance"
	Set-AzLoadBalancerRuleConfig -LoadBalancer $lb -Name "ip-2" -Protocol Tcp -FrontendPort $rule2.FrontendPort -BackendPort 8087 -FrontendIPConfiguration $frontendIpConfig2[0] -BackendAddressPool $BkPool -Probe $MyHealthProbe -IdleTimeoutInMinutes 30 -DisableOutboundSNAT
	$status = "Calendar - Maintenance Page"
}
else
{
	Write-Output "Changing Port to Production"
	Set-AzLoadBalancerRuleConfig -LoadBalancer $lb -Name "ip-2" -Protocol Tcp -FrontendPort $rule2.FrontendPort -BackendPort 8086 -FrontendIPConfiguration $frontendIpConfig2[0] -BackendAddressPool $BkPool -Probe $MyHealthProbe -IdleTimeoutInMinutes 30 -DisableOutboundSNAT
	$status = "Calendar - Production"
}
#Set the new values to LB
Set-AzLoadBalancer -LoadBalancer $lb

#Describe The Rule
$rule1 = Get-AzLoadBalancerRuleConfig -LoadBalancer $lb -Name "to-back-vm-health"
$rule2 = Get-AzLoadBalancerRuleConfig -LoadBalancer $lb -Name "ip-2"

#Verify Configuration
Write-Host "Your Outbound Port for Rule $($rule1.Name) is: $($rule1.BackendPort) - $status" -ForegroundColor Green
Write-Host "Your Outbound Port for Rule $($rule2.Name) is: $($rule2.BackendPort) - $status" -ForegroundColor Green

