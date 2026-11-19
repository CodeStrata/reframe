# One repository's resources, created by reframe run --provision.
# State lives in the Reframe state bucket with S3 locking; Reframe passes the
# bucket, key and region at init (terraform init -backend-config=...).

terraform {
  required_version = ">= 1.10.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
  backend "s3" {
    use_lockfile = true
    encrypt      = true
  }
}

variable "region" {
  type = string
}

variable "project" {
  type = string
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{0,62}$", var.project))
    error_message = "A project name: lower-case letters, digits and hyphens."
  }
}

variable "run" {
  type = string
}

variable "bucket_name" {
  type = string
  validation {
    condition     = startswith(var.bucket_name, "reframe-")
    error_message = "Reframe-created names start with reframe-, which the bootstrap policy is scoped to."
  }
}

variable "role_name" {
  type = string
  validation {
    condition     = startswith(var.role_name, "reframe-")
    error_message = "Reframe-created names start with reframe-, which the bootstrap policy is scoped to."
  }
}

variable "bedrock_model_arns" {
  description = "Pinned Bedrock models or inference profiles; empty for the claude-cli backend."
  type        = list(string)
  default     = []
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

module "repo" {
  source      = "../modules/repo"
  bucket_name = var.bucket_name
  role_name   = var.role_name
}

module "bedrock_invoke" {
  source      = "../modules/bedrock_invoke"
  count       = length(var.bedrock_model_arns) > 0 ? 1 : 0
  policy_name = "reframe-${var.project}-bedrock-invoke"
  model_arns  = var.bedrock_model_arns
}

output "bucket" {
  value = module.repo.bucket
}

output "role_name" {
  value = module.repo.role_name
}

output "write_prefix" {
  value = module.repo.write_prefix
}
