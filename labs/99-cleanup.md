# Lab 99: Cleanup

Remove everything the labs created, in this order.

## 1. The agent (Labs 1-3, 6, 7)

From the `src` directory:

```bash
agentcore destroy
```

This removes the AgentCore Runtime agent and endpoint, the ECR repository
and images (if container deployment was used), the auto-created IAM
execution role, and optionally the CloudWatch log groups.

## 2. The Gateway (Lab 5)

```bash
python cleanup_gateway.py
```

This removes the Gateway, the demo Lambda target, and the Cognito authorizer
the Gateway setup created.

## 3. The Memory store (Lab 4)

Using the memory ID the demo printed:

```python
from bedrock_agentcore.memory import MemoryClient
MemoryClient(region_name="us-west-2").delete_memory("YOUR_MEMORY_ID")
```

## 4. The Cognito user pool (Lab 6)

```bash
aws cognito-idp delete-user-pool --user-pool-id YOUR_POOL_ID
```

## 5. Verify

```bash
agentcore status
```

Notes: Bedrock model access itself costs nothing; only invocations do. If
you raised the X-Ray trace indexing percentage in Lab 7, set it back to the
default in CloudWatch Transaction Search settings.
