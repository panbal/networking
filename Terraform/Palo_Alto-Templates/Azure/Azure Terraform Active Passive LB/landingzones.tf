#----------------------------------------------------------------------------------------------------------------------
# Network - HUB
#----------------------------------------------------------------------------------------------------------------------

module "palo_active_passive" {
  source = "./modules/palo_active_passive"

  coid           = local.coid
  environment    = local.environment
  location       = local.location
  location_short = local.location_short
  function       = local.function

  size            = local.size
  zone1           = local.zone1
  zone2           = local.zone2
  psk             = local.psk
  version         = local.version

  shared_space_prefix       = local.shared_space_prefix
  hub_address_space         = local.hub_address_space
  virtual_wan_address_space = local.virtual_wan_address_space
  mgmt_space_prefix         = [cidrsubnet(local.hub_address_space[0], 4, 0)]
  public_space_prefix       = [cidrsubnet(local.hub_address_space[0], 4, 3)]
  private_space_prefix      = [cidrsubnet(local.hub_address_space[0], 4, 2)]
  ha2_space_prefix          = [cidrsubnet(local.hub_address_space[0], 4, 1)]
  lb_space_prefix           = [cidrsubnet(local.hub_address_space[0], 4, 4)]
  resource_group_networking = azurerm_resource_group.resource_group_networking00
  resource_group_compute    = azurerm_resource_group.resource_group_compute00

  admin_username = var.admin_username_networking
  admin_password = var.admin_password_init
}

#----------------------------------------------------------------------------------------------------------------------
# Resource Group
#----------------------------------------------------------------------------------------------------------------------

resource "azurerm_resource_group" "resource_group_compute00" {
  name     = "${local.coid}-${local.location}-compute00-rg"
  location = local.location

  lifecycle {
    ignore_changes = [
      # Ignore changes to tags, e.g. as customers sometimes want to co-mingle their own
      tags,
    ]
  }
}

resource "azurerm_resource_group" "resource_group_networking00" {
  name     = "${local.coid}-${local.location}-networking00-rg"
  location = local.location

  lifecycle {
    ignore_changes = [
      # Ignore changes to tags, e.g. as customers sometimes want to co-mingle their own
      tags,
    ]
  }
}

resource "azurerm_resource_group" "resource_group_management00" {
  name     = "${local.coid}-${local.location}-management00-rg"
  location = local.location

  lifecycle {
    ignore_changes = [
      # Ignore changes to tags, e.g. as customers sometimes want to co-mingle their own
      tags,
    ]
  }
}

resource "azurerm_resource_group" "resource_group_storage00" {
  name     = "${local.coid}-${local.location}-storage00-rg"
  location = local.location

  lifecycle {
    ignore_changes = [
      # Ignore changes to tags, e.g. as customers sometimes want to co-mingle their own
      tags,
    ]
  }
}

#----------------------------------------------------------------------------------------------------------------------
# Storage Accounts
#----------------------------------------------------------------------------------------------------------------------

resource "random_id" "storage_account00" {
  byte_length = 8
}

resource "azurerm_storage_account" "storagediag00" {
  name                = "${lower(local.coid)}${lower(random_id.storage_account00.hex)}"
  resource_group_name = azurerm_resource_group.resource_group_storage00.name

  location                 = local.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  network_rules {
    default_action = "Deny"
  }

  tags = {
    "service" = "diagnostics"
  }

  lifecycle {
    ignore_changes = [
      # Ignore changes to tags, e.g. as customers sometimes want to co-mingle their own
      tags,
    ]
  }

}

resource "random_id" "storage_account01" {
  byte_length = 8
}

resource "azurerm_storage_account" "storagediag01" {
  name                = "${lower(local.coid)}${lower(random_id.storage_account01.hex)}"
  resource_group_name = azurerm_resource_group.resource_group_storage00.name

  location                 = local.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  network_rules {
    default_action = "Deny"
  }

}

#----------------------------------------------------------------------------------------------------------------------
# Diagnostics
#----------------------------------------------------------------------------------------------------------------------

resource "azurerm_monitor_diagnostic_setting" "logs" {
  name                           = "log-export"
  target_resource_id             = "/subscriptions/${var.subscription_id}"
  storage_account_id             = azurerm_storage_account.storagediag01.id
  log_analytics_destination_type = "AzureDiagnostics"

  enabled_log {
    category = "Administrative"
    retention_policy {
      enabled = false
    }
  }

  enabled_log {
    category = "Security"
    retention_policy {
      enabled = false
    }
  }

  lifecycle {
    ignore_changes = [
      # Ignore changes to tags, e.g. as customers sometimes want to co-mingle their own
      log_analytics_destination_type,
    ]
  }
}

#----------------------------------------------------------------------------------------------------------------------
# Backups
#----------------------------------------------------------------------------------------------------------------------

resource "azurerm_recovery_services_vault" "vault01" {
  name                = "${local.coid}-${local.location}-vault00-grs"
  location            = azurerm_resource_group.resource_group_management00.location
  resource_group_name = azurerm_resource_group.resource_group_management00.name
  sku                 = "Standard"
  storage_mode_type   = "GeoRedundant"
}

resource "azurerm_backup_policy_vm" "backup_policy01" {
  name                = "daily-backups00"
  resource_group_name = azurerm_resource_group.resource_group_management00.name
  recovery_vault_name = azurerm_recovery_services_vault.vault01.name

  timezone = "UTC"

  backup {
    frequency = "Daily"
    time      = "05:00"
  }

  retention_daily {
    count = 30
  }
}

resource "azurerm_recovery_services_vault" "vault02" {
  name                = "${local.coid}-${local.location}-vault00-lrs"
  location            = azurerm_resource_group.resource_group_management00.location
  resource_group_name = azurerm_resource_group.resource_group_management00.name
  sku                 = "Standard"
  storage_mode_type   = "LocallyRedundant"
}

resource "azurerm_backup_policy_vm" "backup_policy02" {
  name                = "daily-backups01"
  resource_group_name = azurerm_resource_group.resource_group_management00.name
  recovery_vault_name = azurerm_recovery_services_vault.vault02.name

  timezone = "UTC"

  backup {
    frequency = "Daily"
    time      = "05:00"
  }

  retention_daily {
    count = 30
  }
}