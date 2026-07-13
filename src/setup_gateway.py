"""Lab 5: create an AgentCore Gateway with a demo Lambda target.

Uses the starter toolkit's GatewayClient. With target_payload=None, the
toolkit creates a demo Lambda for you exposing two tools: get_weather and
get_time. Configuration is saved to gateway_config.json for the agent script
and for cleanup.
"""

import json

from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient

REGION = "us-west-2"  # change if you deployed elsewhere

client = GatewayClient(region_name=REGION)

print("Step 1: Creating an OAuth authorization server (Amazon Cognito)...")
cognito = client.create_oauth_authorizer_with_cognito("agentcore-lab-gateway")

print("Step 2: Creating the Gateway (an MCP server endpoint)...")
gateway = client.create_mcp_gateway(authorizer_config=cognito["authorizer_config"])

print("Step 3: Adding a Lambda target (demo Lambda created for you)...")
client.create_mcp_gateway_target(gateway=gateway, target_type="lambda")

config = {
    "region": REGION,
    "gateway_id": gateway["gatewayId"],
    "gateway_url": gateway["gatewayUrl"],
    "client_info": cognito["client_info"],
}
with open("gateway_config.json", "w") as f:
    json.dump(config, f, indent=2, default=str)

print("\nGateway ready.")
print(f"  MCP endpoint: {gateway['gatewayUrl']}")
print("  Config saved to gateway_config.json")
