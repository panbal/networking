variable "tenant_id" {
  description = "(Required) Globaly Unique Identifier (GUID) for your Microsoft Tenant"
  type        = string
  default     = ""
}

variable "subscription_id" {
  description = "(Required) Globaly Unique Identifier (GUID) for your Microsoft Subscription within a Tenant"
  type        = string
  default     = ""
}

variable "client_id" {
  description = "(Required) Application ID used to associate your application with Azure AD at runtime"
  type        = string
  sensitive   = true
}

variable "client_secret" {
  description = "(Required) Application secret used for the service principal (App registration)"
  type        = string
  sensitive   = true
}

variable "version" {
  description = "(Required) Firewall Version"
  type        = string
  default     = "10.2.901"
}

variable "size" {
  description = "(Required) size of the vm-series firewalls"
  type        = string
  default     = "Standard_DS3_v2"
}

variable "zone1" {
  description = "(Required) Zone for firewall 1"
  type        = string
  default     = "1"
}

variable "zone2" {
  description = "(Required) Zone for firewall 2"
  type        = string
  default     = "2"
}

variable "psk" {
  description = "(Required) PSK for on-premise Tunnel"
  type        = string
  default     = ""
}


variable "admin_username_networking" {
  description = "(Required) Virtual machine administrator username for network resources"
  type        = string
  default     = "company"
}

variable "admin_password_init" {
  description = "(Required) Virtual machine administrator password used during bootstrap (unchanging). This is not needed if ssh_key_value_init is supplied"
  type        = string
  default     = "compEr@2024"
}

variable "hub_address" {
  description = "(Required) HUB vnet cidr - Second /24 of the assigned CIDR - Firewall VNET-Do not change format"
  type        = list
  default     = ["10.161.11.0/24"]   

}

variable "shared_space_prefix" {
  description = "(Required) Shared subnet CIDR - Second /25 of the HUB vnet"
  type        = list
  default     = ["10.161.11.128/25"]
}

variable "vwan_address" {
  description = "(Required) vwan CIDR - First /24 of the assigned CIDR"
  type        = list
  default     = ["10.161.10.0/24"]
}
variable "company_coid" {
  description = "(Required) COID"
  type        = string
  default     = "comp"

}

variable "company_env" {
  description = "(Required) Environment (PROD, QAS, SBX, DEV)"
  type        = string
  default     = "PROD"
}

variable "company_location" {
  description = "(Required) Region (westus, centralus, westus2, eastus, eastus2)"
  type        = string
  default     = "centralus"
}

variable "company_location_short" {
  description = "(Required) Region initial (eg e: east, w: west, c: central)"
  type        = string
  default     = "c"
}