# The run's Terraform state bucket (docs/specification.md, section 4, stage 2).
# Its own state stays in the run folder, because the bucket it creates is where
# the project root's state goes. Each run is disposable: destroy removes the
# bucket with everything in it, after the project root is destroyed.

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

variable "project" {
  type = string
}

variable "run" {
  type = string
}

variable "state_bucket" {
  type = string
  validation {
    condition     = startswith(var.state_bucket, "reframe-")
    error_message = "Reframe-created names start with reframe-."
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      ManagedBy      = "reframe"
      ReframeProject = var.project
      ReframeRun     = var.run
    }
  }
}

module "state_bucket" {
  source        = "../modules/state_bucket"
  name          = var.state_bucket
  force_destroy = true
}

output "state_bucket" {
  value = module.state_bucket.bucket
}
