
/* Base Variables */
locals {
  tenant_prefix     = var.tenant_prefix
  tags_map          = var.tags
  environment       = var.environment
  environment_short = module.helper.lookup_env_codes[lower(local.environment)]
  application_label = var.application_label
  network_type = var.network_type
  base_module_tags = merge(local.tags_map, {
    deployedBy  = "terraform"
    Label       = var.application_label
    Environment = var.environment
    TenantCode  = var.tenant_prefix
  })

  /* Short Code Lookups*/
  lookup_geo_codes = module.helper.lookup_geo_codes
  lookup_net_codes = module.helper.lookup_net_codes
  lookup_tenant_codes = module.helper.lookup_tenant_codes
  short_network_type = local.lookup_net_codes[local.network_type]
  short_tenant_prefix = local.lookup_tenant_codes[local.tenant_prefix]
  /* Config variable configs*/
  api_webapps = var.api_webapps
  api_webapps_config = [for v in var.api_webapps.webapps : v.config if v.enabled]
}

/* Get Current Subscription */
data "azurerm_subscription" "current" {}

/* Resource Groups */
locals {
  location_merge         = concat(local.api_webapps_config[*].location)
  distinct_azure_regions = distinct(local.location_merge)

  az_resource_groups = {
    for i in local.distinct_azure_regions : i => {
      resource_id = "${data.azurerm_subscription.current.id}/resourceGroups/${local.tenant_prefix}-xas-${local.application_label}-${local.lookup_geo_codes[lower(i)]}-${local.environment_short}-rg01"
      name        = "${local.tenant_prefix}-${local.network_type}-${local.application_label}-${local.lookup_geo_codes[lower(i)]}-${local.environment_short}-rg01"
      location    = i
      tags        = merge(local.base_module_tags, { LocationShort = local.lookup_geo_codes[lower(i)] })
    }
  }
}

/* API Web Apps */
locals {
    python_version = local.api_webapps.python_version
    tier_type = local.api_webapps.tier_type
    webapps_merge = concat(local.api_webapps_config[*]) 
    webapps_by_location = {
        for i in local.webapps_merge: i["location"] => i...
    }
    
    webapps = flatten([
        for wa in local.webapps_by_location : [
            for a in wa : {
                python_version = local.python_version
                location = a.location
                sku = a.sku
                os_type = a.os_type
                series = "${a.series}"
                asp_prefix_name = "${local.tenant_prefix}-${local.network_type}-${local.application_label}-${local.lookup_geo_codes[lower(a.location)]}-${local.environment_short}-asp${a.series}-${local.tier_type}"
                wa_prefix_name = "${local.tenant_prefix}-${local.network_type}-${local.application_label}-${local.lookup_geo_codes[lower(a.location)]}-${local.environment_short}-wa${a.series}-${local.tier_type}"
                rg_name = local.az_resource_groups[a.location].name
                tags = local.az_resource_groups[a.location].name
                # sa_prefix_name = "${local.short_tenant_prefix}${local.short_network_type}${local.application_label}${local.lookup_geo_codes[lower(a.location)]}${local.environment_short}sa${a.series}${local.tier_type}"
            }
        ]
    ])
    az_webapps = {
        for i in local.webapps : i.asp_prefix_name => i
    }


}
# asp, fa, wa

locals {
  DEBUG = {
    /* Base Variables */
    # api_webapps_config = local.api_webapps_config

    /* Resource Groups */
    # location_merge = local.location_merge
    # distinct_azure_regions = local.distinct_azure_regions
    # az_resource_groups = local.az_resource_groups

    /* API Web Apps */
    # python_version = local.python_version
    # webapps_merge = local.webapps_merge
    # webapps_by_location = local.webapps_by_location
    # webapps = local.webapps
    # az_webapps = local.az_webapps

  }
}
output "DEBUG" {
  value = local.DEBUG
}
