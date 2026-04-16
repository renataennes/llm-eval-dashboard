## 📊 Interactive dashboard to compare LLM performance across hallucination, faithfulness, and response quality, with bilingual evaluation (English 🇺🇸 / 
## Portuguese 🇧🇷🇵🇹).

**Stack:** Streamlit · Plotly · Pandas  

---

## 📌 Why this project

Most LLM demos look good — but fail under real evaluation.

This project answers:

How often do models hallucinate?
Do they perform differently across languages?
Can we systematically compare quality?

Built with Streamlit + Plotly — deployable to Streamlit Cloud for free in minutes.

This project bridges two worlds: **Data Analyst skills** (dashboards, KPIs, visualization) and **AI Evaluation expertise** 

**Live demo:** [(https://llm-eval-dashboard-4c5ztls4equwaqjbnu9rsu.streamlit.app/)]  

---

## 🎯 Objectives

🧠 What this evaluates

Each response is analyzed across:

Faithfulness → Is the answer grounded in the source?
Hallucination rate → % of unsupported claims
Relevance → Does it answer the question?
Language consistency (EN vs PT)

---

## 🧪 Methodology

Evaluation combines:

Rule-based checks
LLM-as-a-judge scoring
Structured evaluation dataset

(See /docs/methodology.md)

---

## 🗂️ Project Structure

```
llm-eval-dashboard/
│
├── data/
│   ├── raw/
│   │   ├── bias_confidence.csv
│   │   ├── bias_position.csv
│   │   ├── bias_verbosity.csv
│   │   ├── human_vs_llm_agreement.csv
│   │   ├── kappa_report.csv
│   │   ├── llm_judge_results.csv
│   │   ├── ragas_baseline.csv
│   │   └── red_team_results.csv
│   │
│   └── processed/
│       
│
├── src/
│   ├── __init__.py
│   ├── metrics.py          
│   ├── evaluator.py        
│   ├── bias_analysis.py    
│   └── utils.py
│
├── dashboard/
│   ├── app.py             
│   └── pages/
│       ├── hallucination.py   # (01_hallucination.py)
│       ├── annotation.py      # (02_annotation.py)
│       └── comparison.py      # (03_comparison.py)
│
├── docs/
│   ├── methodology.md      
│   └── metrics.md          
│
├── results/
│
├── .devcontainer/
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 📊 Dashboard features

Language breakdown (EN vs PT)
Hallucination distribution
Metric-based ranking

---

## 🔧 Tech Stack

| Tool | Role |
|---|---|
| `Streamlit` | Web dashboard framework |
| `Plotly` | Interactive charts |
| `Pandas` | Data wrangling |
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


## 🔗 Related Projects

- [Project 1 — RAG Hallucination Detector](https://github.com/renataennes/rag-hallucination-detector))
- [Project 2 — Bilingual LLM Annotation Test Set](https://github.com/renataennes/llm-annotation-testset))

---

*Built as part of an AI Model Evaluation portfolio. Author: Renata Araújo — [LinkedIn](https://www.linkedin.com/in/renata-araujo-en/)*

