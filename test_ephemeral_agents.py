import os
import sys
import json
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

# Import your agent definitions from main.py
from main import ComplianceSentinel, SovereignDispatcher, ReconstructorAudit

load_dotenv()

def verify_pipeline():
    print("=== STARTING EPHEMERAL AGENT VERIFICATION ===")
    
    # 1. Verify Agent 1: Compliance Sentinel (Local Policy & Redaction)
    print("\n[Step 1] Starting Compliance Sentinel...")
    sentinel = ComplianceSentinel()
    
    test_clause = "Northwind Traders agrees to wire £120,000 to legal@northwind.com under London jurisdiction."
    sanitized_text, vault, tier = sentinel.sanitize(test_clause)
    
    # Assertions for Sentinel
    assert "{{ORG_1}}" in sanitized_text, "Failed: Organization not redacted."
    assert "{{MONEY_2}}" in sanitized_text or "{{MONEY_1}}" in sanitized_text, "Failed: Currency not redacted."
    assert "{{EMAIL_3}}" in sanitized_text or "{{EMAIL_2}}" in sanitized_text or "{{EMAIL_1}}" in sanitized_text, "Failed: Email not redacted."
    assert tier == "UK_ONLY", f"Failed: Expected UK_ONLY tier, got {tier}"
    assert len(vault) >= 3, "Failed: Vault did not capture all tokens."
    
    print("  ✓ Sentinel started and executed successfully.")
    print(f"  ✓ Sanitized Payload: {sanitized_text}")
    print(f"  ✓ Ephemeral Vault: {vault}")
    print(f"  ✓ Policy Tier: {tier}")

    # 2. Verify Agent 2: Sovereign Dispatcher (Model Execution on Foundry)
    print("\n[Step 2] Starting Sovereign Dispatcher (connecting to Azure AI Foundry)...")
    credential = AzureCliCredential()
    client = AIProjectClient(
        endpoint=os.getenv("PROJECT_CONNECTION_STRING"),
        credential=credential
    )
    dispatcher = SovereignDispatcher(client)
    
    raw_response = dispatcher.dispatch(
        sanitized_text=sanitized_text,
        tier=tier,
        instruction="State the party and the sum involved using the provided tokens."
    )
    
    # Assertions for Dispatcher
    assert len(raw_response) > 0, "Failed: Model returned empty response."
    print("  ✓ Dispatcher executed call via Azure AI Foundry.")
    print(f"  ✓ Raw Model Output: {raw_response.strip()}")

    # 3. Verify Agent 3: Reconstructor & Audit
    print("\n[Step 3] Starting Reconstructor & Audit Synthesizer...")
    reconstructor = ReconstructorAudit()
    final_pack = reconstructor.restore_and_log(raw_response, vault, tier)
    
    restored_text = final_pack["result"]
    audit = final_pack["audit"]
    
    # Assertions for Reconstructor
    assert "Northwind Traders" in restored_text, "Failed: Entity was not de-tokenized."
    assert "£120,000" in restored_text, "Failed: Amount was not de-tokenized."
    assert audit["status"] == "APPROVED", "Failed: Audit event missing approval."
    assert audit["tokens_redacted"] == len(vault), "Failed: Redaction count mismatch."
    
    print("  ✓ Reconstructor restored original values.")
    print("  ✓ Audit event created.")
    print(f"\nFinal Restored Output:\n{restored_text}")
    print(f"\nAudit Event:\n{json.dumps(audit, indent=2)}")

    print("\n=== ALL EPHEMERAL AGENTS VERIFIED: 100% OPERATIONAL ===")

if __name__ == "__main__":
    try:
        verify_pipeline()
    except Exception as e:
        print(f"\n[-] Verification failed: {e}")
        sys.exit(1)
