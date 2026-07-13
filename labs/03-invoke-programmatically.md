# Lab 3: Invoke Programmatically

So far you have invoked the agent as a human at a terminal. In production,
agents are usually invoked by other software: an EventBridge rule fires when
something happens, a Lambda function handles the event, and that Lambda calls
the agent through the `InvokeAgentRuntime` API. The CLI and the API hit the
same endpoint; the caller is the only difference.

In this lab you make that API call yourself with boto3.

## 1. Get your agent ARN

```bash
agentcore status
```

Copy the agent ARN from the output. It is also in the hidden
`.bedrock_agentcore.yaml` file in `src/`.

## 2. Look at the code

Open [`src/invoke_agent.py`](../src/invoke_agent.py):

```python
import json
import boto3

AGENT_ARN = "PASTE_YOUR_AGENT_ARN_HERE"
REGION = "us-west-2"  # change if you deployed elsewhere

client = boto3.client("bedrock-agentcore", region_name=REGION)

payload = json.dumps({"prompt": "A customer reports order 1001 is missing. Summarize what a support agent should check first."}).encode()

response = client.invoke_agent_runtime(
    agentRuntimeArn=AGENT_ARN,
    qualifier="DEFAULT",
    payload=payload,
)

body = response["response"].read()
print(json.loads(body))
```

There is no `agentcore` CLI here. This is plain AWS SDK code, which is
exactly what an EventBridge target Lambda would run. Your IAM identity signs
the request (SigV4), Runtime authorizes it, and a fresh isolated session is
opened for the call.

## 3. Run it

Edit the file to paste your ARN, then:

```bash
python src/invoke_agent.py
```

You should see the model's answer printed, fetched from the same deployed
agent, through the same endpoint, without the CLI.

Your identity needs the `bedrock-agentcore:InvokeAgentRuntime` permission for
this call. If you attached `AmazonBedrockAgentCoreFullAccess` in Lab 0, you
have it.

## 4. Where to go from here

To make this fully event-driven, create an EventBridge rule whose target is a
small Lambda containing code like the above. The pattern is: an event occurs,
the Lambda handler runs, the handler calls `InvokeAgentRuntime`, and the
agent works the problem. Runtime supports long-running work in the same
session for up to eight hours, so extended jobs are supported.

When you are done experimenting, tear everything down:
[`99-cleanup.md`](99-cleanup.md).
