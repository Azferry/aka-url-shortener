
/* Base Variables */
locals {
  tenant_prefix     = var.tenant_prefix
  tags_map          = var.tags
  environment       = var.environment
  environment_short = module.helper.lookup_env_codes[lower(local.environment)]
  application_label = var.application_label
  network_type      = var.network_type
  base_module_tags = merge(local.tags_map, {
    deployedBy  = "terraform"
    Label       = var.application_label
    Environment = var.environment
    TenantCode  = var.tenant_prefix
  })

  /* Short Code Lookups*/
  lookup_geo_codes    = module.helper.lookup_geo_codes
  lookup_net_codes    = module.helper.lookup_net_codes
  lookup_tenant_codes = module.helper.lookup_tenant_codes
  short_network_type  = local.lookup_net_codes[local.network_type]
  short_tenant_prefix = local.lookup_tenant_codes[local.tenant_prefix]
  
  /* Config variable configs*/
  api_webapps        = var.api_webapps
  api_webapps_config = [for v in var.api_webapps.webapps : v.config if v.enabled]
  sql_servers        = [for i in var.sql_db.sql_servers : i if i.enabled]
  redis_cache = [for i in var.redis.redisconfig : i if i.enabled]
}

/* Get Current Subscription */
data "azurerm_subscription" "current" {}
data "azurerm_client_config" "current" {}

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


/* shared_services */
locals {
  shared_srv_location = "eastus2"
  shared_srv_rg = local.az_resource_groups[local.shared_srv_location].name
  prefix_name = "${local.tenant_prefix}-${local.network_type}-${local.application_label}-${local.lookup_geo_codes[lower(local.shared_srv_location)]}-${local.environment_short}"
}

/* API Web Apps */
locals {
  python_version = local.api_webapps.python_version
  tier_type      = local.api_webapps.tier_type
  webapps_merge  = concat(local.api_webapps_config[*])
  webapps_by_location = {
    for i in local.webapps_merge : i["location"] => i...
  }

  webapps = flatten([
    for wa in local.webapps_by_location : [
      for a in wa : {
        python_version  = local.python_version
        location        = a.location
        sku             = a.sku
        os_type         = a.os_type
        series          = "${a.series}"
        asp_prefix_name = "${local.tenant_prefix}-${local.network_type}-${local.application_label}-${local.lookup_geo_codes[lower(a.location)]}-${local.environment_short}-asp${a.series}-${local.tier_type}"
        wa_prefix_name  = "${local.tenant_prefix}-${local.network_type}-${local.application_label}-${local.lookup_geo_codes[lower(a.location)]}-${local.environment_short}-wa${a.series}-${local.tier_type}"
        rg_name         = local.az_resource_groups[a.location].name
        tags            = merge(local.base_module_tags, { LocationShort = local.lookup_geo_codes[lower(a.location)] })
        # sa_prefix_name = "${local.short_tenant_prefix}${local.short_network_type}${local.application_label}${local.lookup_geo_codes[lower(a.location)]}${local.environment_short}sa${a.series}${local.tier_type}"
      }
    ]
  ])
  az_webapps = {
    for i in local.webapps : i.asp_prefix_name => i
  }

}
# asp, fa, wa

/* Redis Cache */
locals {
    redis_tls_version = "1.2"
    redis_enable_non_ssl_port = false
    redis_by_location = {
        for i in local.redis_cache : i["location"] => i...
    }

    redis = flatten([
    for rc in local.redis_by_location : [
      for a in rc : {
        location = a.location
        series = a.series
        family = a.family
        capacity = a.capacity
        sku_name = a.sku_name
        name = "${local.tenant_prefix}-${local.network_type}-${local.application_label}-${local.lookup_geo_codes[lower(a.location)]}-${local.environment_short}-redis${a.series}"
        rg_name = local.az_resource_groups[a.location].name
      }
    ]])

    az_redis = {
        for i in local.redis : i.name => i
    }

}
/* SQL DB */
locals {
  sql_servers_by_location = {
    for i in local.sql_servers : i.location => i...
  }
  sql_servers_config = flatten([
    for sq in local.sql_servers_by_location : [
      for a in sq : {
        location  = a.location
        version   = a.version
        name      = "${local.tenant_prefix}-${local.network_type}-${local.application_label}-${local.lookup_geo_codes[lower(a.location)]}-${local.environment_short}-sql${a.series}"
        databases = a.databases
        rg_name   = local.az_resource_groups[a.location].name
        server_id = "${data.azurerm_subscription.current.id}/resourceGroups/${local.az_resource_groups[a.location].name}/providers/Microsoft.Sql/servers/${local.tenant_prefix}-${local.network_type}-${local.application_label}-${local.lookup_geo_codes[lower(a.location)]}-${local.environment_short}-sql${a.series}"
        tags      = merge(local.base_module_tags, { LocationShort = local.lookup_geo_codes[lower(a.location)] })
        username = "NTCAdmin"
        password = "MSFTusa!!2020"
      }
    ]
  ])

  az_sql_servers = {
    for i in local.sql_servers_config : i.name => i
  }

  sql_dbs_flatten = flatten([
    for server in local.az_sql_servers : [
      for db in server.databases : {
        name            = db.name
        sql_server_name = server.name
        max_size_gb     = db.max_size_gb
        read_scale      = db.read_scale
        sku_name        = db.sku_name
        collation       = "SQL_Latin1_General_CP1_CI_AS"
        license_type    = "LicenseIncluded"
        zone_redundant  = db.zone_redundant
        server_id       = server.server_id
        tags            = merge(local.base_module_tags, { LocationShort = local.lookup_geo_codes[lower(server.location)] })
      }
    ]
  ])

  az_sql_databases = {
    for i in local.sql_dbs_flatten : i.sql_server_name => i
  }
}
# @Microsoft.KeyVault(VaultName=myvault;SecretName=mysecret)

/* KV Secrets */
locals {
  kv_id = "${data.azurerm_subscription.current.id}/resourceGroups/ntc-xas-akau-eus2-n-rg01/providers/Microsoft.KeyVault/vaults/ntc-xas-akau-eus2-n-kv01"
  kv_secrets_sql_host = {
    for i in local.az_sql_servers : "${i.name}host" => {
        key_name = "${i.name}-host"
        value = "${i.name}.database.windows.net"
        key_vault_id = local.kv_id
    }
  }

  kv_secrets_sql_user = {
    for i in local.az_sql_servers : "${i.name}usr" => {
        key_name = "${i.name}-usr"
        value = i.username
        key_vault_id = local.kv_id
    }
  }

  kv_secrets_sql_pw = {
    for i in local.az_sql_servers : "${i.name}pw" => {
        key_name = "${i.name}-pw"
        value = i.password
        key_vault_id = local.kv_id
    }
  }

  az_key_vault_secrets = merge(local.kv_secrets_sql_host, 
                                local.kv_secrets_sql_user,
                                local.kv_secrets_sql_pw)
}

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

    /* Redis */
    # redis_cache = local.redis_cache
    # redis_by_location = local.redis_by_location
    # redis = local.redis

    /* SQL Servers */
    # sql_servers_by_location = local.sql_servers_by_location
    # sql_servers = local.sql_servers
    # sql_servers_config = local.sql_servers_config
    # sql_dbs_flatten = local.sql_dbs_flatten
    # az_sql_servers = local.az_sql_servers
    # az_sql_databases = local.az_sql_databases

    /* Key Vault Keys */
    # kv_secrets_sql_host = local.kv_secrets_sql_host
    # az_key_vault_secrets = local.az_key_vault_secrets
  }
}
output "DEBUG" {
  value = local.DEBUG
}
