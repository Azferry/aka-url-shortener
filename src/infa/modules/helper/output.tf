output "lookup_geo_codes" {
  value = local.geo_short_codes
  description = "List of geolocations mapped to location short codes for naming conventions"
}

output "lookup_env_codes" {
    value = local.env_short_codes
    description = "List of environment codes and reduced to 1 char"
}