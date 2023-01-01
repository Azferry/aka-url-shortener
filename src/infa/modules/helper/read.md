# Helper

## Location Short Codes

```terraform
module "helper" {
  source = "../modules/helper"
}

locals {
    lookup_geo_codes = module.helper.lookup_geo_codes
    short_location = local.lookup_geo_codes[lower(location)]
}
```
