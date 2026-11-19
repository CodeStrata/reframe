# One repository's resources (specification section 8): the encrypted, versioned
# source bucket with public access blocked, and the sandbox role AWS Transform
# assumes, which denies reads outside that bucket. Ported from v1's sandbox
# definitions after review (docs/v2/port-or-drop.md).

variable "bucket_name" {
  description = "Source bucket for this repository."
  type        = string
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$", var.bucket_name))
    error_message = "An S3 bucket name: 3 to 63 lower-case letters, digits, dots and hyphens."
  }
}

variable "role_name" {
  description = "Sandbox role for this repository."
  type        = string
  validation {
    condition     = can(regex("^[A-Za-z0-9+=,.@_-]{1,64}$", var.role_name))
    error_message = "An IAM role name of at most 64 characters."
  }
}

variable "write_prefix" {
  description = "Prefix Reframe writes under, ending in a slash."
  type        = string
  default     = "reframe/"
  validation {
    condition     = can(regex("^[A-Za-z0-9!_.*'()-]+(/[A-Za-z0-9!_.*'()-]+)*/$", var.write_prefix))
    error_message = "A key prefix ending in a slash."
  }
}

data "aws_caller_identity" "current" {}

data "aws_iam_session_context" "current" {
  arn = data.aws_caller_identity.current.arn
}

resource "aws_s3_bucket" "source" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_ownership_controls" "source" {
  bucket = aws_s3_bucket.source.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "source" {
  bucket                  = aws_s3_bucket.source.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "source" {
  bucket = aws_s3_bucket.source.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "source" {
  bucket = aws_s3_bucket.source.id
  versioning_configuration {
    status = "Enabled"
  }
}

data "aws_iam_policy_document" "trust" {
  statement {
    sid     = "TransformAssumesInThisAccount"
    effect  = "Allow"
    actions = ["sts:AssumeRole", "sts:SetContext"]
    principals {
      type        = "Service"
      identifiers = ["transform.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [data.aws_caller_identity.current.account_id]
    }
  }

  statement {
    sid     = "DenyCheck"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "AWS"
      identifiers = [data.aws_iam_session_context.current.issuer_arn]
    }
  }
}

data "aws_iam_policy_document" "sandbox" {
  statement {
    sid       = "ListSource"
    effect    = "Allow"
    actions   = ["s3:ListBucket", "s3:GetBucketLocation"]
    resources = [aws_s3_bucket.source.arn]
  }

  statement {
    sid    = "UseSource"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:AbortMultipartUpload",
      "s3:ListMultipartUploadParts",
      "s3:PutObjectTagging",
    ]
    resources = ["${aws_s3_bucket.source.arn}/*"]
  }

  statement {
    sid           = "DenyReadsOutsideSource"
    effect        = "Deny"
    actions       = ["s3:GetObject", "s3:GetObjectVersion", "s3:ListBucket"]
    not_resources = [aws_s3_bucket.source.arn, "${aws_s3_bucket.source.arn}/*"]
  }
}

resource "aws_iam_role" "sandbox" {
  name               = var.role_name
  assume_role_policy = data.aws_iam_policy_document.trust.json
}

resource "aws_iam_role_policy" "sandbox" {
  name   = "${var.role_name}-boundary"
  role   = aws_iam_role.sandbox.id
  policy = data.aws_iam_policy_document.sandbox.json
}

output "bucket" {
  value = aws_s3_bucket.source.id
}

output "role_name" {
  value = aws_iam_role.sandbox.name
}

output "write_prefix" {
  value = var.write_prefix
}
