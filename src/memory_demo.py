"""Lab 4: AgentCore Memory. Create a store, record a conversation, retrieve
a long-term memory.

Shape only: confirm field names against the current bedrock-agentcore SDK.
Long-term extraction is asynchronous; allow a couple of minutes.
"""

import time

from bedrock_agentcore.memory import MemoryClient

REGION = "us-west-2"  # change if you deployed elsewhere

client = MemoryClient(region_name=REGION)

print("Creating memory store (this can take 2-5 minutes for long-term)...")
memory = client.create_memory_and_wait(
    name="LabAgentMemory",
    strategies=[
        {
            "userPreferenceMemoryStrategy": {
                "name": "preferences",
                "namespaces": ["/users/{actorId}"],
            }
        }
    ],
)
memory_id = memory["id"]
print(f"Memory store ready: {memory_id}")

print("Recording a conversation as short-term events...")
client.create_event(
    memory_id=memory_id,
    actor_id="customer-001",
    session_id="session-001",
    messages=[
        ("Please send all my order updates by email, never by phone.", "USER"),
        ("Understood. I will send updates by email only.", "ASSISTANT"),
    ],
)

print("Waiting for asynchronous long-term extraction (~2 minutes)...")
time.sleep(120)

print("Retrieving long-term memories for this customer...")
memories = client.retrieve_memories(
    memory_id=memory_id,
    namespace="/users/customer-001",
    query="How does this customer prefer to be contacted?",
)
for m in memories:
    print(m)

print(f"\nDone. To delete the store later: MemoryClient.delete_memory('{memory_id}')")
