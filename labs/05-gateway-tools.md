# Lab 5: Tools with AgentCore Gateway

The agent can think but cannot act on external systems. AgentCore Gateway
turns existing backends (Lambda functions, OpenAPI or Smithy APIs) into
tools an agent can call, exposed through a single managed **MCP** (Model
Context Protocol) endpoint. You describe the backend; you do not rewrite it.

Gateway secures both directions. Inbound, it is an OAuth resource server:
callers must present a valid bearer token from an identity provider such as
Amazon Cognito. Outbound, for Lambda targets, it uses an IAM role to invoke
the function.

## 1. Create the Gateway and a Lambda target

Open [`src/setup_gateway.py`](../src/setup_gateway.py) and read it. It does
three things with the toolkit's `GatewayClient`:

1. Creates a Cognito-backed OAuth authorization server for inbound auth
2. Creates the Gateway (a managed MCP endpoint)
3. Adds a Lambda target. Passing no payload tells the toolkit to create a
   demo Lambda for you, exposing two tools: `get_weather` and `get_time`

```bash
cd src
python setup_gateway.py
```

This takes 2-3 minutes and writes `gateway_config.json` with the gateway URL
and client credentials. In real projects you would pass your own Lambda ARN
and a tool schema instead of the demo, for example:

```json
{
  "lambdaArn": "arn:aws:lambda:us-west-2:123456789012:function:GetOrderStatus",
  "toolSchema": {
    "inlinePayload": [
      {
        "name": "get_order_status",
        "description": "Look up the shipping status of an order",
        "inputSchema": {
          "type": "object",
          "properties": {"order_id": {"type": "string"}},
          "required": ["order_id"]
        }
      }
    ]
  }
}
```

## 2. Connect an agent to the Gateway

Open [`src/gateway_agent.py`](../src/gateway_agent.py). It fetches an OAuth
access token from Cognito, opens an MCP client against the gateway URL with
the token in the `Authorization` header, lists the tools it finds, and hands
them to a Strands agent.

```bash
python gateway_agent.py
```

Ask about the weather and watch the agent choose `get_weather` on its own,
call it through the Gateway, and answer from the result. The agent never saw
the Lambda; it saw a named tool with a description and a schema.

## 3. Verify from the outside

You can talk to the Gateway directly, since MCP is just JSON-RPC over HTTP:

```bash
curl -X POST YOUR_GATEWAY_URL \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

And tail its logs:

```bash
aws logs tail /aws/bedrock-agentcore/gateways/YOUR_GATEWAY_ID --follow
```

Try the curl without the Authorization header. The Gateway refuses: inbound
OAuth is not optional.

Next: [`06-identity-cognito-auth.md`](06-identity-cognito-auth.md).
