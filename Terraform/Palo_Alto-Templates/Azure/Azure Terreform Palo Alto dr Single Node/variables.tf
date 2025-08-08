variable "tenant_id" {
  description = "(Required) Globaly Unique Identifier (GUID) for your Microsoft Tenant"
  type        = string
}

variable "subscription_id" {
  description = "(Required) Globaly Unique Identifier (GUID) for your Microsoft Subscription within a Tenant"
  type        = string
}

variable "client_id" {
  description = "(Required) Application ID used to associate your application with Azure AD at runtime"
  type        = string
}

variable "client_secret" {
  description = "(Required) Application secret used for the service principal (App registration)"
  type        = string
  sensitive   = true
}

variable "admin_username_networking" {
  description = "(Required) Virtual machine administrator username for network resources"
  type        = string
}

variable "admin_password_init" {
  description = "(Required) Virtual machine administrator password used during bootstrap (unchanging). This is not needed if ssh_key_value_init is supplied"
  type        = string
  sensitive   = true
}

variable "hub_address" {
  description = "(Required) HUB vnet cidr"
  type        = list
}

variable "vwan_address" {
  description = "(Required) vwan CIDR"
  type        = list
}
variable "company_coid" {
  description = "(Required) COID"
  type        = string
}

variable "company_env" {
  description = "(Required) Environment (PROD, QAS, SBX, DEV)"
  type        = string
}

variable "company_location" {
  description = "(Required) Region"
  type        = string
}

variable "company_location_short" {
  description = "(Required) Region initial (eg e: east, w: west)"
  type        = string
}

variable "prd_vwan_name_id" {
  description = "(Required) PRD VWAN name - CASE SENSITIVE"
  type        = string
}

variable "prd_vwan_rg" {
  description = "(Required) PRD vWAN RG - CASE SENSITIVE"
  type        = string
}