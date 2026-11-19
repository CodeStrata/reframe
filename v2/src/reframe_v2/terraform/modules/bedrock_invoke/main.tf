# Bedrock invoke permission for the Bedrock backend only (specification section 8):
# InvokeModel on the pinned models or inference profiles, and nothing else.
# Model access itself is an administrator's one-time step that Reframe checks read-only.

variable "policy_name" {
  type = string
}

variable "model_arns" {
  description = "The pinned foundation-model and inference-profile ARNs from the project policy."
  type        = list(string)
  validation {
    condition     = length(var.model_arns) > 0 && alltrue([for arn in var.model_arns : can(regex("^arn:aws[a-z-]*:bedrock:", arn))])
    error_message = "At least one Bedrock model or inference-profile ARN; a wildcard is never used."
  }
  validation {
    condition     = alltrue([for arn in var.model_arns : !strcontains(arn, "*")])
    error_message = "Name each pinned model or inference profile exactly; a wildcard is never used."
  }
}

data "aws_iam_policy_document" "invoke" {
  statement {
    sid       = "InvokePinnedModelsOnly"
    effect    = "Allow"
    actions   = ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"]
    resources = var.model_arns
  }
}

resource "aws_iam_policy" "invoke" {
  name   = var.policy_name
  policy = data.aws_iam_policy_document.invoke.json
}

output "policy_name" {
  value = aws_iam_policy.invoke.name
}
