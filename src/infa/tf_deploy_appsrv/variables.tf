variable "tenant_prefix" {
  type    = string
  default = "ntc"
}

variable "application_label" {
  type = string
}

variable "environment" {
  type    = string
  default = "npd"
}

variable "tags" {
  type        = map(any)
  description = "Tags placed on resource group"
  default     = {}
}

variable "network_type" {
  type = string
}

variable "virtual_networks" {
  type = object({
    vnets = list(object({
      enabled  = bool
      series   = string
      location = string
      address_prefix = list(string)
      subnets = list(object({
        name           = string
        address_prefix = string
        })
      )
    }))
  })
}

variable "api_webapps" {
  type = object({
    python_version = string
    tier_type      = string
    webapps = list(
      object({
        enabled = bool
        config = object({
          location = string
          sku      = string
          os_type  = string
          series   = string
        })
      })
    )
  })
  description = "Web App Config"
}


variable "sql_db" {
  type = object({
    sql_servers = list(object({
      enabled  = bool
      series   = string
      location = string
      version  = string
      databases = list(object({
        name           = string
        max_size_gb    = number
        read_scale     = bool
        sku_name       = string
        zone_redundant = bool
        })
      )
    }))
  })
}

variable "redis" {
  type = object({
    redisconfig = list(object({
      enabled  = bool
      series   = string
      location = string
      sku_name = string
      capacity  = number
      family = string
    }))
  })
}
