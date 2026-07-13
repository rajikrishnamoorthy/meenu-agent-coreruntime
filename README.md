# Amazon Bedrock AgentCore: Hands-On Lab

A hands-on lab covering the core services of **Amazon Bedrock AgentCore**:
Runtime, Memory, Gateway, Identity (JWT inbound auth), and Observability.
You deploy a real agent to your own AWS account and add one capability per
lab.

## Lab sequence

| Lab | Service | What you do |
|---|---|---|
| [00](labs/00-setup.md) | — | Credentials, IAM policies, model access, Python env |
| [01](labs/01-deploy-a-minimal-agent.md) | Runtime | Deploy an echo agent; understand session-isolated microVMs |
| [02](labs/02-add-a-model.md) | Runtime | Add a Bedrock model via Strands Agents |
| [03](labs/03-invoke-programmatically.md) | Runtime | Invoke with `InvokeAgentRuntime` (boto3), the event-driven pattern |
| [04](labs/04-memory.md) | Memory | Short-term events, long-term strategies, cross-session recall |
| [05](labs/05-gateway-tools.md) | Gateway | Turn a Lambda into an MCP tool; connect the agent to it |
| [06](labs/06-identity-cognito-auth.md) | Identity | Cognito user pool, JWT bearer tokens, and the no-token rejection test |
| [07](labs/07-observability.md) | Observability | Transaction Search, OpenTelemetry instrumentation, traces, alarms |
| [99](labs/99-cleanup.md) | — | Tear everything down |

Labs 1-3 are the core and must be done in order. Labs 4-7 each build on
Lab 2's deployed agent but are otherwise independent of one another.

## Prerequisites

Work through [`labs/00-setup.md`](labs/00-setup.md) first. In short:

- An AWS account with credentials configured (`aws configure`)
- IAM permissions: `AmazonBedrockAgentCoreFullAccess` plus the starter
  toolkit caller policy (admins can skip; links in the setup doc). Labs 5
  and 6 additionally create Lambda, Cognito, and IAM resources, so a
  personal or sandbox account with broad permissions is easiest.
- Python 3.10 or later
- Anthropic Claude model access enabled in the Amazon Bedrock console, in
  your working Region (the toolkit defaults to `us-west-2`)
- No Docker required. The default deployment path builds in the cloud.

## Cost note

The labs create real resources: an AgentCore Runtime agent, a Memory store,
a Gateway with a demo Lambda, a Cognito user pool, IAM roles, and CloudWatch
log groups, and they make Bedrock model calls. A single run-through costs
little, but not nothing. Two specific flags: long-term Memory stores and
raised X-Ray trace indexing percentages have ongoing cost, so run the
cleanup lab when you finish.

## A note on tooling

This lab uses the Python **bedrock-agentcore-starter-toolkit** and its
`agentcore` commands. AWS also ships a newer Node-based **AgentCore CLI**
(`agentcore create / deploy / add gateway / add memory`) for new projects.
Once you finish this lab, see
[Get started with the AgentCore CLI](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-get-started-cli.html).

The AgentCore services evolve quickly. Where a script mirrors SDK calls
(Memory, Gateway), treat it as the documented shape and confirm parameter
names against the current SDK if something errors.

## Repo layout

```
labs/     Step-by-step instructions, in order
src/      Agent code, setup scripts, and cleanup scripts
```

Start with [`labs/00-setup.md`](labs/00-setup.md).
