"""reframe bootstrap (specification section 13, section 8; P2-04).

--print shows the policy an administrator grants the engineer once.
--terraform <dir> writes the Terraform module, the state-bucket definition and
a resources-file template. Neither makes an AWS call or reads credentials.

Every name Reframe creates starts with "reframe-", so the policy is scoped to
those names. AWS Transform's own permissions are not listed: Reframe does not
guess IAM action names, and the administrator grants what the AWS Transform
documentation names for its users.
"""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any

PREFIX = "reframe-"

TRANSFORM_NOTE = ("AWS Transform permissions are not part of this policy. Grant the engineer what the AWS Transform "
                  "documentation names for its users; Reframe does not guess IAM action names.")


def bootstrap_policy() -> dict[str, Any]:
    """The engineer's policy: Reframe's buckets, roles and policies by name prefix, plus read-only checks."""
    bucket, objects = f"arn:aws:s3:::{PREFIX}*", f"arn:aws:s3:::{PREFIX}*/*"
    role, policy = f"arn:aws:iam::*:role/{PREFIX}*", f"arn:aws:iam::*:policy/{PREFIX}*"
    return {
        "Version": "2012-10-17",
        "Statement": [
            {"Sid": "ReadOnlyChecks", "Effect": "Allow",
             "Action": ["sts:GetCallerIdentity", "iam:SimulatePrincipalPolicy", "cloudformation:DescribeStacks",
                        "ec2:DescribeVpcs", "ec2:DescribeVpcAttribute", "ec2:DescribeSubnets", "ec2:DescribeRouteTables",
                        "ec2:DescribeSecurityGroups", "ec2:DescribeSecurityGroupRules", "ec2:DescribeVpcEndpoints",
                        "ec2:DescribePrefixLists", "ec2:DescribeAvailabilityZones", "ec2:DescribeNetworkInterfaces",
                        "ec2:DescribeTags", "rds:DescribeDBClusters", "rds:DescribeDBInstances",
                        "rds:DescribeDBSubnetGroups", "rds:DescribeDBClusterSnapshots"],
             "Resource": "*"},
            {"Sid": "CreateReframeNetworkAndGraphOnlyWhenTagged", "Effect": "Allow",
             "Action": ["ec2:CreateVpc", "ec2:CreateSubnet", "ec2:CreateRouteTable", "ec2:CreateSecurityGroup",
                        "ec2:CreateVpcEndpoint", "rds:CreateDBCluster", "rds:CreateDBInstance", "rds:CreateDBSubnetGroup"],
             "Resource": "*", "Condition": {"StringEquals": {"aws:RequestTag/ManagedBy": "reframe"}}},
            {"Sid": "TagOnlyWhileCreating", "Effect": "Allow", "Action": ["ec2:CreateTags", "rds:AddTagsToResource"],
             "Resource": "*", "Condition": {"StringEquals": {"aws:RequestTag/ManagedBy": "reframe"}}},
            {"Sid": "ChangeOnlyWhatReframeTagged", "Effect": "Allow",
             "Action": ["ec2:DeleteVpc", "ec2:ModifyVpcAttribute", "ec2:DeleteSubnet", "ec2:DeleteRouteTable",
                        "ec2:AssociateRouteTable", "ec2:DisassociateRouteTable", "ec2:DeleteSecurityGroup",
                        "ec2:AuthorizeSecurityGroupIngress", "ec2:AuthorizeSecurityGroupEgress",
                        "ec2:RevokeSecurityGroupIngress", "ec2:RevokeSecurityGroupEgress", "ec2:DeleteVpcEndpoints",
                        "ec2:ModifyVpcEndpoint", "rds:ModifyDBCluster", "rds:DeleteDBCluster", "rds:DeleteDBInstance",
                        "rds:ModifyDBInstance", "rds:DeleteDBSubnetGroup", "rds:ModifyDBSubnetGroup",
                        "rds:AddRoleToDBCluster", "rds:RemoveRoleFromDBCluster", "rds:ListTagsForResource",
                        "rds:CreateDBClusterSnapshot"],
             "Resource": "*", "Condition": {"StringEquals": {"aws:ResourceTag/ManagedBy": "reframe"}}},
            {"Sid": "ReframeBuckets", "Effect": "Allow",
             "Action": ["s3:CreateBucket", "s3:DeleteBucket", "s3:ListBucket", "s3:GetBucketLocation",
                        "s3:GetBucketVersioning", "s3:PutBucketVersioning", "s3:GetEncryptionConfiguration",
                        "s3:PutEncryptionConfiguration", "s3:GetBucketPublicAccessBlock", "s3:PutBucketPublicAccessBlock",
                        "s3:GetBucketOwnershipControls", "s3:PutBucketOwnershipControls", "s3:GetBucketPolicy",
                        "s3:PutBucketPolicy", "s3:DeleteBucketPolicy", "s3:GetBucketTagging", "s3:PutBucketTagging"],
             "Resource": bucket},
            {"Sid": "ReframeObjects", "Effect": "Allow",
             "Action": ["s3:GetObject", "s3:GetObjectVersion", "s3:PutObject", "s3:DeleteObject"],
             "Resource": objects},
            {"Sid": "ReframeRoles", "Effect": "Allow",
             "Action": ["iam:CreateRole", "iam:DeleteRole", "iam:GetRole", "iam:TagRole", "iam:UntagRole",
                        "iam:PutRolePolicy", "iam:GetRolePolicy", "iam:DeleteRolePolicy", "iam:ListRolePolicies",
                        "iam:ListAttachedRolePolicies", "iam:ListInstanceProfilesForRole"],
             "Resource": [role, f"arn:aws:iam::*:role/service-role/{PREFIX}*"]},
            {"Sid": "PassReframeRolesToTransformAndNeptuneOnly", "Effect": "Allow", "Action": "iam:PassRole",
             "Resource": [role, f"arn:aws:iam::*:role/service-role/{PREFIX}*"],
             "Condition": {"StringEquals": {"iam:PassedToService": ["transform.amazonaws.com", "rds.amazonaws.com"]}}},
            {"Sid": "ReframePolicies", "Effect": "Allow",
             "Action": ["iam:CreatePolicy", "iam:DeletePolicy", "iam:GetPolicy", "iam:GetPolicyVersion",
                        "iam:ListPolicyVersions", "iam:TagPolicy"],
             "Resource": policy},
        ],
    }


def print_text() -> str:
    return ("Grant this policy to the engineer who runs Reframe, once per account. It changes nothing by itself.\n\n"
            + json.dumps(bootstrap_policy(), indent=2) + "\n\n" + TRANSFORM_NOTE + "\n")


RESOURCES_TEMPLATE = {
    "schema": "resources_file/1",
    "account": "<12-digit account id>",
    "region": "<region, for example us-east-1>",
    "state_bucket": {"name": "<state bucket>", "write_prefixes": ["projects/<project>/"]},
    "bucket": {"name": "<source bucket>", "write_prefixes": ["reframe/"]},
    "sandbox_role": {"name": "<sandbox role name>"},
    "transform": {"workspace_id": "<workspace id>", "assessment_connector": "<connector id>", "reimagine_connector": None},
    "neptune_stack": None,
}


class BootstrapError(Exception):
    """The files were not written; nothing else changed."""


def _copy(source, target: Path, written: list[Path]) -> None:
    for entry in sorted(source.iterdir(), key=lambda e: e.name):
        if entry.name.startswith((".", "__")):
            continue
        destination = target / entry.name
        if entry.is_dir():
            destination.mkdir()
            _copy(entry, destination, written)
        elif entry.name.endswith((".tf", ".md")):
            destination.write_bytes(entry.read_bytes())
            written.append(destination)


def write_terraform(directory: Path) -> list[Path]:
    """Write the Terraform and a resources-file template into an empty or new folder. No AWS call."""
    if directory.exists() and (not directory.is_dir() or any(directory.iterdir())):
        raise BootstrapError(f"{directory} is not an empty folder; nothing was written")
    directory.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    _copy(resources.files("reframe_v2") / "terraform", directory, written)
    template = directory / "resources.template.json"
    template.write_text(json.dumps(RESOURCES_TEMPLATE, indent=2) + "\n", encoding="utf-8")
    written.append(template)
    return written
