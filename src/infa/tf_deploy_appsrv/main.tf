

module "helper" {
  source = "../modules/helper"
}


resource "azurerm_resource_group" "rg" {
  for_each = local.az_resource_groups
  name     = each.value.name
  location = each.value.location
}


module "webapps" {
  source = "../modules/webapp"
  for_each = local.az_webapps
  webapp = each.value
}