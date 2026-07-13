"""Lab 3: invoke the deployed agent programmatically with the AWS SDK.

Fill in AGENT_ARN from `agentcore status` before running.
Requires the bedrock-agentcore:InvokeAgentRuntime permission.
"""

import json

import boto3

AGENT_ARN = "PASTE_YOUR_AGENT_ARN_HERE"
REGION = "us-west-2"  # change if you deployed elsewhere

client = boto3.client("bedrock-agentcore", region_name=REGION)

payload = json.dumps(
    {
        "prompt": (
            "A customer reports order 1001 is missing. "
            "Summarize what a support agent should check first."
        )
    }
).encode()

response = client.invoke_agent_runtime(
    agentRuntimeArn=AGENT_ARN,
    qualifier="DEFAULT",
    payload=payload,
)

body = response["response"].read()
print(json.loads(body))
