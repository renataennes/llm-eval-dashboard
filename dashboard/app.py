# ============================================================
# PROJECT 3 — LLM Eval Dashboard (Streamlit)
# Author: Renata Araújo | AI Model Evaluation Portfolio
# ============================================================
# SETUP:
#   pip install streamlit plotly pandas wordcloud matplotlib
#
# RUN:
#   streamlit run dashboard/app.py
# ============================================================
# ── app.py — Entry point do dashboard 
# Streamlit usa este ficheiro para arrancar a aplicação
# As páginas ficam na pasta pages/ e carregam automaticamente

import streamlit as st

st.set_page_config(
    page_title="LLM Eval Dashboard",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 LLM Evaluation Dashboard")
st.markdown("**Renata Araújo** · AI Evaluation Portfolio · Lisboa, Portugal")

st.divider()

st.markdown("""
### Sobre este dashboard

Visualização interactiva dos resultados de 3 projectos de avaliação de LLMs:

| Página | Conteúdo |
|--------|----------|
| 🔍 Hallucination Analysis | Resultados RAGAS + LLM-as-a-Judge |
| 📊 Annotation Quality | Kappa bilíngue EN/PT |
| ⚖️ Comparação | Humano vs. LLM side-by-side |
""")

st.info("Usa o menu lateral para navegar entre as páginas.")