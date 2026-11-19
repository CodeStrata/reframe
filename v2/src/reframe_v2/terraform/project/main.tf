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

variable "reimagine" {
  description = "Set up the reimagine connector's graph and role: either the existing graph the person chose, or a new graph."
  type        = bool
  default     = false
}

variable "existing_graph" {
  description = "The existing Neptune cluster the person chose by name (reframe graph). Used as client-owned: never managed here."
  type = object({
    cluster_arn         = string
    cluster_resource_id = string
    configuration       = map(string)
  })
  default = null
  validation {
    condition = try(length(setsubtract(["s3BucketArn", "neptuneClusterArn", "neptuneClusterResourceId", "neptuneBulkUploadRoleArn",
    "vpcSubnetIds", "vpcSecurityGroupId"], keys(var.existing_graph.configuration))) == 0, var.existing_graph == null)
    error_message = "The existing graph needs all six connector values; reframe graph writes them."
  }
}

variable "graph_network" {
  description = "Where a new graph goes, normally the account's default VPC (reframe graph). Nothing here is created except the S3 endpoint on the listed route tables."
  type = object({
    vpc_id                      = string
    subnet_ids                  = list(string)
    s3_endpoint_route_table_ids = list(string)
  })
  default = null
  validation {
    condition     = !var.reimagine || ((var.existing_graph == null) != (var.graph_network == null))
    error_message = "With reimagine, give either existing_graph or graph_network, not both; reframe graph writes the one you chose."
  }
}

variable "neptune_max_capacity" {
  description = "Maximum NCUs per Neptune instance: the ceiling on graph spend while a job runs."
  type        = number
  default     = 8
}

variable "neptune_instance_count" {
  type    = number
  default = 1
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

module "neptune_graph" {
  source                      = "../modules/neptune_graph"
  count                       = var.reimagine && var.existing_graph == null ? 1 : 0
  name                        = "reframe-${var.project}-kg"
  bucket_name                 = module.repo.bucket
  vpc_id                      = try(var.graph_network.vpc_id, null)
  subnet_ids                  = try(var.graph_network.subnet_ids, null)
  s3_endpoint_route_table_ids = try(var.graph_network.s3_endpoint_route_table_ids, [])
  max_capacity                = var.neptune_max_capacity
  instance_count              = var.neptune_instance_count
}

locals {
  graph = !var.reimagine ? null : var.existing_graph != null ? {
    cluster_arn         = var.existing_graph.cluster_arn
    cluster_resource_id = var.existing_graph.cluster_resource_id
    configuration       = var.existing_graph.configuration
    } : {
    cluster_arn         = module.neptune_graph[0].cluster_arn
    cluster_resource_id = module.neptune_graph[0].cluster_resource_id
    configuration       = tomap(module.neptune_graph[0].connector_configuration)
  }
}

module "reimagine_role" {
  source              = "../modules/reimagine_role"
  count               = var.reimagine ? 1 : 0
  role_name           = "reframe-${var.project}-rmg"
  bucket_name         = trimprefix(local.graph.configuration["s3BucketArn"], "arn:aws:s3:::")
  cluster_arn         = local.graph.cluster_arn
  cluster_resource_id = local.graph.cluster_resource_id
}

output "reimagine_connector" {
  description = "What the Transform adapter creates the reimagine connector from; null without reimagine."
  value = var.reimagine ? {
    configuration = local.graph.configuration
    role_arn      = module.reimagine_role[0].role_arn
    graph         = var.existing_graph != null ? "existing" : "created"
  } : null
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
