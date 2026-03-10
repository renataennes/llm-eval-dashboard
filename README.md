# 📊 LLM Eval Dashboard — Model Comparison & Quality Monitoring

> **AI Model Evaluation Portfolio Project** | Renata Araújo  
> Skills: Python · Streamlit · Power BI · Pandas · Plotly · Data Visualization · LLM Evaluation

---

## 📌 Overview

An interactive **evaluation dashboard** that compares LLM quality across models (GPT-4o, Claude 3.5, Gemini 1.5) and languages (EN/PT), using results from Projects 1 and 2 as data sources.

Built with Streamlit + Plotly — deployable to Streamlit Cloud for free in minutes.

This project bridges two worlds: **Data Analyst skills** (dashboards, KPIs, visualization) and **AI Evaluation expertise** — showing exactly the combination that top AI labs look for.

**Live demo:** [streamlit.app/renataennes-llm-eval →](#)  
**Power BI version:** [`dashboard/LLM_Eval_Dashboard.pbix`](dashboard/LLM_Eval_Dashboard.pbix)

---

## 🎯 Objectives

- Aggregate evaluation results from Projects 1 and 2 into a unified view
- Compare hallucination rates, faithfulness, and quality scores across models
- Visualize performance gaps between English and Portuguese
- Export reports for stakeholder communication

---

## 🗂️ Project Structure

```
project3-eval-dashboard/
│
├── data/
│   ├── eval_results_en.json     # From Project 1 (EN)
│   ├── eval_results_pt.json     # From Project 1 (PT)
│   ├── annotations_en.jsonl     # From Project 2 (EN)
│   └── annotations_pt.jsonl    # From Project 2 (PT)
│
├── dashboard/
│   ├── app.py                  # Main Streamlit app
│   ├── components/
│   │   ├── overview.py         # Summary KPI cards
│   │   ├── hallucination.py    # Hallucination analysis charts
│   │   ├── by_language.py      # EN vs PT comparison
│   │   ├── by_model.py         # Model comparison view
│   │   └── sample_explorer.py  # Browse individual examples
│   └── LLM_Eval_Dashboard.pbix # Power BI version
│
├── src/
│   ├── data_loader.py          # Load and normalize all eval data
│   └── metrics.py              # Reusable metric computations
│
├── requirements.txt
└── README.md
```

---

## 📊 Dashboard Sections

### 1. 🏠 Overview — KPI Cards
- Total responses evaluated
- Overall hallucination rate
- Average faithfulness score
- % of "excellent" rated responses

### 2. 🔴 Hallucination Analysis
- Hallucination rate by model (bar chart)
- Hallucination rate over time / by prompt category
- Most common unsupported claims (word cloud)

### 3. 🌐 EN vs PT Comparison
- Side-by-side quality metrics
- Gap analysis: which dimensions drop most in Portuguese
- Sample explorer filtered by language

### 4. 🤖 Model Comparison
- Faithfulness, helpfulness, safety scores per model
- Radar chart: multi-dimensional model profile
- Cost vs. quality tradeoff visualization

### 5. 🔍 Example Explorer
- Browse annotated examples with full context
- Filter by: label, category, model, language
- Highlight unsupported claims inline

---

## 🔧 Tech Stack

| Tool | Role |
|---|---|
| `Streamlit` | Web dashboard framework |
| `Plotly` | Interactive charts |
| `Pandas` | Data wrangling |
| `Power BI` | Enterprise dashboard version |
| `WordCloud` | Visualize common failure patterns |

---

## 🚀 Getting Started

```bash
# 1. Clone
git clone https://github.com/renataennes/llm-eval-dashboard
cd llm-eval-dashboard

# 2. Install
pip install -r requirements.txt

# 3. Add data from Project 1 and 2
cp ../project1-rag-hallucination/results/*.json data/
cp ../project2-annotation-testset/data/annotated/*.jsonl data/

# 4. Run dashboard
streamlit run dashboard/app.py
```

**Deploy to Streamlit Cloud (free):**
1. Push repo to GitHub
2. Go to share.streamlit.io → New app
3. Point to `dashboard/app.py`
4. Done — share the public URL

---

## 📸 Dashboard Preview

```
┌────────────────────────────────────────────────────────────┐
│  LLM EVAL DASHBOARD              Renata Araújo              │
├──────────────┬──────────────┬──────────────┬───────────────┤
│ 120 evaluated│ 18% halluci. │ 0.82 faithful│ 64% excellent │
├──────────────┴──────────────┴──────────────┴───────────────┤
│                                                             │
│  Hallucination Rate by Model          EN vs PT Gap         │
│  ┌─────────────────────────┐    ┌──────────────────────┐   │
│  │ gpt-4o     ████ 13%     │    │ EN faithfulness 0.87 │   │
│  │ claude-3.5 ███  11%     │    │ PT faithfulness 0.79 │   │
│  │ gemini-1.5 █████ 19%    │    │ Delta: -0.08 ⚠️       │   │
│  └─────────────────────────┘    └──────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

---

## 🔗 Related Projects

- [Project 1 — RAG Hallucination Detector](../project1-rag-hallucination/)
- [Project 2 — Bilingual LLM Annotation Test Set](../project2-annotation-testset/)

---

*Built as part of an AI Model Evaluation portfolio. Author: Renata Araújo — [LinkedIn](https://www.linkedin.com/in/renata-araujo-en/)*

