

module "helper" {
  source = "../modules/helper"
}


resource "azurerm_resource_group" "rg" {
  for_each = local.az_resource_groups
  name     = each.value.name
  location = each.value.location
  tags = each.value.tags
}


module "shared_services" {
    source = "../modules/shared_services"
    location = local.shared_srv_location
    resource_group_name = local.shared_srv_rg
    prefix_name = local.prefix_name
    # Add Tags
}

module "webapps" {
  source   = "../modules/webapp"
  for_each = local.az_webapps
  webapp   = each.value
  log_analytics_id = module.shared_services.log_workspace_id
  key_vault_id = module.shared_services.key_vault_id
  app_settings = {
    HOST_TYPE = "AzWebApp"
    DATACENTER_ID = "WUS2"
    APPINSIGHTS_CONNSTR = "@Microsoft.KeyVault(SecretUri=https://ntc-xas-akau-eus2-n-kv01.vault.azure.net/secrets/application-insights-connstr)"    
  
  }
  depends_on = [
    azurerm_resource_group.rg,
    module.shared_services
  ]
}

resource "azurerm_mssql_server" "sql" {
  for_each                     = local.az_sql_servers
  name                         = each.value.name
  resource_group_name          = each.value.rg_name
  location                     = each.value.location
  version                      = each.value.version
  administrator_login          = each.value.username
  administrator_login_password = each.value.password
  tags                         = each.value.tags

  identity {
    type = "SystemAssigned"
  }
  depends_on = [
    azurerm_resource_group.rg
  ]
}

resource "azurerm_key_vault_secret" "kv_secrets" {
    for_each = local.az_key_vault_secrets
  name         = each.value.key_name
  value        = each.value.value
  key_vault_id = module.shared_services.key_vault_id
  depends_on = [
    module.shared_services
  ]
}

resource "azurerm_mssql_database" "sql" {
  for_each       = local.az_sql_databases
  name           = each.value.name
  server_id      = each.value.server_id
  collation      = each.value.collation
  license_type   = each.value.license_type
#   max_size_gb    = each.value.max_size_gb
  read_scale     = each.value.read_scale
  sku_name       = each.value.sku_name
  zone_redundant = each.value.zone_redundant

  tags = each.value.tags
  depends_on = [
    azurerm_mssql_server.sql,
    azurerm_resource_group.rg
  ]
}

resource "azurerm_redis_cache" "redis" {
  for_each = local.az_redis
  name                = each.value.name
  location            = each.value.location
  resource_group_name = each.value.rg_name
  capacity            = each.value.capacity
  family              = each.value.family
  sku_name            = each.value.sku_name
  enable_non_ssl_port = local.redis_enable_non_ssl_port
  minimum_tls_version = local.redis_tls_version

  redis_configuration {
  }
}

resource "azurerm_key_vault_secret" "redis_host" {
    for_each = azurerm_redis_cache.redis
  name         = "${each.value.name}-host"
  value        = each.value.hostname
  key_vault_id = module.shared_services.key_vault_id
  depends_on = [
    azurerm_redis_cache.redis
  ]
}

resource "azurerm_key_vault_secret" "redis_key" {
    for_each = azurerm_redis_cache.redis
  name         = "${each.value.name}-key"
  value        = each.value.primary_access_key
  key_vault_id = module.shared_services.key_vault_id
  depends_on = [
    azurerm_redis_cache.redis
  ]
}