# ── Página 1: Hallucination Analysis ─────────────────────────────────
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Hallucination Analysis", layout="wide")
st.title("🔍 Hallucination Analysis")

# Carregar dados 
# csvs carregados para a pasta

@st.cache_data
def carregar_dados():
    ragas = pd.read_csv("data/ragas_baseline.csv")
    judge = pd.read_csv("data/llm_judge_results.csv")
    red   = pd.read_csv("data/red_team_results.csv")
    return ragas, judge, red

try:
    df_ragas, df_judge, df_red = carregar_dados()

    # Métricas no topo
    st.subheader("RAGAS Scores")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Faithfulness",      f"{df_ragas['faithfulness'].mean():.3f}",      delta="benchmark: 0.80")
    col2.metric("Answer Relevancy",  f"{df_ragas['answer_relevancy'].mean():.3f}",  delta="benchmark: 0.80")
    col3.metric("Context Recall",    f"{df_ragas['context_recall'].mean():.3f}",    delta="benchmark: 0.70")
    col4.metric("Context Precision", f"{df_ragas['context_precision'].mean():.3f}", delta="benchmark: 0.80")

    st.divider()

    #  Gráfico de barras 
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("RAGAS vs. Benchmarks")
        metricas = ["faithfulness", "answer_relevancy", "context_recall", "context_precision"]
        scores   = [df_ragas[m].mean() for m in metricas]
        benchmarks = [0.80, 0.80, 0.70, 0.80]

        fig = px.bar(
            x=metricas,
            y=scores,
            color=scores,
            color_continuous_scale="RdYlGn",
            range_color=[0, 1],
            labels={"x": "Métrica", "y": "Score"}
        )
        fig.add_hline(y=0.70, line_dash="dash", line_color="orange", annotation_text="Min. benchmark")
        fig.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("LLM-as-a-Judge — Distribuição")
        contagem = df_judge["categoria"].value_counts().reset_index()
        contagem.columns = ["Categoria", "Count"]
        fig2 = px.pie(contagem, values="Count", names="Categoria",
                      color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    #  Red Team 
    st.subheader("Red Team Results")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("✅ SAFE",    f"{(df_red['classificacao'] == 'SAFE').sum()}/10")
    col_b.metric("⚠️ PARTIAL", f"{(df_red['classificacao'] == 'PARTIAL').sum()}/10")
    col_c.metric("🔴 UNSAFE",  f"{(df_red['classificacao'] == 'UNSAFE').sum()}/10")

    st.dataframe(df_red[["categoria", "severidade", "classificacao", "explicacao"]],
                 use_container_width=True)

except FileNotFoundError:
    st.warning("Ficheiros CSV não encontrados. Copia os resultados do P1 para data/")
    st.code("cp ../rag-hallucination-detector/results/*.csv data/")