resource "azurerm_service_plan" "wa" {
  name                = var.webapp.asp_prefix_name
  resource_group_name = var.webapp.rg_name
  location            = var.webapp.location
  os_type             = var.webapp.os_type
  sku_name            = var.webapp.sku
}

resource "azurerm_linux_web_app" "wa" {
  name                = var.webapp.wa_prefix_name
  resource_group_name = var.webapp.rg_name
  location            = var.webapp.location
  service_plan_id     = azurerm_service_plan.wa.id

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }

  app_settings = var.app_settings


  identity {
    type = "SystemAssigned"
  }

  depends_on = [
    azurerm_service_plan.wa
  ]
}

resource "azurerm_key_vault_access_policy" "wa" {
  key_vault_id = var.key_vault_id
  tenant_id    = azurerm_linux_web_app.wa.identity[0].tenant_id
  object_id = azurerm_linux_web_app.wa.identity[0].principal_id

  secret_permissions = [
    "Get",
  ]
  depends_on = [
    azurerm_linux_web_app.wa
  ]
}


resource "azurerm_monitor_diagnostic_setting" "diag" {
  name               = "la_diag_settings"
  target_resource_id = azurerm_linux_web_app.wa.id
  log_analytics_workspace_id = var.log_analytics_id

  log {
    category = "AppServiceAntivirusScanAuditLogs"

    retention_policy {
      enabled = false
    }
  }

  log {
    category = "AppServiceAppLogs"

    retention_policy {
      enabled = false
    }
  }

  log {
    category = "AppServiceAuditLogs"

    retention_policy {
      enabled = false
    }
  }

  log {
    category = "AppServiceConsoleLogs"

    retention_policy {
      enabled = false
    }
  }

  log {
    category = "AppServiceFileAuditLogs"

    retention_policy {
      enabled = false
    }
  }

  log {
    category = "AppServiceHTTPLogs"

    retention_policy {
      enabled = false
    }
  }

  log {
    category = "AppServiceIPSecAuditLogs"

    retention_policy {
      enabled = false
    }
  }

  log {
    category = "AppServicePlatformlogs"

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