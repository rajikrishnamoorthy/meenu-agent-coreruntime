#!/bin/bash
# Lab 6: create a Cognito user pool, app client, and test user for
# JWT (bearer token) inbound authorization on AgentCore Runtime.
set -e

REGION=$(aws configure get region)

POOL_ID=$(aws cognito-idp create-user-pool \
  --pool-name AgentCoreLabPool \
  --policies '{"PasswordPolicy":{"MinimumLength":8}}' \
  --region "$REGION" \
  --query 'UserPool.Id' --output text)

CLIENT_ID=$(aws cognito-idp create-user-pool-client \
  --user-pool-id "$POOL_ID" \
  --client-name AgentCoreLabClient \
  --no-generate-secret \
  --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH \
  --region "$REGION" \
  --query 'UserPoolClient.ClientId' --output text)

aws cognito-idp admin-create-user \
  --user-pool-id "$POOL_ID" \
  --username testuser \
  --temporary-password "TempPass123!" \
  --message-action SUPPRESS \
  --region "$REGION" > /dev/null

aws cognito-idp admin-set-user-password \
  --user-pool-id "$POOL_ID" \
  --username testuser \
  --password "LabPassword123!" \
  --permanent \
  --region "$REGION"

echo "User pool ID : $POOL_ID"
echo "Client ID    : $CLIENT_ID"
echo "Discovery URL: https://cognito-idp.$REGION.amazonaws.com/$POOL_ID/.well-known/openid-configuration"
echo ""
echo "Save these three values. You need the discovery URL and client ID"
echo "when reconfiguring the agent, and the client ID to fetch tokens."
