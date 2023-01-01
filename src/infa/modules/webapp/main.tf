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

  site_config {}

  depends_on = [
    azurerm_service_plan.wa
  ]
}