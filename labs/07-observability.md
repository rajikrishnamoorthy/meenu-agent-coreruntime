# Lab 7: Observability with CloudWatch and OpenTelemetry

An agent you cannot see is a black box. AgentCore emits telemetry in the
OpenTelemetry (OTel) standard, and CloudWatch collects it: every session,
every model call, every tool invocation, timed and traced.

Enabling it has two independent parts. Neither depends on the other's
configuration, but you need both for full traces.

## 1. One-time account setup: CloudWatch Transaction Search

Traces need somewhere to land. In the AWS console:

1. Open **CloudWatch**, then **Application Signals (APM) > Transaction
   Search**.
2. Choose **Enable Transaction Search**.
3. Check the box to ingest spans as structured logs. You can raise the
   X-Ray trace indexing percentage from the default 1% while learning; set
   it back later, as indexing above 1% has cost.

This is once per account per Region. Details:
[AgentCore observability configuration](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html).

## 2. Instrument the agent

The agent process must emit OTel data. For starter toolkit deployments this
is handled by having `aws-opentelemetry-distro` in the `requirements.txt`
that gets packaged with your agent. This repo's requirements file already
includes it, so simply redeploy:

```bash
cd src
agentcore launch
```

## 3. Generate traffic and look at the traces

Invoke the agent several times with different prompts:

```bash
agentcore invoke '{"prompt": "Summarize what AgentCore Runtime does."}'
agentcore invoke '{"prompt": "List three uses for session isolation."}'
```

Then, in the CloudWatch console, open the **GenAI Observability** page and
choose the **Bedrock AgentCore** view. You should see your agent, its
sessions, and traces breaking each invocation into spans: the request
arriving, the model call, the response. If you completed Lab 5, Gateway tool
calls appear in traces too.

Logs remain available as before:

```bash
agentcore status        # prints the exact aws logs tail commands
```

## 4. Close the loop with an alarm

Observability is more than watching; it is wired to act. Create a CloudWatch
alarm on an agent metric (for example, errors on the runtime's log group or
latency from Transaction Search) and give it an action: notify an SNS topic
that emails the on-call engineer, or trigger a Lambda function. The pattern
to remember: metric crosses threshold, alarm fires, action runs, before a
customer feels it.

Next: [`99-cleanup.md`](99-cleanup.md).
