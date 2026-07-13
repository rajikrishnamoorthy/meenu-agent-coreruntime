"""Lab 5: connect an agent to the Gateway over MCP and use its tools.

Run after setup_gateway.py: python gateway_agent.py
"""

import json

from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient

with open("gateway_config.json") as f:
    config = json.load(f)

gc = GatewayClient(region_name=config["region"])
print("Fetching an OAuth access token from Cognito...")
token = gc.get_access_token_for_cognito(config["client_info"])

mcp = MCPClient(
    lambda: streamablehttp_client(
        config["gateway_url"],
        headers={"Authorization": f"Bearer {token}"},
    )
)

with mcp:
    tools = mcp.list_tools_sync()
    print(f"Tools discovered through the Gateway: {[t.tool_name for t in tools]}")
    agent = Agent(tools=tools)
    agent("What is the weather in Seattle right now?")
