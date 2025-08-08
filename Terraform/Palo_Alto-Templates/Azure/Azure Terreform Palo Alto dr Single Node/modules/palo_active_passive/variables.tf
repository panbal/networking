
variable "coid" {
  description = "(Required) the coid"
  type        = string
}

variable "environment" {
  description = "(Required) the environment"
  type        = string
}

variable "location" {
  description = "(Required) the location to build in"
  type        = string
}

variable "location_short" {
  description = "(Required) the location to build in, short name"
  type        = string
}

variable "function" {
  description = "(Optional) Virtual machine administrator password"
  type        = string
}

variable "resource_group_networking" {
  description = "(Required) the resource group to build network components in"
  type        = any
}

variable "resource_group_compute" {
  description = "(Required) the resource group to build compute components in"
  type        = any
}

variable "admin_username" {
  description = "(Required) Virtual machine administrator username"
  type        = string
}

variable "admin_password" {
  description = "(Required) Virtual machine administrator password"
  type        = string
  sensitive   = true
}

variable "hub_address_space" {
  description = "(Required) the hub vnet address space ie. 100.71.64.0/24"
  type        = list(string)
}

variable "virtual_wan_address_space" {
  description = "(Required) the wan hub address space ie. 100.71.65.0/24"
  type        = list(string)
}

variable "mgmt_space_prefix" {
  description = "(Required) the managment subnet ie. 100.71.64.0/28"
  type        = list(string)
}

variable "ha2_space_prefix" {
  description = "(Required) the ha subnet ie. 100.71.64.16/28"
  type        = list(string)
}

variable "private_space_prefix" {
  description = "(Required) the private subnet ie. 100.71.64.32/28"
  type        = list(string)
}

variable "public_space_prefix" {
  description = "(Required) the public subnet ie. 100.71.64.48/28"
  type        = list(string)
}

variable "lb_space_prefix" {
  description = "(Required) the load-balancer subnet ie. 100.71.64.64/28"
  type        = list(string)
}

variable "inbound_tcp_ports" {
  description = "(Optional) the inbound tcp ports"
  type        = list(string)
  default     = [443, 80]
}

variable "inbound_udp_ports" {
  description = "(Optional) the inbound udp ports"
  type        = list(string)
  default     = [500, 4500, 4501]
}
variable "prd_vwan_name" {
  description = "(Required) VWAN service name from PRD - CASE SENSITIVE"
  type        = string
}

variable "prd_vwan_sg" {
  description = "(Required) VWAN RG Name from PRD - CASE SENSITIVE"
  type        = string
}