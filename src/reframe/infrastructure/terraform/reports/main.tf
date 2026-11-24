# The published reports' private bucket (docs/sharing.md, section 4). One per account and region, apart from any run:
# only people who can sign in to the account and read S3 can open the reports. State stays on the owner's computer, in
# ~/.reframe/reports-store, and the bucket is removed only by reframe reports teardown.

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

variable "bucket_name" {
  type = string
  validation {
    condition     = can(regex("^reframe-reports-[a-z0-9]{8}$", var.bucket_name))
    error_message = "The bucket name Reframe chose: reframe-reports- and eight lower-case letters or digits."
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      ManagedBy    = "reframe"
      ReframeStore = "reports"
    }
  }
}

resource "aws_s3_bucket" "reports" {
  bucket        = var.bucket_name
  force_destroy = true # teardown lists the bucket and its object count and asks for consent first
}

resource "aws_s3_bucket_ownership_controls" "reports" {
  bucket = aws_s3_bucket.reports.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "reports" {
  bucket                  = aws_s3_bucket.reports.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "reports" {
  bucket = aws_s3_bucket.reports.id
  versioning_configuration {
    status = "Enabled"
  }
}

data "aws_iam_policy_document" "tls_only" {
  statement {
    sid     = "RefuseRequestsNotOverTLS"
    effect  = "Deny"
    actions = ["s3:*"]
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    resources = [aws_s3_bucket.reports.arn, "${aws_s3_bucket.reports.arn}/*"]
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "reports" {
  bucket     = aws_s3_bucket.reports.id
  policy     = data.aws_iam_policy_document.tls_only.json
  depends_on = [aws_s3_bucket_public_access_block.reports]
}

output "bucket" {
  value = aws_s3_bucket.reports.id
}
