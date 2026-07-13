# Lab 0: Setup

Environment preparation takes about ten minutes.

## 1. AWS account and credentials

You need an AWS account and working credentials on your machine. Install the
AWS CLI version 2 if you have not, then run:

```bash
aws configure
```

Verify your identity:

```bash
aws sts get-caller-identity
```

If this prints your account ID, you are signed in.

## 2. IAM permissions

If you are an administrator in your account, skip to step 3.

Otherwise, your IAM identity needs two things attached:

- The `AmazonBedrockAgentCoreFullAccess` managed policy
- The starter toolkit caller policy, documented at
  [Use the starter toolkit](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-starter-toolkit.html)

## 3. Enable model access in Bedrock

Lab 2 calls a Claude model through Amazon Bedrock. In the AWS console:

1. Open the **Amazon Bedrock** console in your working Region. The toolkit
   defaults to `us-west-2`, so use that unless you know you want another.
2. Go to **Model access** and enable **Anthropic Claude** (Claude Sonnet 4.0
   or the closest available version).

If you skip this, Lab 1 still works (the echo agent calls no model), but
Lab 2 will fail with a model access error.

## 4. Python environment

You need Python 3.10 or later. Create a virtual environment and install the
dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The requirements file installs:

- `bedrock-agentcore` (the SDK: `BedrockAgentCoreApp` and the entrypoint)
- `bedrock-agentcore-starter-toolkit` (the `agentcore` CLI commands)
- `strands-agents` (the agent framework used in Lab 2)
- `boto3` (used in Lab 3)

Verify the CLI is on your path:

```bash
agentcore --help
```

## 5. Docker? Not needed.

The default deployment mode packages your code and deploys it directly, or
builds containers in the cloud with AWS CodeBuild. You only need Docker if you
later want the `--local` or `--local-build` flags. If the toolkit prints a
"Docker not found" warning, ignore it.

You are ready. Open [`01-deploy-a-minimal-agent.md`](01-deploy-a-minimal-agent.md).
