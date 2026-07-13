# Lab 4: Persistent Memory with AgentCore Memory

The agent from Labs 1-3 starts every conversation from zero. AgentCore
Memory fixes that. It is a managed memory service that lives outside any
single Runtime session, so what it stores survives after the session's
microVM is destroyed.

## Two kinds of memory

**Short-term memory** stores the raw conversation as events: every turn,
written down as it happens, addressed by an `actorId` (who the user is) and a
`sessionId` (which conversation this is). Events persist for a configured
retention period, so an agent can reread recent turns even across a restart.

**Long-term memory** is extracted from those events asynchronously by
built-in strategies. There are four:

| Strategy | What it extracts |
|---|---|
| Semantic | Facts stated in conversation |
| User preference | Preferences, choices, styles |
| Summary | Running summaries of whole conversations |
| Episodic | What happened in an interaction, as a coherent episode |

See [built-in strategies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-configuring-built-in-strategies.html)
in the AWS docs.

## 1. Run the demo

Open [`src/memory_demo.py`](../src/memory_demo.py) and read it first. It
creates a memory store with the user-preference strategy, records a short
conversation ("send my updates by email, never by phone") as events, waits
for the asynchronous extraction, then queries long-term memory with a natural
language question.

```bash
cd src
python memory_demo.py
```

Expect the store creation to take 2-5 minutes and the extraction wait another
2. The final output should include an extracted preference about email
contact. That preference now exists independently of any session and any
agent: a second agent pointed at the same store and namespace would retrieve
the same fact. That is how state is shared across sessions and across agents.

## 2. Alternative: let the toolkit provision memory

The `agentcore configure` command (without the `--disable-memory` flag we
used in Lab 1) prompts you to provision short-term or short-plus-long-term
memory for the agent, and injects the memory ID into the agent's environment
as `BEDROCK_AGENTCORE_MEMORY_ID`. Try it:

```bash
agentcore configure --entrypoint agent_with_brain.py --name supportagent
```

Answer the memory prompts and read what it creates. Note that long-term
memory provisioning can take a few minutes; `agentcore status` shows when it
is active.

## Cleanup reminder

The demo script prints the memory ID at the end. Note it down; Lab 99 deletes
it.

Next: [`05-gateway-tools.md`](05-gateway-tools.md).
