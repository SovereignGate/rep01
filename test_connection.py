import os
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

conn_target = os.getenv("PROJECT_CONNECTION_STRING")
deployment_name = os.getenv("DEPLOYMENT_NAME", "gpt-4o-uksouth")

print("[*] Testing connection with AzureCliCredential...")
print(f"[*] Target Endpoint/ConnStr: {conn_target}")
print(f"[*] Target Deployment: {deployment_name}")

if not conn_target:
    print("\n[!] ERROR: PROJECT_CONNECTION_STRING is missing in .env")
    exit(1)

try:
    credential = AzureCliCredential()
    
    # Direct endpoint initialization vs connection string
    if conn_target.startswith("https://"):
        client = AIProjectClient(
            endpoint=conn_target,
            credential=credential
        )
    else:
        client = AIProjectClient.from_connection_string(
            conn_str=conn_target,
            credential=credential
        )
        
    print("[+] Successfully initialized AIProjectClient.")

    print(f"[*] Testing agent creation on deployment '{deployment_name}'...")
    test_agent = client.agents.create_agent(
        model=deployment_name,
        name="sovereign-conn-test",
        instructions="Respond with 'PONG' and nothing else."
    )
    print(f"[+] Agent created successfully with ID: {test_agent.id}")

    thread = client.agents.create_thread()
    client.agents.create_message(thread_id=thread.id, role="user", content="PING")
    run = client.agents.create_and_process_run(thread_id=thread.id, assistant_id=test_agent.id)
    
    messages = client.agents.list_messages(thread_id=thread.id)
    response = messages["data"][0]["content"][0]["text"]["value"]
    print(f"[+] Foundry Agent Response: {response.strip()}")

    # Cleanup test agent
    client.agents.delete_agent(test_agent.id)
    print("[+] Ephemeral agent deleted. Foundry connection is 100% operational!")

except Exception as e:
    print(f"\n[-] Connection Test Failed: {type(e).__name__}")
    print(f"Details: {e}")
