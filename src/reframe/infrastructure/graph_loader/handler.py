"""Reframe's graph loader, run inside the run's VPC: Neptune bulk load, load status, and SPARQL, signed with IAM
(docs/pipeline-2.md, stage C7). Every event names the cluster endpoint ("endpoint").

Event: {"action": "load", "source": "s3://...", "role": "<loader role ARN>"}
       {"action": "status", "load_id": "..."}
       {"action": "sparql", "query": "..."}  (SELECT/ASK)
       {"action": "update", "update": "..."}  (SPARQL UPDATE, for example DROP GRAPH)
"""

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

REGION = os.environ["AWS_REGION"]
ENDPOINT = re.compile(r"^[a-z0-9.-]+\.neptune\.amazonaws\.com$")


def _call(endpoint, method, path, body=None, content_type="application/json"):
    url = f"https://{endpoint}:8182{path}"
    data = body.encode() if isinstance(body, str) else body
    request = AWSRequest(method=method, url=url, data=data, headers={"Content-Type": content_type} if data else {})
    SigV4Auth(boto3.Session().get_credentials().get_frozen_credentials(), "neptune-db", REGION).add_auth(request)
    prepared = urllib.request.Request(url, data=data, method=method, headers=dict(request.headers))
    try:
        with urllib.request.urlopen(prepared, timeout=60) as response:
            return {"status": response.status, "body": json.loads(response.read() or b"{}")}
    except urllib.error.HTTPError as error:
        return {"status": error.code, "body": error.read().decode(errors="replace")[:2000]}


def handler(event, context):
    action, endpoint = event.get("action"), str(event.get("endpoint") or "")
    if not ENDPOINT.match(endpoint):  # only a Neptune endpoint, so the function cannot be pointed anywhere else
        return {"status": 400, "body": "endpoint must be a Neptune cluster endpoint"}
    if action == "load":
        body = {"source": event["source"], "format": "nquads", "iamRoleArn": event["role"], "region": REGION,
                "failOnError": "TRUE", "parallelism": "MEDIUM", "updateSingleCardinalityProperties": "FALSE",
                "queueRequest": "TRUE"}
        return _call(endpoint, "POST", "/loader", json.dumps(body))
    if action == "status":
        return _call(endpoint, "GET", f"/loader/{urllib.parse.quote(event['load_id'])}?details=true&errors=true")
    if action == "sparql":
        return _call(endpoint, "POST", "/sparql", urllib.parse.urlencode({"query": event["query"]}), "application/x-www-form-urlencoded")
    if action == "update":
        return _call(endpoint, "POST", "/sparql", urllib.parse.urlencode({"update": event["update"]}), "application/x-www-form-urlencoded")
    return {"status": 400, "body": f"unknown action {action!r}"}
