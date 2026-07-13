"""Lab 1: a minimal echo agent. Establishes the deployment before adding a model."""

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
