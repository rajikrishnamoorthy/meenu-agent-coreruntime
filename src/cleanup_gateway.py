"""Lab 99: remove the Gateway, its demo Lambda, and the Cognito authorizer."""

import json

from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient

with open("gateway_config.json") as f:
    config = json.load(f)

client = GatewayClient(region_name=config["region"])
client.cleanup_gateway(config["gateway_id"], config["client_info"])
print("Gateway cleanup complete.")
