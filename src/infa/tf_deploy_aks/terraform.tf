terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.29.0"
    }
  }

  required_version = ">= 0.15.1"
}

provider "azurerm" {
  features {}
}
