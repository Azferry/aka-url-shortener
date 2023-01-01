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

variable "api_webapps" {
  type = object({
    python_version = string
    tier_type = string
    webapps = list(
      object({
        enabled = bool
        config = object({
          location = string
          sku      = string
          os_type  = string
          series = string
        })
      })
    )
  })
  default = {
    python_version = "3.10"
    tier_type = "string"
    webapps = [{
      config = {
        location = "value"
        sku      = "value"
        os_type  = "string"
        series = "series"
      }
      enabled = false
    }]
  }
}

