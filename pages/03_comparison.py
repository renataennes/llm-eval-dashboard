# Página 3: Comparação Humano vs. LLM 
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Comparação", layout="wide")
st.title("⚖️ Human vs. LLM-as-a-Judge")

st.markdown(
    "Comparação directa entre anotação humana bilíngue (EN/PT) "
    "e avaliação automática por LLM."
)

st.divider()

# Agreement overview 
st.subheader("Agreement Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Human vs. LLM Agreement", "100%")
col2.metric("Cohen's Kappa (κ)",        "1.0")
col3.metric("Disagreements",            "0/20")

st.success(
    "The LLM judge achieved perfect agreement with human annotation "
    "on the HaluEval dataset — all 20 cases classified as FACTUAL_ERROR."
)

st.divider()

# Comparação das abordagens 
st.subheader("Abordagens Comparadas")

dados_comp = {
    "Abordagem":      ["Human (Bilingual)", "LLM-as-a-Judge", "RAGAS"],
    "Tipo":           ["Manual", "Automático", "Automático"],
    "Custo":          ["Alto", "Baixo", "Baixo"],
    "Velocidade":     ["Lento", "Rápido", "Rápido"],
    "Confiabilidade": ["Alta", "Moderada", "Depende do modelo"],
    "Viés conhecido": ["Cultural/linguístico", "Confidence (100%)", "Context window"],
}

st.dataframe(pd.DataFrame(dados_comp), use_container_width=True)

st.divider()

# Radar chart 
st.subheader("Perfil de Qualidade — Radar")

categorias = [
    "Faithfulness", "Relevance",
    "Fluency", "Completeness", "Safety"
]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[1.0, 0.0, 0.0, -0.111, 1.0],
    theta=categorias,
    fill="toself",
    name="Cohen's Kappa EN/PT",
    line_color="#6366f1"
))

fig.add_trace(go.Scatterpolar(
    r=[1.0, 1.0, 1.0, 1.0, 1.0],
    theta=categorias,
    fill="toself",
    name="Human vs. LLM (HaluEval)",
    line_color="#16a34a",
    opacity=0.4
))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[-0.2, 1.0])),
    showlegend=True,
    height=450
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Conclusão 
st.subheader("Conclusão")

st.markdown("""
**O que esta análise mostra:**

1. **Anotação bilíngue é insubstituível** para tarefas com variação cultural
   — as 4 discordâncias EN/PT têm justificativa linguística clara que
   um avaliador monolíngue não capturaria.

2. **LLM-as-a-Judge funciona bem para erros factuais óbvios** (κ = 1.0
   no HaluEval) mas falha em casos subtis e tem confidence bias de 100%.

3. **A combinação das duas abordagens é o estado da arte** — automático
   para escala, humano bilíngue para calibração e casos edge.
""")