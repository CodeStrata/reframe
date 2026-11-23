# Pipeline 2's graph loader (docs/pipeline-2.md, stage C7; spike P2-02). The Neptune cluster has no public
# endpoint and admits port 8182 only from the run's app security group, so a small Lambda function in the app
# subnets with that group starts bulk loads (N-Quads, through the cluster's own bulk-loader role) and runs SPARQL,
# signed with IAM. Reframe passes the cluster endpoint with each call.

variable "name" {
  type = string
  validation {
    condition     = can(regex("^reframe-[A-Za-z0-9-]{1,48}$", var.name))
    error_message = "A name starting with reframe-, at most 56 characters."
  }
}

variable "zip" {
  description = "The function's package, built by Reframe from reframe/infrastructure/graph_loader/handler.py."
  type        = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_group_id" {
  type = string
}

variable "cluster_resource_id" {
  type = string
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_partition" "current" {}

data "aws_iam_policy_document" "trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "loader" {
  statement {
    sid = "Graph"
    actions = ["neptune-db:connect", "neptune-db:StartLoaderJob", "neptune-db:GetLoaderJobStatus", "neptune-db:ReadDataViaQuery",
    "neptune-db:WriteDataViaQuery", "neptune-db:DeleteDataViaQuery"]
    resources = ["arn:${data.aws_partition.current.partition}:neptune-db:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:${var.cluster_resource_id}/*"]
  }
  statement {
    sid = "Network"
    actions = ["ec2:CreateNetworkInterface", "ec2:DescribeNetworkInterfaces", "ec2:DeleteNetworkInterface",
    "ec2:AssignPrivateIpAddresses", "ec2:UnassignPrivateIpAddresses"]
    resources = ["*"]
  }
  statement {
    sid       = "Logs"
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.loader.arn}:*"]
  }
}

resource "aws_cloudwatch_log_group" "loader" {
  name              = "/aws/lambda/${var.name}"
  retention_in_days = 7
}

resource "aws_iam_role" "loader" {
  name               = var.name
  assume_role_policy = data.aws_iam_policy_document.trust.json
}

resource "aws_iam_role_policy" "loader" {
  name   = var.name
  role   = aws_iam_role.loader.id
  policy = data.aws_iam_policy_document.loader.json
}

resource "aws_lambda_function" "loader" {
  function_name    = var.name
  role             = aws_iam_role.loader.arn
  runtime          = "python3.12"
  handler          = "handler.handler"
  filename         = var.zip
  source_code_hash = filebase64sha256(var.zip)
  timeout          = 120
  memory_size      = 256
  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [var.security_group_id]
  }
  logging_config {
    log_format = "Text"
    log_group  = aws_cloudwatch_log_group.loader.name
  }
  depends_on = [aws_iam_role_policy.loader]
}

output "function_name" {
  value = aws_lambda_function.loader.function_name
}
