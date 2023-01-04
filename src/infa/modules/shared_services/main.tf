 
 data "azurerm_subscription" "current" {}
data "azurerm_client_config" "current" {}
 
 resource "azurerm_key_vault" "kv" {
  name                        = "${var.prefix_name}-kv01"
  location                    = var.location
  resource_group_name         = var.resource_group_name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false
  sku_name = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    key_permissions = [
      "Get",
    ]

    secret_permissions = [
      "Set",
      "Get",
      "List",
      "Delete",
      "Purge",
      "Recover"
    ]
  }
}

resource "azurerm_log_analytics_workspace" "appin" {
  name                = "${var.prefix_name}-log01"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 60
}

resource "azurerm_application_insights" "appin" {
  name                = "${var.prefix_name}-appi01"
  location            = var.location
  resource_group_name = var.resource_group_name
  workspace_id        = azurerm_log_analytics_workspace.appin.id
  application_type    = "web"
}

resource "azurerm_key_vault_secret" "appin" {
  name         = "application-insights-connstr"
  value        = azurerm_application_insights.appin.connection_string
  key_vault_id = azurerm_key_vault.kv.id
}

output "appi_connection_string" {
  value = azurerm_application_insights.appin.connection_string
}

output "key_vault_id" {
  value = azurerm_key_vault.kv.id
}

output "log_workspace_id" {
  value = azurerm_log_analytics_workspace.appin.id
}