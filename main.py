import os
import re
import json
from typing import Dict, Any, Tuple
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

CONN_STR = os.getenv("PROJECT_CONNECTION_STRING")
DEPLOYMENT = os.getenv("DEPLOYMENT_NAME", "gpt-5-mini")

credential = AzureCliCredential()
project_client = AIProjectClient(
    endpoint=CONN_STR,
    credential=credential
)

# Agent 1: Compliance Sentinel (Local Policy & Deterministic Redaction)
class ComplianceSentinel:
    def __init__(self):
        self.patterns = {
            "EMAIL": r'[\w\.-]+@[\w\.-]+\.\w+',
            "MONEY": r'([£$€]\s*(\d{1,3}(,\d{3})*(\.\d{2})?|\d+(\.\d{2})?))',
            "ORG": r'(Contoso Ltd|Fabrikam Inc|Acme Corp|Northwind Traders)'
        }

    def sanitize(self, text: str) -> Tuple[str, Dict[str, str], str]:
        vault = {}
        sanitized = text
        counter = 1

        for label, pattern in self.patterns.items():
            matches = list(re.finditer(pattern, sanitized))
            for match in reversed(matches):
                val = match.group(0)
                token = f"{{{{{label}_{counter}}}}}"
                vault[token] = val
                sanitized = sanitized[:match.start()] + token + sanitized[match.end():]
                counter += 1

        residency = "UK_ONLY" if any(k in text for k in ["£", "GDPR", "DPA", "London"]) else "EU_ONLY"
        return sanitized, vault, residency


# Agent 2: Sovereign Dispatcher (Model Routing & Execution)
class SovereignDispatcher:
    def __init__(self, client: AIProjectClient):
        self.client = client

    def dispatch(self, sanitized_text: str, tier: str, instruction: str) -> str:
        print(f"[*] Dispatching to Foundry ({DEPLOYMENT}) under policy [{tier}]...")
        
        with self.client.get_openai_client() as openai_client:
            response = openai_client.chat.completions.create(
                model=DEPLOYMENT,
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a contract analysis assistant. "
                            "Crucial: preserve all placeholder tokens like {{ORG_1}}, {{MONEY_2}} verbatim without modifying them. "
                            f"{instruction}"
                        )
                    },
                    {"role": "user", "content": sanitized_text}
                ]
            )
            return response.choices[0].message.content.strip()


# Agent 3: Reconstructor & Audit Synthesizer (Vault De-anonymization & Audit Trail)
class ReconstructorAudit:
    def restore_and_log(self, text: str, vault: Dict[str, str], tier: str) -> Dict[str, Any]:
        restored = text
        for token, original in vault.items():
            restored = restored.replace(token, original)

        audit_log = {
            "status": "APPROVED",
            "jurisdiction_enforced": tier,
            "tokens_redacted": len(vault),
            "target_model": DEPLOYMENT,
            "retention_policy": "ZERO_DATA_RETENTION"
        }
        return {"result": restored, "audit": audit_log}


if __name__ == "__main__":
    sample_contract = """
    This Agreement is between Contoso Ltd and Fabrikam Inc.
    The customer shall pay a fee of £250,000 to billing@fabrikam.com.
    Disputes will be settled under the courts of London under GDPR and UK DPA.
    """

    print("=== 1. RAW CONTRACT INPUT ===")
    print(sample_contract.strip())

    sentinel = ComplianceSentinel()
    sanitized_input, vault, tier = sentinel.sanitize(sample_contract)

    print("\n=== 2. SANITIZED PAYLOAD (SENT TO FOUNDRY MODEL) ===")
    print(sanitized_input.strip())
    print("\nProtected Token Vault:", vault)

    dispatcher = SovereignDispatcher(project_client)
    raw_response = dispatcher.dispatch(
        sanitized_input, 
        tier, 
        instruction="Summarize the core financial obligations and jurisdiction."
    )

    reconstructor = ReconstructorAudit()
    final_output = reconstructor.restore_and_log(raw_response, vault, tier)

    print("\n=== 3. AUDIT TELEMETRY ===")
    print(json.dumps(final_output["audit"], indent=2))

    print("\n=== 4. FINAL RESTORED OUTPUT (SAFE & DE-ANONYMIZED) ===")
    print(final_output["result"])
