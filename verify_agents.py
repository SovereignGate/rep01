import os
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

client = AIProjectClient(
    endpoint=os.getenv("PROJECT_CONNECTION_STRING"),
    credential=AzureCliCredential()
)

print("=== REGISTERED AZURE AI FOUNDRY AGENTS ===")
agents_list = client.agents.list_agents()

found_agents = {}
for agent in agents_list.data:
    print(f"- Name: {agent.name:<30} | ID: {agent.id} | Model: {agent.model}")
    found_agents[agent.name] = agent.id

if "SovereignGate-Dispatcher" in found_agents:
    agent_id = found_agents["SovereignGate-Dispatcher"]
    print(f"\n[*] Testing execution on '{agent_id}'...")

    # Create session thread
    thread = client.agents.create_thread()
    client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Review payment terms: {{ORG_1}} shall remit {{MONEY_1}}."
    )

    # Process run
    run = client.agents.create_and_process_run(
        thread_id=thread.id,
        assistant_id=agent_id
    )
    print(f"[+] Run completed with status: {run.status}")

    messages = client.agents.list_messages(thread_id=thread.id)
    print(f"[+] Agent Output:\n{messages['data'][0]['content'][0]['text']['value']}")
else:
    print("\n[!] No SovereignGate agents found. Please run register_foundry_agents.py first.")
