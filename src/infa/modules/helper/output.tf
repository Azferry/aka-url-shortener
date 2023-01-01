output "lookup_geo_codes" {
  value = local.geo_short_codes
  description = "List of geolocations mapped to location short codes for naming conventions"
}

output "lookup_env_codes" {
    value = local.environment_short_codes
    description = "List of environment codes and reduced to 1 char"
}

output "lookup_net_codes" {
    value = local.network_short_codes
    description = "List the network short code types"
}

output "lookup_tenant_codes" {
    value = local.tenant_short_codes
    description = "provide 3 char tenant code and returns 2 char tenant code"
  
}