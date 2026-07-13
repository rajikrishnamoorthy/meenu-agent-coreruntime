# Lab 1: Deploy a Minimal Agent

In this lab you deploy the smallest possible agent to AgentCore Runtime: an
echo agent with no model behind it. That is deliberate. Separating the
hosting from the AI lets you verify the deployment pipeline, invocation path,
and permissions before any model is involved. If something fails here, you
know it is infrastructure, not the agent logic.

## 1. Look at the code

Open [`src/agent.py`](../src/agent.py):

```python
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    user_message = payload.get("prompt", "")
    # Here you call your model or agent framework (Strands, LangGraph, and friends).
    reply = f"You said: {user_message}"
    return {"reply": reply}

if __name__ == "__main__":
    app.run()
```

The `@app.entrypoint` decorator marks the function that AgentCore Runtime
calls on every invocation. The payload is the JSON body the caller sends;
whatever the function returns is the response.

## 2. Configure

From the repo root, with your virtual environment active:

```bash
cd src
agentcore configure --entrypoint agent.py --name supportagent --disable-memory
```

The toolkit will prompt you interactively. Accept the defaults:

- **Execution Role**: press Enter to auto-create one
- **ECR Repository**: press Enter to auto-create
- **Requirements file**: confirm the detected `requirements.txt`
- **OAuth authorizer**: answer `no` (this lab uses IAM authorization)

We pass `--disable-memory` because this lab focuses on Runtime only.
AgentCore Memory is a separate service you can add later.

Configuration is saved in a hidden file, `.bedrock_agentcore.yaml`.

## 3. Launch

```bash
agentcore launch
```

The toolkit packages your code, creates the execution role and repository if
needed, and deploys the agent. When it finishes, note two things from the
output:

- The **agent ARN**. You need it in Lab 3.
- The **CloudWatch log locations**.

You now have a live, serverless agent endpoint. You did not create a server,
and you will never patch one. Runtime scales sessions up and down on its own.

Tip: to test on your own machine before deploying, `agentcore launch -l` runs
the agent locally (this mode does require Docker).

## 4. Invoke

```bash
agentcore invoke '{"prompt": "Where is my order?"}'
```

The response:

```
You said: Where is my order?
```

## 5. Why an echo is the right first result

The agent only repeated the input because the code contains no model call
yet; the comment marks where one goes. What matters is what happened
underneath:

- Your request was authorized with your IAM credentials (SigV4).
- Runtime opened an isolated session: a dedicated microVM with its own CPU,
  memory, and filesystem, used by this session alone.
- Your entrypoint ran inside it and answered.
- When the session ends, Runtime destroys the microVM and sanitizes its
  memory. Nothing leaks between sessions.

The deployment pipeline, the invocation path, and the isolation model are all
now proven. Adding intelligence is a code change, not an infrastructure
change.

## 6. Check the status

```bash
agentcore status
```

This shows the agent, its endpoint, and the exact CloudWatch log commands you
can copy to tail the logs.

Next: [`02-add-a-model.md`](02-add-a-model.md).
