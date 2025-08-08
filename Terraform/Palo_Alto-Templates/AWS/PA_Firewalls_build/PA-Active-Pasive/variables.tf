variable "aws_access_key_id" {
  description = "(Required) IAM user Access Key"
  type        = string
}

variable "aws_secret_access_key" {
  description = "(Required) IAM user Secret Access Key"
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
  description = "(Required) HUB VPC cidr"
  type        = list
}

variable "instance_type" {
  description = "(Required) Instance Size"
  type        = string
}

variable "aws_region" {
  description = "(Required) AWS region for deployment"
  type        = string
}

variable "aws_availability_zone" {
  description = "(Required) AWS Availability Zone for deployment - Single AZ"
  type        = string
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