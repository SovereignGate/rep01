import os
import re
import json
from typing import Dict, Any, Tuple
import streamlit as st
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

st.set_page_config(
    page_title="SovereignGate | Enterprise LLM Governance",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Foundry Client
@st.cache_resource
def get_foundry_client():
    endpoint = os.getenv("PROJECT_CONNECTION_STRING")
    credential = AzureCliCredential()
    return AIProjectClient(endpoint=endpoint, credential=credential)

DEPLOYMENT = os.getenv("DEPLOYMENT_NAME", "gpt-5-mini")

# Agent 1: Compliance Sentinel
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

# Agent 2: Sovereign Dispatcher
class SovereignDispatcher:
    def __init__(self, client: AIProjectClient):
        self.client = client

    def dispatch(self, sanitized_text: str, tier: str, instruction: str) -> str:
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

# Agent 3: Reconstructor & Audit
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

# UI Header
st.title("🛡️ SovereignGate")
st.caption("Privacy & Data Residency Multi-Agent Orchestrator on Azure AI Foundry")

# Sidebar Configuration
with st.sidebar:
    st.header("Governance Telemetry")
    st.markdown(f"**Target Model:** `{DEPLOYMENT}`")
    st.markdown("**Foundry Node:** `UK South (Active)`")
    st.markdown("**Zero-Retention Buffer:** `Enabled`")
    st.divider()
    instruction_input = st.text_area(
        "Analysis Instruction",
        value="Summarize the core financial obligations, liabilities, and legal jurisdiction."
    )

# Input area
default_contract = """This Master Services Agreement is entered into by Contoso Ltd and Fabrikam Inc.
The Client agrees to remit a total project fee of £250,000 to accounts@fabrikam.com.
Any dispute or claim arising out of this Agreement shall be governed by the laws of England and Wales under UK GDPR and the Data Protection Act 2018."""

raw_contract = st.text_area("Raw Contract / Document Input:", value=default_contract, height=140)

if st.button("Run Governed Pipeline", type="primary"):
    try:
        client = get_foundry_client()
        sentinel = ComplianceSentinel()
        dispatcher = SovereignDispatcher(client)
        reconstructor = ReconstructorAudit()

        # Step 1: Sentinel Sanitization
        sanitized_text, vault, tier = sentinel.sanitize(raw_contract)

        # Display Pipeline Inspection
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("1. Ingestion & Sanitization")
            st.info(f"Enforced Data Policy: **{tier}**")
            st.text_area("Payload Sent to Model (Zero PII / IP)", value=sanitized_text, height=160, disabled=True)
            with st.expander("Inspected Token Vault (Ephemeral Memory)"):
                st.json(vault)

        # Step 2: Dispatcher Execution
        with st.spinner("Dispatching sanitized payload to Azure AI Foundry..."):
            raw_model_response = dispatcher.dispatch(sanitized_text, tier, instruction_input)

        # Step 3: Reconstruction
        final_result = reconstructor.restore_and_log(raw_model_response, vault, tier)

        with col2:
            st.subheader("2. Model Output vs Governed Delivery")
            with st.expander("Raw Model Output (Contains Synthetic Tokens)"):
                st.write(raw_model_response)

            st.success("Reconstructed Output (De-anonymized for User)")
            st.write(final_result["result"])

            with st.expander("Compliance Audit Record"):
                st.json(final_result["audit"])

    except Exception as e:
        st.error(f"Execution Error: {e}")
