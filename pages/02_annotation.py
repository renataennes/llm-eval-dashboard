# Página 2: Annotation Quality 
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Annotation Quality", layout="wide")
st.title("📊 Annotation Quality — Bilingual EN/PT")

#  Métricas principais 
st.subheader("Inter-Annotator Agreement")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pairs", "100")
col2.metric("Languages", "EN + PT")
col3.metric("Agreement Rate", "92.0%")
col4.metric("Cohen's Kappa", "1.0", delta="faithfulness & safety")

st.divider()

# Kappa por dimensão 
st.subheader("Kappa por Dimensão")

try:
    df_kappa = pd.read_csv("../data/kappa_report.csv")

    col_left, col_right = st.columns(2)

    with col_left:
        fig = px.bar(
            df_kappa,
            x="dimensao",
            y="kappa_simples",
            color="kappa_simples",
            color_continuous_scale="RdYlGn",
            range_color=[-0.2, 1.0],
            labels={"dimensao": "Dimensão", "kappa_simples": "Kappa"},
            title="Cohen's Kappa por Dimensão"
        )
        fig.add_hline(
            y=0.60,
            line_dash="dash",
            line_color="orange",
            annotation_text="Threshold aceitável (0.60)"
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("#### Interpretação")
        for _, row in df_kappa.iterrows():
            dim = row["dimensao"]
            k = row["kappa_simples"]
            if k == 1.0:
                st.success(f"**{dim}** — κ = 1.0 ✅ Perfeito")
            elif k >= 0.60:
                st.info(f"**{dim}** — κ = {k:.3f} ✅ Bom")
            elif k == 0.0:
                st.warning(f"**{dim}** — κ = 0.0 ⚠️ 1 discordância (n=10)")
            else:
                st.warning(f"**{dim}** — κ = {k:.3f} ⚠️ Ver análise")

        st.caption(
            "Kappas baixos reflectem tamanho da amostra (n=10), "
            "não inconsistência. Agreement rate global: 92%."
        )

except FileNotFoundError:
    st.warning("kappa_report.csv não encontrado em data/")

st.divider()

# Discordâncias bilíngues 
st.subheader("Discordâncias EN/PT — Análise Qualitativa")

discordancias = {
    "MIR-F2": {
        "dimensao": "Completeness",
        "en": 5, "pt": 4,
        "motivo": "PT omits Fahrenheit scale — less relevant for Portuguese audiences"
    },
    "MIR-F4": {
        "dimensao": "Completeness",
        "en": 4, "pt": 5,
        "motivo": "PT richer — historical detail about Brasília included"
    },
    "MIR-A2": {
        "dimensao": "Fluency",
        "en": 5, "pt": 4,
        "motivo": "PT does not mention AVC explicitly — minor omission"
    },
    "MIR-C1": {
        "dimensao": "Relevance",
        "en": 5, "pt": 4,
        "motivo": "Meetup has low penetration in PT/BR market"
    },
}

for par, dados in discordancias.items():
    with st.expander(f"{par} — {dados['dimensao']}"):
        col_a, col_b = st.columns(2)
        col_a.metric("EN Score", dados["en"])
        col_b.metric("PT Score", dados["pt"])
        st.info(f"**Root cause:** {dados['motivo']}")

st.divider()

# Bias analysis 
st.subheader("LLM-as-a-Judge Bias Analysis")

col1, col2, col3 = st.columns(3)
col1.metric("Position Bias",   "0%",   delta="🟢 Low")
col2.metric("Verbosity Bias",  "30%",  delta="🟡 Moderate")
col3.metric("Confidence Bias", "100%", delta="🔴 High")

st.warning(
    "**Key finding:** Confidence bias is systematic and severe — "
    "tone alone overrides content in 100% of cases. "
    "Human oversight is essential for safety-critical tasks."
)