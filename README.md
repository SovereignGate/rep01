# SovereignGate

> **Confidential Multi-Agent AI Gateway and Policy Orchestrator for Regulated Enterprise Workflows**  
> *Built natively on Azure AI Foundry for the Microsoft Agentathon (Track 3: Architect)*

[![Azure AI Foundry](https://img.shields.io/badge/Azure%20AI-Foundry-0078D4?logo=microsoftazure&logoColor=white)](https://ai.azure.com/)
[![Runtime](https://img.shields.io/badge/Orchestrator-Python%203.11%20%7C%20Streamlit-3776AB?logo=python&logoColor=white)](https://python.org)
[![Governance](https://img.shields.io/badge/Compliance-UK%20DPA%202018%20%7C%20EU%20GDPR-107C41)](https://ico.org.uk)
[![Data Posture](https://img.shields.io/badge/Data%20Posture-Zero%20Data%20Retention-blueviolet)]()

---

## Executive Summary

Enterprise adoption of frontier language models faces a structural dilemma: **productivity requires context, but compliance forbids exposure.**

In contract lifecycle management (CLM) and regulated SME operations, business users frequently expose high-value proprietary terms, pricing tiers, party identities, and employee PII to external models via unmonitored browser sessions. Legacy Data Loss Prevention (DLP) tools react by bluntly severing network access, paralyzing employee efficiency and driving shadow AI into unmanaged channels.

**SovereignGate resolves this dilemma.**

Instead of blocking access, SovereignGate acts as an autonomous privacy proxy and policy orchestrator. It intercepts unstructured enterprise prompts, strips confidential business intelligence into deterministic synthetic placeholders in ephemeral volatile memory, enforces strict regional data residency routing on **Azure AI Foundry**, and re-inflates the response in flight.

The external frontier model reasons across full semantic depth without ever seeing, retaining, or training on proprietary enterprise assets.

---

## Architecture: The 3-Agent Ephemeral Pipeline


The end-to-end lifecycle processes contract clauses across three stateless agents:

- **Ingress (Agent 1: Compliance Sentinel):** Inspects raw text, redacts sensitive entities into synthetic tags (e.g., {{ORG_1}}, {{MONEY_1}}), stores real values in an ephemeral session vault, and classifies regional residency tiers.
- **Inference (Agent 2: Sovereign Dispatcher):** Selects a compliant Azure AI Foundry deployment (e.g., UK South) and executes the prompt over abstract synthetic tokens.
- **Egress (Agent 3: Reconstructor & Audit):** Replaces synthetic tags with original identities and writes a compliance ledger event.

### Agent Roles & Operational Boundaries

1. **Compliance Sentinel (ComplianceSentinel)**
   - Operates entirely on the local ingress boundary.
   - Replaces identifying strings with structured placeholders ({{ORG_1}}, {{MONEY_1}}, {{EMAIL_1}}).
   - Evaluates governing jurisdiction triggers (such as UK GDPR, London arbitration, Data Protection Act 2018) to assign sovereign residency constraints.

2. **Sovereign Dispatcher (SovereignDispatcher)**
   - Acts as the trusted execution bridge to Azure AI Foundry.
   - Routes prompts according to residency rules (locking UK_ONLY payloads to UK South deployments such as gpt-5-mini).
   - Enforces zero-data-retention guarantees, preventing provider training loop contamination.

3. **Reconstructor & Audit Synthesizer (ReconstructorAudit)**
   - Reconstructs the final user deliverable by de-tokenizing the response using the ephemeral session vault.
   - Emits an auditable compliance record containing redaction count, residency policy enforced, target deployment used, and approval status.
   - Flushes volatile session keys from memory immediately upon delivery.

---

## Live Demonstration

The repository includes a split-screen Streamlit application demonstrating real-time ingestion, isolation, and reconstruction.

Launch Command:

    streamlit run app.py --server.port 8501 --server.address 0.0.0.0

- **Left Column:** Live inspection of the sanitized payload leaving the enterprise perimeter alongside the active Ephemeral Vault.
- **Right Column:** Direct comparison of raw model inference (reasoning over synthetic tags) against the fully restored client deliverable and compliance audit record.

---

## Why SovereignGate Stands Out

| Evaluation Criteria | Prototype Reality | Enterprise Strategic Value |
| :--- | :--- | :--- |
| **Innovation** | Autonomous proxying over blunt network blocking. | Replaces static DLP regular expressions with multi-agent policy negotiation and dynamic token re-inflation. |
| **Usability** | Transparent to the end user. | Zero prompt-engineering overhead for employees; standard input yields standard output with automated boundary defense. |
| **Impact** | Measurable regulatory risk mitigation. | Neutralizes GDPR/UK DPA non-compliance exposure and guarantees zero enterprise IP leakage. |
| **Foundry Native** | Deep Azure AI architecture alignment. | Directly leverages Azure AI Projects, Azure CLI credential delegation, and sovereign regional model endpoints. |

---

## Quickstart & Verification in GitHub Codespaces

Follow these steps to run and test the complete pipeline from scratch.

### 1. Prerequisites
- An active Azure Subscription with an Azure AI Foundry project.
- Azure CLI authenticated via:

    az login --use-device-code

### 2. Environment Configuration
Create a  file in the root directory:

    PROJECT_CONNECTION_STRING="https://<your-resource-name>[.services.ai.azure.com/api/projects/](https://.services.ai.azure.com/api/projects/)<your-project-name>"
    DEPLOYMENT_NAME="gpt-5-mini"

### 3. Dependency Installation
Set up a Python virtual environment and install dependencies:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

### 4. Automated Headless Verification
Run the verification test suite to ensure all three agents execute their tasks and pass data cleanly:

    python test_ephemeral_agents.py

### 5. Launch the Web Interface
Start the interactive demo UI:

    streamlit run app.py --server.port 8501 --server.address 0.0.0.0

Open port 8501 in your browser and click **Run Governed Pipeline** to inspect the live token redaction, model reasoning, and reconstruction side by side.

### 6. Pitch Deck Generation
Generate the pitch presentation materials directly inside Codespaces:

    python generate_decks.py

Outputs:  and .

---

## Strategic Roadmap

For a breakdown of the production modernization path (including Microsoft Presidio integration, Azure AI Search policy grounding, and automated Azure AI Evaluation benchmarking), see [NextStep.md](./NextStep.md).
