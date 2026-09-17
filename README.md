# SovereignGate

> **Confidential Multi-Agent AI Gateway & Policy Orchestrator for Regulated Enterprise Workflows**  
> *Built natively on Azure AI Foundry for the Microsoft Agentathon (Track 3: Architect)*

[![Azure AI Foundry](https://img.shields.io/badge/Azure%20AI-Foundry-0078D4?logo=microsoftazure&logoColor=white)](https://ai.azure.com/)
[![Runtime](https://img.shields.io/badge/Orchestrator-Python%203.11%20%7C%20FastAPI%20%7C%20Streamlit-3776AB?logo=python&logoColor=white)](https://python.org)
[![Governance](https://img.shields.io/badge/Compliance-UK%20DPA%202018%20%7C%20EU%20GDPR-107C41)](https://ico.org.uk)
[![Zero Retention](https://img.shields.io/badge/Data%20Posture-Zero%20Data%20Retention-blueviolet)]()

---

## Executive Summary

Enterprise adoption of frontier language models faces a structural dilemma: **productivity requires context, but compliance forbids exposure.**

In contract lifecycle management (CLM) and regulated SME operations, business users frequently expose high-value proprietary terms, pricing tiers, party identities, and employee PII to external models via unmonitored browser sessions. Legacy Data Loss Prevention (DLP) tools react by bluntly severing network access, paralyzing employee efficiency and driving shadow AI into unmanaged channels.

**SovereignGate resolves this dilemma.**

Instead of blocking access, SovereignGate acts as an autonomous privacy proxy and policy orchestrator. It intercepts unstructured enterprise prompts, strips confidential business intelligence into deterministic synthetic placeholders in ephemeral volatile memory, enforces strict regional data residency routing on **Azure AI Foundry**, and re-inflates the response in flight.

The external frontier model reasons across full semantic depth without ever seeing, retaining, or training on proprietary enterprise assets.

---

## Architecture: The 3-Agent Ephemeral Pipeline

SovereignGate implements a decoupled, zero-retention agentic pipeline orchestrated via the Azure AI Foundry SDK:
[ Inbound Prompt / Raw CLM Contract Text ]
                                  │
                                  ▼
    ┌───────────────────────────────────────────────────────────┐
    │  Agent 1: Compliance Sentinel (Local Policy & Redaction)  │
    │  • Inspects entities: Counterparties, Values, PII, Terms  │
    │  • Extracts to Ephemeral Session Vault (Volatile RAM)     │
    │  • Classifies Residency Tier (e.g., UK_ONLY / EU_ONLY)    │
    └─────────────────────────────┬─────────────────────────────┘
                                  │ Sanitized Payload ({{ORG_1}}, {{MONEY_1}})
                                  ▼
    ┌───────────────────────────────────────────────────────────┐
    │  Agent 2: Sovereign Dispatcher (Azure AI Foundry Router)  │
    │  • Evaluates statutory jurisdiction vs. model catalog     │
    │  • Dispatches exclusively to compliant regional node      │
    │  • Model reasons purely over abstract synthetic tokens    │
    └─────────────────────────────┬─────────────────────────────┘
                                  │ Raw Inference Output
                                  ▼
    ┌───────────────────────────────────────────────────────────┐
    │  Agent 3: Reconstructor & Audit Synthesizer               │
    │  • Cryptographic re-inflation of original identities      │
    │  • Zero residual memory leak verification                 │
    │  • Emits structured compliance telemetry to ledger        │
    └─────────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼
                [ Clean, Governed Output to End User ]
### Agent Roles & Operational Boundaries

1. **Compliance Sentinel (`ComplianceSentinel`)**
   * Operates entirely on the local ingress boundary.
   * Replaces identifying strings with structured placeholders (`{{ORG_1}}`, `{{MONEY_1}}`, `{{EMAIL_1}}`).
   * Evaluates governing jurisdiction triggers (e.g., UK GDPR, London arbitration, Data Protection Act 2018) to assign sovereign residency constraints.

2. **Sovereign Dispatcher (`SovereignDispatcher`)**
   * Acts as the trusted execution bridge to Azure AI Foundry.
   * Routes prompts according to residency rules (e.g., locking UK_ONLY payloads to UK South deployments like `gpt-5-mini`).
   * Enforces zero-data-retention guarantees, preventing provider training loop contamination.

3. **Reconstructor & Audit Synthesizer (`ReconstructorAudit`)**
   * Reconstructs the final user deliverable by de-tokenizing the response using the ephemeral session vault.
   * Emits an auditable compliance record containing redaction count, residency policy enforced, target deployment used, and approval status.
   * Flushes volatile session keys from memory immediately upon delivery.

---

## Live Demonstration

The repository includes a split-screen Streamlit workspace demonstrating real-time ingestion, isolation, and reconstruction:

```bash
# Launch the live verification dashboard
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

