import os
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

conn_target = os.getenv("PROJECT_CONNECTION_STRING")
deployment_name = os.getenv("DEPLOYMENT_NAME", "gpt-5-mini")

print("[*] Testing connection with AzureCliCredential...")
print(f"[*] Target Endpoint: {conn_target}")
print(f"[*] Target Deployment: {deployment_name}")

if not conn_target:
    print("\n[!] ERROR: PROJECT_CONNECTION_STRING is missing in .env")
    exit(1)

try:
    credential = AzureCliCredential()
    
    client = AIProjectClient(
        endpoint=conn_target,
        credential=credential
    )
    print("[+] Successfully initialized AIProjectClient.")

    print(f"[*] Invoking model deployment '{deployment_name}' via Foundry...")
    with client.get_openai_client() as openai_client:
        response = openai_client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a connectivity test assistant."},
                {"role": "user", "content": "Respond with 'PONG' and nothing else."}
            ]
        )
        reply = response.choices[0].message.content.strip()
        print(f"[+] Foundry Model Response: {reply}")

    print("\n[+] Success! Your Azure AI Foundry endpoint, model, and CLI credentials are fully operational.")

except Exception as e:
    print(f"\n[-] Connection Test Failed: {type(e).__name__}")
    print(f"Details: {e}")
