# Biogen Clinical Intelligence Demo

A Snowflake demo for Biogen's clinical/SAS team, showcasing Snowflake as a clinical AI platform — not just a data warehouse. Deployable to any Snowflake account.

## Session Details

| | |
|---|---|
| **Date** | Wednesday, May 13, 2026 |
| **Audience** | Biogen Clinical Team (SAS experts, new to Snowflake AI) |
| **Snowflake Team** | Bob LeBoeuf (SE), Kelci Miclaus (Life Sciences SME), Ryan Stevens (AE) |

## Repository Contents

| File | Description |
|------|-------------|
| `biogen_snowflake_may13.html` | 17-slide branded HTML presentation (open in browser, arrow keys to navigate) |
| `biogen_demo_script.sql` | 640-line demo script — run top-to-bottom in any Snowflake account |
| `STUDY-2024-001_CSR_Final.pdf` | 13-page mock Clinical Study Report (Phase 2a MS trial, ICH E3 format) |
| `generate_csr.py` | Python script to regenerate/modify the CSR PDF (requires `reportlab`) |

## Deployment

This demo can be deployed to **any Snowflake account** with Cortex AI enabled. Run `biogen_demo_script.sql` in sequence — it creates all objects from scratch.

**Requirements:**
- SYSADMIN role (or equivalent with CREATE DATABASE, CREATE WAREHOUSE)
- Cortex AI functions enabled (AI_COMPLETE, PARSE_DOCUMENT, EMBED_TEXT_768)
- Cortex Search Service available
- Semantic View + Agent support (Snowflake Intelligence)

## Demo Architecture

```
BIOGEN_CLINICAL_DEMO
├── SDTM (Schema)
│   ├── DM                          — Subject Demographics (10 subjects)
│   ├── AE                          — Adverse Events (10 events)
│   ├── LB                          — Lab Results (10 results)
│   ├── DV                          — Protocol Deviations (4 deviations)
│   ├── AE_AI_SUMMARIES             — AI_COMPLETE narrative summaries + classification
│   ├── AE_AI_URGENCY               — AI_COMPLETE urgency scoring
│   ├── DV_AI_CLASSIFICATIONS       — AI_COMPLETE deviation categorization
│   ├── V_CLINICAL_SUMMARY          — Pre-built analytics view
│   ├── CLINICAL_INTELLIGENCE_SV    — Semantic View (5 tables, 8 metrics, 21 dimensions)
│   └── CLINICAL_INTELLIGENCE_AGENT — Snowflake Intelligence Agent
├── DOCS (Schema)
│   ├── CSR_CHUNKS                  — 13 parsed + vectorized CSR pages
│   ├── CLINICAL_DOCS_STAGE         — SSE-encrypted stage with CSR PDF
│   └── CSR_SEARCH                  — Cortex Search Service (managed RAG)
└── CLINICAL_DEMO_WH                — XS warehouse, auto-suspend 60s
```

## Demo Flow (9 Acts)

| Act | Topic | Key Feature |
|-----|-------|-------------|
| 1 | Load SDTM Clinical Data | `COPY INTO`, Snowpipe |
| 2 | GxP Governance | Column masking, row access policies, audit trail |
| 3 | Clinical Analytics | SQL equivalents of PROC FREQ / PROC MEANS |
| 4 | Cortex AI on Narratives | `AI_COMPLETE` for summarization + classification |
| 5 | Cortex Analyst | Semantic model + natural language → SQL |
| 6 | Cortex Search Service | Managed RAG over CSR document |
| 7 | AI_COMPLETE Persisted Results | Pre-computed LLM outputs in tables |
| 8 | Semantic View | Unified semantic layer for Cortex Analyst |
| 9 | Snowflake Intelligence Agent | Combined chatbot: structured data + document search |

## Snowflake Intelligence Agent

The agent is accessible in Snowsight under **Intelligence**. It combines:

- **Cortex Analyst** (via Semantic View) — structured data queries over clinical trial tables
- **Cortex Search** — semantic search over the Clinical Study Report PDF

### Sample Questions

- "Which treatment arm had the most serious adverse events?"
- "What was the primary endpoint result for Drug A 20mg?"
- "Show me all subjects with ALT above 3x ULN"
- "What did the CSR conclude about the benefit-risk profile?"
- "What deviations were classified as dosing errors?"

## Running the Demo

1. Open `biogen_snowflake_may13.html` in a browser for the slide deck
2. Open `biogen_demo_script.sql` in Snowsight (or any SQL editor connected to your account)
3. Run Acts 1–5 in sequence for the core demo
4. Acts 6–9 are pre-built — just run the verification/query statements
5. Open Snowflake Intelligence to demo the agent conversationally

## Key Talking Points for SAS Audience

- Snowflake Notebooks are an alternative to SAS Grid batch jobs — queries can be pushed to Snowflake without forcing a massive change to your workflow
- `AI_COMPLETE` = call LLMs as SQL functions (no API keys, no data leaves Snowflake)
- Semantic View = define your data model once, query in plain English forever
- Cortex Search Service = managed RAG (no manual vector embeddings)
- Snowflake Agent = one chatbot interface for all clinical data + documents
