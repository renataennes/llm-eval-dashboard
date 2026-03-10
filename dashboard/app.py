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

import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="LLM Eval Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────

@st.cache_data
def load_rag_results():
    """Load RAG evaluation results from Project 1."""
    results = []
    for lang in ["en", "pt"]:
        path = Path(f"data/eval_results_{lang}.json")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
                for item in items:
                    item["source"] = "rag"
                results.extend(items)
    return pd.DataFrame(results)


@st.cache_data
def load_annotation_results():
    """Load annotation results from Project 2."""
    results = []
    for lang in ["en", "pt"]:
        path = Path(f"data/annotations_{lang}.jsonl")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    item = json.loads(line)
                    item["source"] = "annotation"
                    results.append(item)
    return pd.DataFrame(results)


def get_sample_data():
    """Generate synthetic sample data for demo purposes."""
    import random
    random.seed(42)
    models = ["gpt-4o", "claude-3.5-sonnet", "gemini-1.5-pro"]
    languages = ["en", "pt"]
    categories = ["factual", "reasoning", "adversarial", "ambiguous", "instructional"]
    labels = ["excellent", "acceptable", "needs_improvement", "reject"]
    hallucination_labels = ["faithful", "partially_grounded", "hallucinated"]

    rows = []
    for i in range(120):
        model = random.choice(models)
        lang = random.choice(languages)
        # PT has slightly more hallucinations (realistic)
        h_weights = [0.65, 0.20, 0.15] if lang == "en" else [0.55, 0.25, 0.20]
        rows.append({
            "id": f"{lang}_{i:03d}",
            "language": lang,
            "model": model,
            "prompt_category": random.choice(categories),
            "hallucination_label": random.choices(hallucination_labels, weights=h_weights)[0],
            "faithfulness_score": round(random.uniform(0.5, 1.0), 2),
            "helpfulness": random.randint(2, 5),
            "safety": random.randint(3, 5),
            "fluency": random.randint(3, 5),
            "overall_label": random.choices(labels, weights=[0.35, 0.40, 0.18, 0.07])[0],
            "prompt": f"Sample question #{i}",
            "response": f"Sample response #{i}",
        })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────
# LOAD DATA (use real data if available, else demo)
# ─────────────────────────────────────────────

try:
    rag_df = load_rag_results()
    ann_df = load_annotation_results()
    if len(rag_df) == 0 and len(ann_df) == 0:
        df = get_sample_data()
        st.sidebar.warning("⚠️ Using demo data. Add real evaluation files to /data")
    else:
        df = get_sample_data()  # Replace with real merge logic
except Exception:
    df = get_sample_data()
    st.sidebar.info("📋 Running with demo data")


# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────

st.sidebar.title("🔍 Filters")

selected_models = st.sidebar.multiselect(
    "Models",
    options=df["model"].unique().tolist(),
    default=df["model"].unique().tolist()
)

selected_languages = st.sidebar.multiselect(
    "Language",
    options=["en", "pt"],
    default=["en", "pt"]
)

selected_categories = st.sidebar.multiselect(
    "Prompt Category",
    options=df["prompt_category"].unique().tolist(),
    default=df["prompt_category"].unique().tolist()
)

filtered_df = df[
    (df["model"].isin(selected_models)) &
    (df["language"].isin(selected_languages)) &
    (df["prompt_category"].isin(selected_categories))
]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.title("📊 LLM Eval Dashboard")
st.caption("AI Model Evaluation Portfolio · Renata Araújo · [LinkedIn](https://www.linkedin.com/in/renata-araujo-en/)")
st.divider()

# ─────────────────────────────────────────────
# TAB LAYOUT
# ─────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Overview",
    "🔴 Hallucination",
    "🌐 EN vs PT",
    "🤖 Model Comparison",
    "🔍 Example Explorer"
])


# ─────── TAB 1: OVERVIEW ───────
with tab1:
    total = len(filtered_df)
    hallucinated = (filtered_df["hallucination_label"] == "hallucinated").sum()
    hallucination_rate = hallucinated / total if total > 0 else 0
    avg_faithfulness = filtered_df["faithfulness_score"].mean()
    pct_excellent = (filtered_df["overall_label"] == "excellent").sum() / total if total > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Evaluated", total)
    col2.metric("Hallucination Rate", f"{hallucination_rate:.0%}",
                delta=f"{(hallucination_rate - 0.15):.0%} vs benchmark",
                delta_color="inverse")
    col3.metric("Avg Faithfulness", f"{avg_faithfulness:.2f}")
    col4.metric("Excellent Responses", f"{pct_excellent:.0%}")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        label_counts = filtered_df["overall_label"].value_counts().reset_index()
        label_counts.columns = ["label", "count"]
        color_map = {
            "excellent": "#22c55e",
            "acceptable": "#3b82f6",
            "needs_improvement": "#f59e0b",
            "reject": "#ef4444"
        }
        fig_labels = px.bar(
            label_counts, x="label", y="count",
            color="label", color_discrete_map=color_map,
            title="Response Quality Distribution",
            labels={"label": "Label", "count": "Count"}
        )
        fig_labels.update_layout(showlegend=False)
        st.plotly_chart(fig_labels, use_container_width=True)

    with col_right:
        cat_counts = filtered_df["prompt_category"].value_counts().reset_index()
        cat_counts.columns = ["category", "count"]
        fig_cat = px.pie(
            cat_counts, values="count", names="category",
            title="Prompt Category Breakdown",
            hole=0.4
        )
        st.plotly_chart(fig_cat, use_container_width=True)


# ─────── TAB 2: HALLUCINATION ───────
with tab2:
    st.subheader("🔴 Hallucination Analysis")

    col_a, col_b = st.columns(2)

    with col_a:
        hall_by_model = filtered_df.groupby("model").apply(
            lambda x: (x["hallucination_label"] == "hallucinated").mean()
        ).reset_index()
        hall_by_model.columns = ["model", "hallucination_rate"]
        hall_by_model["hallucination_rate"] = (hall_by_model["hallucination_rate"] * 100).round(1)

        fig_hall = px.bar(
            hall_by_model.sort_values("hallucination_rate"),
            x="hallucination_rate", y="model",
            orientation="h",
            color="hallucination_rate",
            color_continuous_scale="RdYlGn_r",
            title="Hallucination Rate by Model (%)",
            labels={"hallucination_rate": "Rate (%)", "model": "Model"}
        )
        st.plotly_chart(fig_hall, use_container_width=True)

    with col_b:
        hall_by_cat = filtered_df.groupby("prompt_category").apply(
            lambda x: (x["hallucination_label"] == "hallucinated").mean()
        ).reset_index()
        hall_by_cat.columns = ["category", "hallucination_rate"]
        hall_by_cat["hallucination_rate"] = (hall_by_cat["hallucination_rate"] * 100).round(1)

        fig_cat_hall = px.bar(
            hall_by_cat.sort_values("hallucination_rate", ascending=False),
            x="category", y="hallucination_rate",
            color="hallucination_rate",
            color_continuous_scale="RdYlGn_r",
            title="Hallucination Rate by Prompt Category (%)",
        )
        st.plotly_chart(fig_cat_hall, use_container_width=True)

    # Label breakdown table
    st.subheader("Label Distribution Detail")
    pivot = filtered_df.groupby(["model", "hallucination_label"]).size().unstack(fill_value=0)
    st.dataframe(pivot, use_container_width=True)


# ─────── TAB 3: EN vs PT ───────
with tab3:
    st.subheader("🌐 English vs Portuguese Quality Gap")

    metrics = ["faithfulness_score", "helpfulness", "safety", "fluency"]
    en_df = filtered_df[filtered_df["language"] == "en"]
    pt_df = filtered_df[filtered_df["language"] == "pt"]

    comparison = pd.DataFrame({
        "metric": metrics,
        "EN": [en_df[m].mean() for m in metrics],
        "PT": [pt_df[m].mean() for m in metrics]
    })
    comparison["delta"] = comparison["PT"] - comparison["EN"]

    col_x, col_y = st.columns(2)

    with col_x:
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            name="English", x=comparison["metric"], y=comparison["EN"],
            marker_color="#3b82f6"
        ))
        fig_comp.add_trace(go.Bar(
            name="Portuguese", x=comparison["metric"], y=comparison["PT"],
            marker_color="#f97316"
        ))
        fig_comp.update_layout(
            title="EN vs PT — Average Scores per Dimension",
            barmode="group", yaxis_range=[0, 5]
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_y:
        fig_delta = px.bar(
            comparison, x="metric", y="delta",
            color="delta",
            color_continuous_scale="RdYlGn",
            title="PT–EN Delta (positive = PT better)",
            labels={"delta": "Delta", "metric": "Metric"}
        )
        fig_delta.add_hline(y=0, line_dash="dash", line_color="gray")
        st.plotly_chart(fig_delta, use_container_width=True)

    # Hallucination by language
    hall_lang = filtered_df.groupby("language").apply(
        lambda x: (x["hallucination_label"] == "hallucinated").mean() * 100
    ).reset_index()
    hall_lang.columns = ["language", "hallucination_rate"]
    st.metric("EN Hallucination Rate", f"{hall_lang[hall_lang['language']=='en']['hallucination_rate'].values[0]:.1f}%")
    st.metric("PT Hallucination Rate", f"{hall_lang[hall_lang['language']=='pt']['hallucination_rate'].values[0]:.1f}%")


# ─────── TAB 4: MODEL COMPARISON ───────
with tab4:
    st.subheader("🤖 Model Performance Comparison")

    model_stats = filtered_df.groupby("model").agg(
        faithfulness=("faithfulness_score", "mean"),
        helpfulness=("helpfulness", "mean"),
        safety=("safety", "mean"),
        fluency=("fluency", "mean"),
        total=("id", "count")
    ).reset_index()

    # Radar chart
    categories_radar = ["faithfulness", "helpfulness", "safety", "fluency"]

    fig_radar = go.Figure()
    for _, row in model_stats.iterrows():
        values = [row[c] for c in categories_radar]
        values_normalized = [v / 5 for v in values]
        fig_radar.add_trace(go.Scatterpolar(
            r=values_normalized + [values_normalized[0]],
            theta=categories_radar + [categories_radar[0]],
            fill="toself",
            name=row["model"]
        ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        title="Model Quality Radar (normalized 0–1)"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.dataframe(
        model_stats.style.background_gradient(
            subset=["faithfulness", "helpfulness", "safety", "fluency"],
            cmap="RdYlGn"
        ),
        use_container_width=True
    )


# ─────── TAB 5: EXAMPLE EXPLORER ───────
with tab5:
    st.subheader("🔍 Browse Annotated Examples")

    col_f1, col_f2, col_f3 = st.columns(3)
    filter_model = col_f1.selectbox("Model", ["All"] + df["model"].unique().tolist())
    filter_lang = col_f2.selectbox("Language", ["All", "en", "pt"])
    filter_label = col_f3.selectbox("Label", ["All"] + df["hallucination_label"].unique().tolist())

    sample = filtered_df.copy()
    if filter_model != "All":
        sample = sample[sample["model"] == filter_model]
    if filter_lang != "All":
        sample = sample[sample["language"] == filter_lang]
    if filter_label != "All":
        sample = sample[sample["hallucination_label"] == filter_label]

    st.write(f"Showing {len(sample)} items")

    for _, row in sample.head(10).iterrows():
        label_color = {
            "faithful": "🟢",
            "partially_grounded": "🟡",
            "hallucinated": "🔴"
        }.get(row["hallucination_label"], "⚪")

        with st.expander(f"{label_color} [{row['id']}] {row['prompt'][:80]}..."):
            st.write(f"**Model:** {row['model']} | **Language:** {row['language'].upper()} | **Category:** {row['prompt_category']}")
            st.write(f"**Hallucination Label:** {row['hallucination_label']} | **Overall:** {row['overall_label']}")
            st.write(f"**Faithfulness Score:** {row['faithfulness_score']}")
            st.divider()
            st.write(f"**Prompt:** {row['prompt']}")
            st.write(f"**Response:** {row['response']}")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────

st.divider()
st.caption("Built by Renata Araújo · AI Model Evaluation Portfolio · [GitHub](https://github.com/renataennes) · [LinkedIn](https://www.linkedin.com/in/renata-araujo-en/)")
