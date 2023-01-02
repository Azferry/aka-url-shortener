

module "helper" {
  source = "../modules/helper"
}


resource "azurerm_resource_group" "rg" {
  for_each = local.az_resource_groups
  name     = each.value.name
  location = each.value.location
  tags = each.value.tags
}


module "webapps" {
  source   = "../modules/webapp"
  for_each = local.az_webapps
  webapp   = each.value

  depends_on = [
    azurerm_resource_group.rg
  ]
}

resource "azurerm_mssql_server" "sql" {
  for_each                     = local.az_sql_servers
  name                         = each.value.name
  resource_group_name          = each.value.rg_name
  location                     = each.value.location
  version                      = each.value.version
  administrator_login          = "NTCAdmin"
  administrator_login_password = "MSFTusa!!2020"
  tags                         = each.value.tags
  depends_on = [
    azurerm_resource_group.rg
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

resource "azurerm_log_analytics_workspace" "appin" {
  name                = local.law_name
  location            = local.app_insights_location
  resource_group_name = local.app_insights_rg
  sku                 = "PerGB2018"
  retention_in_days   = local.appinsight_retention
}

resource "azurerm_application_insights" "appin" {
  name                = local.appi_name
  location            = local.app_insights_location
  resource_group_name = local.app_insights_rg
  workspace_id        = azurerm_log_analytics_workspace.appin.id
  application_type    = "web"
}
