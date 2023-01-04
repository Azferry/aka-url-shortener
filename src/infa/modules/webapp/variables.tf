variable "webapp" {
  type = object({
    python_version = string
    # tier_type = string
    location = string
    sku      = string
    os_type  = string
    series = string
    asp_prefix_name = string
    wa_prefix_name = string
    rg_name = string
  })
}

variable "log_analytics_id" {
  type = string
}