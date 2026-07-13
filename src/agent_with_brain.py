"""Lab 2: the same entrypoint, now calling a Bedrock model via Strands Agents."""

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
