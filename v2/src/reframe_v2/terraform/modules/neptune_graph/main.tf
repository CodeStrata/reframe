# The Neptune Serverless knowledge graph for one repository (specification section 8).
# Used only when the person has no existing graph to reuse, or declines one
# (reframe graph, P2-06); a chosen existing graph is never managed here.
#
# What AWS checks for a reimagine connector, as v1 recorded it (#206) and this
# module guarantees: engine 1.4.5.1 or later, IAM database authentication,
# storage encryption, a serverless scaling configuration, and at least two
# application subnets in different Availability Zones.
#
# The network is an existing one, normally the account's default VPC, passed
# in by reframe graph. This module creates no VPC, subnet, route table,
# internet gateway or NAT: only the security groups, and an S3 gateway
# endpoint on the route tables that lack one, which AWS documents the Neptune
# bulk loader needs.
#
# Cost: Neptune Serverless bills per NCU-hour for every instance while the
# cluster runs, whether or not a job is running (about $0.16 per NCU-hour in
# us-east-1 when v1 measured it; check current pricing). The network pieces
# have no charge.

variable "name" {
  description = "Name prefix for every resource, starting with reframe-."
  type        = string
  validation {
    condition     = can(regex("^reframe-[a-z0-9-]{1,40}$", var.name))
    error_message = "A name starting with reframe-, lower-case letters, digits and hyphens, at most 48 characters."
  }
}

variable "bucket_name" {
  description = "The repository's source bucket, which the bulk loader reads and the connector uses."
  type        = string
}

variable "vpc_id" {
  description = "The existing VPC the graph goes in; reframe graph proposes the account's default VPC."
  type        = string
}

variable "subnet_ids" {
  description = "Existing subnets in at least two Availability Zones, for the cluster and the connector."
  type        = list(string)
  validation {
    condition     = length(distinct(var.subnet_ids)) >= 2
    error_message = "The reimagine connector needs at least two subnets."
  }
}

variable "s3_endpoint_route_table_ids" {
  description = "Route tables of those subnets that have no S3 gateway endpoint yet; empty when every one has."
  type        = list(string)
  default     = []
}

variable "engine_version" {
  description = "Neptune engine version; AWS requires 1.4.5.1 or later for the reimagine connector."
  type        = string
  default     = "1.4.5.1"
  validation {
    condition = can(regex("^[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+$", var.engine_version)) && (
      tonumber(split(".", var.engine_version)[0]) > 1 || (tonumber(split(".", var.engine_version)[0]) == 1 && (
        tonumber(split(".", var.engine_version)[1]) > 4 || (tonumber(split(".", var.engine_version)[1]) == 4 && (
          tonumber(split(".", var.engine_version)[2]) > 5 || (tonumber(split(".", var.engine_version)[2]) == 5 &&
          tonumber(split(".", var.engine_version)[3]) >= 1)
    )))))
    error_message = "AWS requires Neptune engine 1.4.5.1 or later for the reimagine connector."
  }
}

variable "min_capacity" {
  description = "Minimum NCUs per instance; billed whenever the cluster runs."
  type        = number
  default     = 1
}

variable "max_capacity" {
  description = "Maximum NCUs per instance; the ceiling on spend while a job runs."
  type        = number
  default     = 8
  validation {
    condition     = var.max_capacity >= var.min_capacity
    error_message = "max_capacity is at least min_capacity."
  }
}

variable "instance_count" {
  description = "Serverless instances. v1's test stack ran two; one halves the idle cost."
  type        = number
  default     = 1
  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 3
    error_message = "One to three instances."
  }
}

data "aws_region" "current" {}

data "aws_subnet" "chosen" {
  for_each = toset(var.subnet_ids)
  id       = each.value
}

data "aws_prefix_list" "s3" {
  name = "com.amazonaws.${data.aws_region.current.region}.s3"
}

resource "aws_vpc_endpoint" "s3" {
  count             = length(var.s3_endpoint_route_table_ids) > 0 ? 1 : 0
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.${data.aws_region.current.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = var.s3_endpoint_route_table_ids
  tags              = { Name = "${var.name}-s3" }
}

resource "aws_security_group" "app" {
  name        = "${var.name}-app"
  description = "AWS Transform reimagine connector network interfaces"
  vpc_id      = var.vpc_id

  lifecycle {
    precondition {
      condition     = length(distinct([for s in data.aws_subnet.chosen : s.availability_zone])) >= 2
      error_message = "The reimagine connector needs subnets in two different Availability Zones."
    }
    precondition {
      condition     = alltrue([for s in data.aws_subnet.chosen : s.vpc_id == var.vpc_id])
      error_message = "Every subnet must be in the VPC the graph goes in."
    }
  }
}

resource "aws_security_group" "graph" {
  name        = "${var.name}-graph"
  description = "Neptune cluster: reachable only from the connector security group"
  vpc_id      = var.vpc_id
}

resource "aws_vpc_security_group_ingress_rule" "graph_from_app" {
  security_group_id            = aws_security_group.graph.id
  referenced_security_group_id = aws_security_group.app.id
  ip_protocol                  = "tcp"
  from_port                    = 8182
  to_port                      = 8182
  description                  = "Neptune from the connector only"
}

resource "aws_vpc_security_group_egress_rule" "app_to_graph" {
  security_group_id            = aws_security_group.app.id
  referenced_security_group_id = aws_security_group.graph.id
  ip_protocol                  = "tcp"
  from_port                    = 8182
  to_port                      = 8182
  description                  = "Connector to Neptune"
}

resource "aws_vpc_security_group_egress_rule" "app_to_s3" {
  security_group_id = aws_security_group.app.id
  prefix_list_id    = data.aws_prefix_list.s3.id
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
  description       = "Connector to S3 through the gateway endpoint"
}

# Terraform removes a new security group's default allow-all egress. AWS's own
# template keeps it on the Neptune group because the bulk loader reads S3 from
# the instances; this is that rule, narrowed to S3.
resource "aws_vpc_security_group_egress_rule" "graph_to_s3" {
  security_group_id = aws_security_group.graph.id
  prefix_list_id    = data.aws_prefix_list.s3.id
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
  description       = "Bulk loader to S3 through the gateway endpoint"
}

data "aws_iam_policy_document" "loader_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["rds.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "loader" {
  statement {
    sid       = "ReadSourceBucketOnly"
    effect    = "Allow"
    actions   = ["s3:GetObject", "s3:ListBucket", "s3:GetBucketLocation"]
    resources = ["arn:aws:s3:::${var.bucket_name}", "arn:aws:s3:::${var.bucket_name}/*"]
  }
}

resource "aws_iam_role" "loader" {
  name               = "${var.name}-loader"
  assume_role_policy = data.aws_iam_policy_document.loader_trust.json
}

resource "aws_iam_role_policy" "loader" {
  name   = "${var.name}-loader"
  role   = aws_iam_role.loader.id
  policy = data.aws_iam_policy_document.loader.json
}

resource "aws_neptune_subnet_group" "graph" {
  name       = var.name
  subnet_ids = var.subnet_ids
}

resource "aws_neptune_cluster" "graph" {
  cluster_identifier                  = var.name
  engine                              = "neptune"
  engine_version                      = var.engine_version
  neptune_subnet_group_name           = aws_neptune_subnet_group.graph.name
  vpc_security_group_ids              = [aws_security_group.graph.id]
  iam_database_authentication_enabled = true
  storage_encrypted                   = true
  iam_roles                           = [aws_iam_role.loader.arn]
  skip_final_snapshot                 = false
  final_snapshot_identifier           = "${var.name}-final"
  deletion_protection                 = false

  serverless_v2_scaling_configuration {
    min_capacity = var.min_capacity
    max_capacity = var.max_capacity
  }
}

resource "aws_neptune_cluster_instance" "graph" {
  count              = var.instance_count
  identifier         = "${var.name}-${count.index + 1}"
  cluster_identifier = aws_neptune_cluster.graph.id
  engine             = "neptune"
  instance_class     = "db.serverless"
}

output "cluster_arn" {
  value = aws_neptune_cluster.graph.arn
}

output "cluster_resource_id" {
  value = aws_neptune_cluster.graph.cluster_resource_id
}

output "connector_configuration" {
  description = "The reimagine connector's configuration, under the keys AWS accepted for v1 (#206)."
  value = {
    s3BucketArn              = "arn:aws:s3:::${var.bucket_name}"
    neptuneClusterArn        = aws_neptune_cluster.graph.arn
    neptuneClusterResourceId = aws_neptune_cluster.graph.cluster_resource_id
    neptuneBulkUploadRoleArn = aws_iam_role.loader.arn
    vpcSubnetIds             = join(",", var.subnet_ids)
    vpcSecurityGroupId       = aws_security_group.app.id
  }
}
