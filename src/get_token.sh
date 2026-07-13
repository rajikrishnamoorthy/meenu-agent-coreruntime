#!/bin/bash
# Lab 6: fetch a bearer (access) token for the test user.
# Usage: ./get_token.sh <CLIENT_ID>
set -e
CLIENT_ID=$1
aws cognito-idp initiate-auth \
  --client-id "$CLIENT_ID" \
  --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME=testuser,PASSWORD='LabPassword123!' \
  --query 'AuthenticationResult.AccessToken' --output text
