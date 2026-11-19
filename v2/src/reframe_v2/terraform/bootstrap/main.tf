# Creates the Reframe state bucket for one account and region. An administrator
# applies this once. Its own state stays local, because the bucket it creates
# is where every later state goes.

terraform {
  required_version = ">= 1.10.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

variable "region" {
  type = string
}

variable "state_bucket" {
  type = string
  validation {
    condition     = startswith(var.state_bucket, "reframe-")
    error_message = "Reframe-created names start with reframe-, which the bootstrap policy is scoped to."
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      ManagedBy      = "reframe"
      ReframeProject = "reframe-state"
      ReframeRun     = "bootstrap"
    }
  }
}

module "state_bucket" {
  source = "../modules/state_bucket"
  name   = var.state_bucket
}

output "state_bucket" {
  value = module.state_bucket.bucket
}
