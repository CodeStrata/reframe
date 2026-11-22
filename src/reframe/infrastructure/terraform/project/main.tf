# One run's resources (docs/specification.md, section 4, stage 2): the source
# bucket and sandbox role, the Neptune graph with its private network, and the
# reimagine connector's role. State lives in the run's state bucket; Reframe
# passes the bucket, key and region at init. Each run is disposable: destroy
# deletes the source bucket with its contents and the graph without a final
# snapshot, so nothing billable is left behind.

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
    condition     = can(regex("^[a-z0-9][a-z0-9-]{0,29}$", var.project))
    error_message = "A project name: lower-case letters, digits and hyphens, at most 30."
  }
}

variable "run" {
  type = string
  validation {
    condition     = can(regex("^[0-9a-f]{6}$", var.run))
    error_message = "A run id: six hexadecimal characters."
  }
}

variable "neptune_max_capacity" {
  description = "Maximum NCUs per Neptune instance: the ceiling on graph spend while a job runs."
  type        = number
  default     = 8
}

variable "existing_graph" {
  description = "An existing Neptune cluster the person chose, used exactly as it is: never managed, changed or destroyed here."
  type = object({
    name                = string
    cluster_arn         = string
    cluster_resource_id = string
    configuration       = map(string)
  })
  default = null
  validation {
    condition = var.existing_graph == null || try(length(setsubtract(["s3BucketArn", "neptuneClusterArn", "neptuneClusterResourceId",
    "neptuneBulkUploadRoleArn", "vpcSubnetIds", "vpcSecurityGroupId"], keys(var.existing_graph.configuration))) == 0, false)
    error_message = "An existing graph needs all six connector values."
  }
}

locals {
  prefix = "reframe-${var.project}-${var.run}"
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
  source        = "../modules/repo"
  bucket_name   = "${local.prefix}-src"
  role_name     = "${local.prefix}-sandbox"
  force_destroy = true
}

module "neptune_graph" {
  source         = "../modules/neptune_graph"
  count          = var.existing_graph == null ? 1 : 0
  name           = "${local.prefix}-kg"
  bucket_name    = module.repo.bucket
  max_capacity   = var.neptune_max_capacity
  instance_count = 1
  final_snapshot = false
}

locals {
  graph = var.existing_graph != null ? {
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
  role_name           = "${local.prefix}-rmg"
  bucket_name         = module.repo.bucket
  cluster_arn         = local.graph.cluster_arn
  cluster_resource_id = local.graph.cluster_resource_id
}

output "bucket" {
  value = module.repo.bucket
}

output "reimagine_connector" {
  description = "What Reframe creates the reimagine connector from."
  value = {
    configuration = local.graph.configuration
    role_arn      = module.reimagine_role.role_arn
    graph         = var.existing_graph != null ? "existing" : "new"
  }
}
