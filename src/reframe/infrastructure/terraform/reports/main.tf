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
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
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

variable "site" {
  description = "The link that asks for the AWS sign-in (docs/sharing.md section 5): CloudFront, Cognito and the edge check."
  type        = bool
  default     = false
}

variable "idp_metadata_url" {
  description = "The IAM Identity Center application's SAML metadata URL, from the Identity Center administrator."
  type        = string
  default     = ""
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

# Lambda@Edge functions live in us-east-1.
provider "aws" {
  alias  = "edge"
  region = "us-east-1"
  default_tags {
    tags = {
      ManagedBy    = "reframe"
      ReframeStore = "reports"
    }
  }
}

data "aws_iam_policy_document" "tls_only" {
  dynamic "statement" {
    for_each = var.site ? [1] : []
    content {
      sid       = "CloudFrontReadsReports"
      effect    = "Allow"
      actions   = ["s3:GetObject"]
      resources = ["${aws_s3_bucket.reports.arn}/*"]
      principals {
        type        = "Service"
        identifiers = ["cloudfront.amazonaws.com"]
      }
      condition {
        test     = "StringEquals"
        variable = "AWS:SourceArn"
        values   = [aws_cloudfront_distribution.site[0].arn]
      }
    }
  }
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

# ---- the link that asks for the AWS sign-in (S-06, S-07) ----------------------------------------------------------------

locals {
  idp       = var.idp_metadata_url == "" ? "" : "IdentityCenter"
  providers = var.idp_metadata_url == "" ? ["COGNITO"] : ["IdentityCenter"]
}

resource "aws_cognito_user_pool" "site" {
  count               = var.site ? 1 : 0
  name                = var.bucket_name
  deletion_protection = "INACTIVE"
  admin_create_user_config {
    allow_admin_create_user_only = true # no one signs up: the only way in is IAM Identity Center
  }
}

resource "aws_cognito_user_pool_domain" "site" {
  count        = var.site ? 1 : 0
  domain       = var.bucket_name
  user_pool_id = aws_cognito_user_pool.site[0].id
}

resource "aws_cognito_identity_provider" "identity_center" {
  count         = var.site && var.idp_metadata_url != "" ? 1 : 0
  user_pool_id  = aws_cognito_user_pool.site[0].id
  provider_name = "IdentityCenter"
  provider_type = "SAML"
  provider_details = {
    MetadataURL = var.idp_metadata_url
  }
  attribute_mapping = {
    email = "email"
  }
}

resource "aws_cognito_user_pool_client" "site" {
  count                                = var.site ? 1 : 0
  name                                 = "reframe-reports"
  user_pool_id                         = aws_cognito_user_pool.site[0].id
  generate_secret                      = false
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_scopes                 = ["openid", "email", "profile"]
  callback_urls                        = ["https://localhost/_reframe/callback"] # set to the CloudFront address below
  supported_identity_providers         = local.providers
  explicit_auth_flows                  = ["ALLOW_REFRESH_TOKEN_AUTH"]
  prevent_user_existence_errors        = "ENABLED"
  id_token_validity                    = 60
  token_validity_units {
    id_token = "minutes"
  }
  lifecycle {
    ignore_changes = [callback_urls, logout_urls]
  }
  depends_on = [aws_cognito_identity_provider.identity_center]
}

data "aws_iam_policy_document" "edge_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com", "edgelambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "edge" {
  count              = var.site ? 1 : 0
  name               = "${var.bucket_name}-edge"
  assume_role_policy = data.aws_iam_policy_document.edge_trust.json
}

resource "aws_iam_role_policy_attachment" "edge_logs" {
  count      = var.site ? 1 : 0
  role       = aws_iam_role.edge[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "archive_file" "edge" {
  count       = var.site ? 1 : 0
  type        = "zip"
  output_path = "${path.module}/edge.zip"
  source {
    filename = "index.mjs"
    content  = file("${path.module}/edge.mjs")
  }
  source {
    filename = "config.json"
    content = jsonencode({
      pool   = aws_cognito_user_pool.site[0].id
      client = aws_cognito_user_pool_client.site[0].id
      domain = "${aws_cognito_user_pool_domain.site[0].domain}.auth.${var.region}.amazoncognito.com"
      region = var.region
      idp    = local.idp
    })
  }
}

resource "aws_lambda_function" "edge" {
  count            = var.site ? 1 : 0
  provider         = aws.edge
  function_name    = "${var.bucket_name}-edge"
  role             = aws_iam_role.edge[0].arn
  runtime          = "nodejs20.x"
  handler          = "index.handler"
  filename         = data.archive_file.edge[0].output_path
  source_code_hash = data.archive_file.edge[0].output_base64sha256
  publish          = true
  timeout          = 5
  memory_size      = 128
}

resource "aws_cloudfront_origin_access_control" "site" {
  count                             = var.site ? 1 : 0
  name                              = var.bucket_name
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "site" {
  count       = var.site ? 1 : 0
  enabled     = true
  comment     = "Reframe reports: the AWS sign-in before any page"
  price_class = "PriceClass_100"
  origin {
    origin_id                = "reports"
    domain_name              = aws_s3_bucket.reports.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.site[0].id
  }
  default_cache_behavior {
    target_origin_id       = "reports"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    cache_policy_id        = "658327ea-f89d-4fab-a63d-7e88639e58f6" # CachingOptimized; the sign-in check runs before the cache
    lambda_function_association {
      event_type = "viewer-request"
      lambda_arn = aws_lambda_function.edge[0].qualified_arn
    }
  }
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# The sign-in returns to the CloudFront address, which exists only after the distribution: set it on the client then.
resource "terraform_data" "callback" {
  count            = var.site ? 1 : 0
  triggers_replace = [aws_cloudfront_distribution.site[0].domain_name, aws_cognito_user_pool_client.site[0].id, join(",", local.providers)]
  provisioner "local-exec" {
    command = join(" ", [
      "aws cognito-idp update-user-pool-client --region ${var.region}",
      "--user-pool-id ${aws_cognito_user_pool.site[0].id} --client-id ${aws_cognito_user_pool_client.site[0].id} --client-name reframe-reports",
      "--callback-urls https://${aws_cloudfront_distribution.site[0].domain_name}/_reframe/callback",
      "--allowed-o-auth-flows code --allowed-o-auth-flows-user-pool-client --allowed-o-auth-scopes openid email profile",
      "--supported-identity-providers ${join(" ", local.providers)} --explicit-auth-flows ALLOW_REFRESH_TOKEN_AUTH",
      "--prevent-user-existence-errors ENABLED --id-token-validity 60 --token-validity-units IdToken=minutes --output json > /dev/null",
    ])
  }
}

output "site" {
  value = var.site ? {
    url             = "https://${aws_cloudfront_distribution.site[0].domain_name}"
    acs_url         = "https://${aws_cognito_user_pool_domain.site[0].domain}.auth.${var.region}.amazoncognito.com/saml2/idpresponse"
    audience        = "urn:amazon:cognito:sp:${aws_cognito_user_pool.site[0].id}"
    identity_center = var.idp_metadata_url != ""
  } : null
}
