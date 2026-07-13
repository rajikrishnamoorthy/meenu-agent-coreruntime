# Lab 6: Inbound Auth with Cognito JWT Tokens

So far you have invoked the agent with IAM (SigV4) credentials: fine for AWS
principals, wrong for human end users. AgentCore Runtime also supports
**JWT bearer token** inbound authorization: users sign in with an identity
provider such as Amazon Cognito, receive a token, and present it with each
request. Runtime validates the token against the provider's OpenID discovery
document and only admits requests whose token matches the allowed client.

In this lab you stand up a Cognito user pool, reconfigure the agent to
require JWT auth, invoke with a token, and then prove the negative case:
no token, no entry.

## 1. Create the user pool and a test user

```bash
cd src
./setup_cognito.sh
```

The script creates a user pool, an app client (no secret, password auth
enabled), and a test user (`testuser` / `LabPassword123!`). It prints three
values; save them:

- User pool ID
- Client ID
- Discovery URL (the pool's `/.well-known/openid-configuration` address)

## 2. Reconfigure the agent to require JWT

```bash
agentcore configure --entrypoint agent_with_brain.py --name supportagent --disable-memory
```

This time, when prompted **"Configure OAuth authorizer?"**, answer **yes**,
and supply the discovery URL and the client ID from step 1. Then redeploy:

```bash
agentcore launch
```

The Runtime endpoint now rejects plain IAM invocations and expects a bearer
token vouched for by your Cognito pool.

## 3. Get a token and invoke

```bash
TOKEN=$(./get_token.sh <CLIENT_ID>)
agentcore invoke '{"prompt": "Hello, who are you?"}' --bearer-token "$TOKEN"
```

The token is a JWT: three base64 sections carrying claims such as the client
ID and expiry. Runtime read those claims, checked them against the allowed
client you configured, and admitted the request. Paste the token into a JWT
inspector (or decode the middle section with base64) to see the claims
yourself.

If your toolkit version names the flag differently, check
`agentcore invoke --help`.

## 4. The test everyone forgets

Invoke the same prompt with no token:

```bash
agentcore invoke '{"prompt": "Hello, who are you?"}'
```

Expect a rejection (an authorization error / HTTP 403). This is the check
that separates a demo from a production posture: proving that unauthorized
callers are refused, not just that authorized ones succeed.

## Restore IAM auth for the remaining labs

Lab 3's boto3 script uses IAM auth. If you want to rerun it, reconfigure
once more and answer **no** to the OAuth authorizer prompt, then
`agentcore launch`.

Next: [`07-observability.md`](07-observability.md).
