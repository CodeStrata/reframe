# The Neptune Serverless knowledge graph for one repository (docs/specification.md, section 4, stage 2).
# Used only when the person has no existing graph to reuse, or declines one
# (reframe graph, P2-06); a chosen existing graph is never managed here.
#
# What AWS checks for a reimagine connector, as v1 recorded it (#206) and this
# module guarantees: engine 1.4.5.1 or later, IAM database authentication,
# storage encryption, a serverless scaling configuration, and at least two
# application subnets in different Availability Zones.
#
# The network is the graph's own and private, as AWS's own Neptune template
# builds it: a VPC, two subnets in different Availability Zones, one route
# table and an S3 gateway endpoint, which the bulk loader needs to read the
# source bucket. There is no internet gateway or NAT. No existing network is
# used or changed, and destroying the module removes the network with the
# graph (P2-08, #259).
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

variable "vpc_cidr" {
  description = "The private network's address range. It is never connected to another network, so it may overlap others."
  type        = string
  default     = "10.42.0.0/16"
  validation {
    condition     = can(cidrnetmask(var.vpc_cidr)) && tonumber(split("/", var.vpc_cidr)[1]) <= 24
    error_message = "An IPv4 CIDR block of /24 or larger."
  }
}

variable "final_snapshot" {
  description = "Keep a final snapshot when the graph is deleted. Off only for a disposable test project, so it leaves nothing billable behind."
  type        = bool
  default     = true
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

data "aws_availability_zones" "available" {
  state = "available"
  filter {
    name   = "zone-type"
    values = ["availability-zone"]
  }
}

data "aws_prefix_list" "s3" {
  name = "com.amazonaws.${data.aws_region.current.region}.s3"
}

resource "aws_vpc" "graph" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = { Name = var.name }
}

resource "aws_subnet" "app" {
  count             = 2
  vpc_id            = aws_vpc.graph.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  tags              = { Name = "${var.name}-app-${count.index + 1}" }

  lifecycle {
    precondition {
      condition     = length(data.aws_availability_zones.available.names) >= 2
      error_message = "The reimagine connector needs subnets in two Availability Zones; this region offers fewer."
    }
  }
}

resource "aws_route_table" "app" {
  vpc_id = aws_vpc.graph.id
  tags   = { Name = "${var.name}-app" }
}

resource "aws_route_table_association" "app" {
  count          = 2
  subnet_id      = aws_subnet.app[count.index].id
  route_table_id = aws_route_table.app.id
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.graph.id
  service_name      = "com.amazonaws.${data.aws_region.current.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.app.id]
  tags              = { Name = "${var.name}-s3" }
}

resource "aws_security_group" "app" {
  name        = "${var.name}-app"
  description = "AWS Transform reimagine connector network interfaces"
  vpc_id      = aws_vpc.graph.id
}

resource "aws_security_group" "graph" {
  name        = "${var.name}-graph"
  description = "Neptune cluster: reachable only from the connector security group"
  vpc_id      = aws_vpc.graph.id
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
  subnet_ids = aws_subnet.app[*].id
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
  skip_final_snapshot                 = !var.final_snapshot
  final_snapshot_identifier           = var.final_snapshot ? "${var.name}-final" : null
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
    vpcSubnetIds             = join(",", aws_subnet.app[*].id)
    vpcSecurityGroupId       = aws_security_group.app.id
  }
}

output "vpc_id" {
  value = aws_vpc.graph.id
}
