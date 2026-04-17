# 📊 LLM Eval Dashboard

Interactive evaluation dashboard visualising results from a complete
AI Evaluation portfolio — hallucination detection, bilingual annotation
quality, and LLM-as-a-Judge bias analysis.

**Stack:** Streamlit · Plotly · Pandas  
**Status:** ✅ Live  
🔗 **[Live Demo](https://llm-eval-dashboard-4c5ztls4equwaqjbnu9rsu.streamlit.app/)**

---

## Results at a Glance

| Metric | Value |
|--------|-------|
| RAGAS Faithfulness | 0.117 |
| RAGAS Context Precision | 0.400 |
| Human vs. LLM Agreement | 100% (κ = 1.0) |
| Bilingual Agreement EN/PT | 92% (κ = 0.92) |
| Confidence Bias | 🔴 100% |
| Position Bias | 🟢 0% |
| Red Team SAFE Rate | 4/10 |
| Red Team UNSAFE Rate | 0/10 |

---

## Overview

This dashboard is the final layer of a 3-project AI Evaluation
portfolio. It brings together results from two upstream projects
into a single interactive interface — making evaluation findings
accessible without reading code.

**Three pages:**

| Page | What it shows |
|------|---------------|
| 🔍 Hallucination Analysis | RAGAS scores + LLM-as-a-Judge distribution + Red Team |
| 📊 Annotation Quality | Cohen's Kappa EN/PT + disagreement analysis + bias experiments |
| ⚖️ Comparison | Human vs. LLM side-by-side + approach tradeoffs + radar chart |

---

## Project Structure
llm-eval-dashboard/
├── app.py                        # Entry point
├── pages/
│   ├── 01_hallucination.py       # RAGAS + LLM Judge + Red Team
│   ├── 02_annotation.py          # Kappa EN/PT + bias analysis
│   └── 03_comparison.py          # Human vs. LLM comparison
├── data/
│   ├── ragas_baseline.csv
│   ├── llm_judge_results.csv
│   ├── red_team_results.csv
│   ├── kappa_report.csv
│   ├── human_vs_llm_agreement.csv
│   ├── bias_confidence.csv
│   ├── bias_position.csv
│   └── bias_verbosity.csv
├── docs/
│   └── methodology.md
├── requirements.txt
└── README.md

---

## Key Findings

**Hallucination Detection**
RAGAS scores below benchmark reflect a minimal baseline pipeline
under context window constraints — diagnostic signal, not failure.
LLM-as-a-Judge achieved κ = 1.0 agreement with human annotation
on HaluEval (20 examples, 100% FACTUAL_ERROR detection).

**Bilingual Annotation Quality**
92% agreement rate across 50 EN/PT comparisons.
All 4 disagreements have clear linguistic or cultural justification —
none are annotation errors. Bilingual evaluation captures signal
that monolingual annotation systematically misses.

**LLM-as-a-Judge Bias**
Confidence bias: 100% — tone overrides content every time.
Verbosity bias: 30% — length acts as proxy for quality.
Position bias: 0% — verdicts are stable regardless of order.

---

## Data Sources

| Dataset | Used for |
|---------|----------|
| explodinggradients/amnesty_qa | RAG evaluation (RAGAS) |
| pminervini/HaluEval | Hallucination classification |
| Custom bilingual testset | EN/PT annotation agreement |
| Custom red team prompts | Safety evaluation |

---

## Getting Started

```bash
git clone https://github.com/renataennes/llm-eval-dashboard
cd llm-eval-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---


## 🔗 Related Projects

- [Project 1 — RAG Hallucination Detector](https://github.com/renataennes/rag-hallucination-detector))
- [Project 2 — Bilingual LLM Annotation Test Set](https://github.com/renataennes/llm-annotation-testset))

---

*Built as part of an AI Model Evaluation portfolio. Author: Renata Araújo — [LinkedIn](https://www.linkedin.com/in/renata-araujo-en/)*

