resource "azurerm_monitor_diagnostic_setting" "sqlDiag" {
    for_each = azurerm_mssql_database.sql
  name               = "la_diag_settings"
  target_resource_id = each.value.id#azurerm_mssql_server.sql.id
  log_analytics_workspace_id = module.shared_services.log_workspace_id

  log {
    category = "SQLInsights"

    retention_policy {
      enabled = false
    }
  }
  log {
    category = "AutomaticTuning"

    retention_policy {
      enabled = false
    }
  }
  log {
    category = "QueryStoreRuntimeStatistics"

    retention_policy {
      enabled = false
    }
  }
  log {
    category = "QueryStoreWaitStatistics"

    retention_policy {
      enabled = false
    }
  }
  log {
    category = "Errors"

    retention_policy {
      enabled = false
    }
  }
  log {
    category = "DatabaseWaitStatistics"

    retention_policy {
      enabled = false
    }
  }
  log {
    category = "Timeouts"

    retention_policy {
      enabled = false
    }
  }
  log {
    category = "Blocks"

    retention_policy {
      enabled = false
    }
  }
  log {
    category = "Deadlocks"

    retention_policy {
      enabled = false
    }
  }


  metric {
    category = "Basic"

    retention_policy {
      enabled = false
    }
  }
  metric {
    category = "InstanceAndAppAdvanced"

    retention_policy {
      enabled = false
    }
  }
  metric {
    category = "WorkloadManagement"

    retention_policy {
      enabled = false
    }
  }
  
  lifecycle {
    ignore_changes = [
       log,metric
    ]
  }
}

resource "azurerm_monitor_diagnostic_setting" "redisDiag" {
    for_each = azurerm_redis_cache.redis
  name               = "la_diag_settings"
  target_resource_id = each.value.id#azurerm_mssql_server.sql.id
  log_analytics_workspace_id = module.shared_services.log_workspace_id

  log {
    category = "ConnectedClientList"

    retention_policy {
      enabled = false
    }
  }


  metric {
    category = "AllMetrics"

    retention_policy {
      enabled = false
    }
  }
  lifecycle {
    ignore_changes = [
     log, metric
    ]
  }
}