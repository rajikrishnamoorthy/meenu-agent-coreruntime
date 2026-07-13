# Lab 2: Add a Model

The echo agent proved the hosting works. Now you replace the echo with a real
reasoning step: a call to a Claude model through the Strands Agents framework.

## 1. Look at the new code

Open [`src/agent_with_brain.py`](../src/agent_with_brain.py):

```python
from strands import Agent
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()
agent = Agent()

@app.entrypoint
def invoke(payload):
    user_message = payload.get("prompt", "Hello")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()
```

Two lines changed everything. `Agent()` creates a Strands agent that calls a
Bedrock model (Claude, by default) in your account. The entrypoint now hands
the user's message to the agent instead of echoing it. The hosting contract
(`BedrockAgentCoreApp`, `@app.entrypoint`) is unchanged.

This is why Lab 0 asked you to enable Claude model access. If you skipped
that step, do it now.

## 2. Reconfigure and relaunch

From the `src` directory:

```bash
agentcore configure --entrypoint agent_with_brain.py --name supportagent --disable-memory
agentcore launch
```

Accept the same defaults as before. The toolkit updates the deployment to run
the new entrypoint.

## 3. Ask it something real

```bash
agentcore invoke '{"prompt": "Explain in two sentences what a serverless runtime is."}'
```

This time the reply is not an echo. The request travelled into the isolated
session, the agent called the model, and a generated answer came back.

## 4. Read the logs

Every invocation leaves a trail. Run:

```bash
agentcore status
```

Copy the `aws logs tail` command it prints and run it to stream the agent's
logs from CloudWatch: the request arriving, the model being called, the
answer going out.

For full tracing of every reasoning step and tool call (via OpenTelemetry),
enable CloudWatch Transaction Search once per account. See
[AgentCore observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html).

## What the agent still cannot do

It has hosting and a model, but no persistent memory (each conversation
starts from zero) and no tools (it cannot check a real order system). Those
are separate AgentCore services: **Memory** and **Gateway**. This lab stops
at Runtime on purpose, but the toolkit makes both easy to add. Try running
`agentcore configure` without `--disable-memory` and read the memory prompts
it offers.

Next: [`03-invoke-programmatically.md`](03-invoke-programmatically.md).
