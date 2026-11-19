# The reimagine connector's IAM role (specification section 8). Its trust and
# permissions mirror what the AWS console generates for this connector, as v1
# recorded and used live (#206). AWS Transform assumes it; the connector
# itself is created by the Transform adapter from the graph's outputs.

variable "role_name" {
  type = string
  validation {
    condition     = can(regex("^reframe-[A-Za-z0-9+=,.@_-]{1,56}$", var.role_name))
    error_message = "A role name starting with reframe-, at most 64 characters."
  }
}

variable "bucket_name" {
  type = string
}

variable "cluster_arn" {
  type = string
}

variable "cluster_resource_id" {
  type = string
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_partition" "current" {}

locals {
  p         = data.aws_partition.current.partition
  region    = data.aws_region.current.region
  account   = data.aws_caller_identity.current.account_id
  bucket    = "arn:${local.p}:s3:::${var.bucket_name}"
  interface = "arn:${local.p}:ec2:${local.region}:${local.account}:network-interface/*"
  tag       = "ManagedByAWSTransform"
}

data "aws_iam_policy_document" "trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole", "sts:SetContext"]
    principals {
      type        = "Service"
      identifiers = ["transform.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [local.account]
    }
    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = ["arn:${local.p}:transform:${local.region}:${local.account}:connector/*"]
    }
  }
}

data "aws_iam_policy_document" "connector" {
  statement {
    effect    = "Allow"
    actions   = ["s3:GetBucketLocation", "s3:ListBucket", "s3:GetObject", "s3:ListMultipartUploadParts", "s3:ListBucketMultipartUploads", "s3:GetBucketPublicAccessBlock"]
    resources = ["${local.bucket}/*", local.bucket]
    condition {
      test     = "StringEquals"
      variable = "aws:ResourceAccount"
      values   = [local.account]
    }
  }
  statement {
    effect    = "Allow"
    actions   = ["s3:GetAccountPublicAccessBlock"]
    resources = ["*"]
    condition {
      test     = "StringEquals"
      variable = "aws:ResourceAccount"
      values   = [local.account]
    }
  }
  statement {
    effect    = "Allow"
    actions   = ["s3:PutObject", "s3:AbortMultipartUpload"]
    resources = ["${local.bucket}/transform-output/*"]
    condition {
      test     = "StringEquals"
      variable = "aws:ResourceAccount"
      values   = [local.account]
    }
  }
  statement {
    sid       = "AllowS3Deletes"
    effect    = "Allow"
    actions   = ["s3:DeleteObject"]
    resources = ["${local.bucket}/transform-output/neptune-quads/*"]
    condition {
      test     = "StringEquals"
      variable = "aws:ResourceAccount"
      values   = [local.account]
    }
  }
  statement {
    effect    = "Allow"
    actions   = ["ec2:DescribeDhcpOptions", "ec2:DescribeNetworkInterfaces", "ec2:DescribeSubnets", "ec2:DescribeSecurityGroups", "ec2:DescribeVpcs"]
    resources = ["*"]
  }
  statement {
    effect    = "Allow"
    actions   = ["ec2:CreateNetworkInterfacePermission"]
    resources = [local.interface]
  }
  statement {
    effect    = "Allow"
    actions   = ["ec2:CreateTags"]
    resources = [local.interface]
    condition {
      test     = "StringEquals"
      variable = "aws:RequestTag/${local.tag}"
      values   = [""]
    }
    condition {
      test     = "StringEquals"
      variable = "ec2:CreateAction"
      values   = ["CreateNetworkInterface"]
    }
  }
  statement {
    effect    = "Allow"
    actions   = ["ec2:DeleteNetworkInterface"]
    resources = ["*"]
    condition {
      test     = "StringEquals"
      variable = "aws:ResourceTag/${local.tag}"
      values   = [""]
    }
  }
  statement {
    effect    = "Allow"
    actions   = ["ec2:CreateNetworkInterface"]
    resources = ["arn:${local.p}:ec2:${local.region}:${local.account}:subnet/*", "arn:${local.p}:ec2:${local.region}:${local.account}:security-group/*"]
  }
  statement {
    effect    = "Allow"
    actions   = ["ec2:CreateNetworkInterface"]
    resources = [local.interface]
    condition {
      test     = "ForAnyValue:StringEquals"
      variable = "aws:TagKeys"
      values   = [local.tag]
    }
  }
  statement {
    effect    = "Allow"
    actions   = ["ec2:ModifyNetworkInterfaceAttribute"]
    resources = [local.interface]
    condition {
      test     = "Null"
      variable = "aws:ResourceTag/${local.tag}"
      values   = ["false"]
    }
  }
  statement {
    effect    = "Allow"
    actions   = ["ec2:ModifyNetworkInterfaceAttribute"]
    resources = ["arn:${local.p}:ec2:${local.region}:*:instance/*"]
  }
  statement {
    sid       = "AllowNeptuneDBAccess"
    effect    = "Allow"
    actions   = ["neptune-db:ReadDataViaQuery", "neptune-db:DeleteDataViaQuery", "neptune-db:StartLoaderJob", "neptune-db:GetLoaderJobStatus", "neptune-db:CancelLoaderJob", "neptune-db:ListLoaderJobs", "neptune-db:GetQueryStatus"]
    resources = ["arn:${local.p}:neptune-db:${local.region}:${local.account}:${var.cluster_resource_id}/*"]
  }
  statement {
    sid       = "AllowNeptuneDescribe"
    effect    = "Allow"
    actions   = ["rds:DescribeDBClusters"]
    resources = [var.cluster_arn]
  }
}

resource "aws_iam_role" "connector" {
  name               = var.role_name
  path               = "/service-role/"
  assume_role_policy = data.aws_iam_policy_document.trust.json
}

resource "aws_iam_role_policy" "connector" {
  name   = "${var.role_name}-connector"
  role   = aws_iam_role.connector.id
  policy = data.aws_iam_policy_document.connector.json
}

output "role_arn" {
  value = aws_iam_role.connector.arn
}
