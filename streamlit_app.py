import streamlit as st
import pandas as pd
import glob
import plotly.express as px
from pathlib import Path

BASE_PATH = "./data/cdm_gold"

def read_gold(folder):
    files = glob.glob(f"{BASE_PATH}/{folder}/*.csv")
    if not files:
        return pd.DataFrame()
    return pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

def read_gold_file(filename):
    path = Path(BASE_PATH) / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

st.set_page_config(page_title="Vendas Analytics", layout="wide")
st.title("Brazilian E-Commerce Public Dashboard")
st.markdown("Pipeline Medallion + Spark + BI")

# ======================
# KPIs (já existentes)
# ======================
kpi = read_gold("kpi_global")
if not kpi.empty:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Pedidos", int(kpi["total_orders"][0]))
    col2.metric("Total Clientes", int(kpi["total_customers"][0]))
    col3.metric("Receita Total", f"R$ {float(kpi['total_revenue'][0]):,.2f}")
    col4.metric("Ticket Médio", f"R$ {float(kpi['avg_ticket'][0]):,.2f}")

revenue_month = read_gold("revenue_monthly")
if not revenue_month.empty:
    revenue_month["month"] = pd.to_datetime(revenue_month["month"])
    fig = px.line(revenue_month, x="month", y="revenue", title="Evolução Mensal do Faturamento")
    st.plotly_chart(fig, use_container_width=True)

rev_cat = read_gold("revenue_category")
if not rev_cat.empty:
    fig = px.bar(rev_cat, x="revenue", y="category_en", orientation="h", title="Top 10 Categorias por Faturamento")
    st.plotly_chart(fig, use_container_width=True)

review_cat = read_gold("review_category")
if not review_cat.empty:
    fig = px.scatter(
        review_cat, x="total_orders", y="avg_review_score", size="total_orders",
        hover_name="category_en", title="Avaliação x Volume de Pedidos"
    )
    st.plotly_chart(fig, use_container_width=True)

rev_state = read_gold("revenue_state")
if not rev_state.empty:
    fig = px.bar(rev_state, x="state", y="revenue", title="Top 10 Receita por Estado")
    st.plotly_chart(fig, use_container_width=True)

# ======================
# NOVO: LLM Features
# ======================
st.divider()
st.header("LLM Insights (Amostra de Reviews)") 
llm = read_gold_file("gold_order_review_llm_features.csv")
if llm.empty:
    st.warning("Arquivo gold_order_review_llm_features.csv não encontrado em ./data/cdm_gold/")
else:
    # filtros
    llm["sentiment_score"] = pd.to_numeric(llm.get("sentiment_score"), errors="coerce")
    llm["delivery_delay_days"] = pd.to_numeric(llm.get("delivery_delay_days"), errors="coerce")
    llm["total_item_value"] = pd.to_numeric(llm.get("total_item_value"), errors="coerce")

    cats = sorted([c for c in llm["category_en"].dropna().unique()])
    sel_cat = st.multiselect("Filtrar categorias", cats, default=cats[:10] if len(cats) > 10 else cats)

    sentiments = ["positive", "neutral", "negative"]
    sel_sent = st.multiselect("Filtrar sentimento", sentiments, default=sentiments)

    df = llm.copy()
    if sel_cat:
        df = df[df["category_en"].isin(sel_cat)]
    if "sentiment_label" in df.columns:
        df = df[df["sentiment_label"].isin(sel_sent)]

    # KPIs LLM
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reviews na amostra", len(df))
    c2.metric("% Mismatch", f"{(df['expectation_mismatch'].mean()*100):.1f}%" if "expectation_mismatch" in df.columns else "—")
    c3.metric("Sentimento médio", f"{df['sentiment_score'].mean():.2f}" if "sentiment_score" in df.columns else "—")
    c4.metric("Atraso médio (dias)", f"{df['delivery_delay_days'].mean():.1f}" if "delivery_delay_days" in df.columns else "—")

    st.subheader("Distribuição de Sentimento")
    sent_counts = df["sentiment_label"].value_counts().reset_index()
    sent_counts.columns = ["sentiment_label", "count"]
    fig = px.bar(sent_counts, x="sentiment_label", y="count", title="Sentimento nas reviews (amostra)")
    st.plotly_chart(fig, use_container_width=True)


    st.subheader("Severidade das reclamações")
    if "complaint_severity" in df.columns:
        sev = df["complaint_severity"].value_counts().reset_index()
        sev.columns = ["complaint_severity", "count"]
        fig = px.bar(sev, x="complaint_severity", y="count", title="Severidade (low/medium/high)")
        st.plotly_chart(fig, use_container_width=True)

    # 3) Top 10 tópicos
    st.subheader("Top 10 tópicos mais citados")
    if "topics_top3" in df.columns:
        topics = (
            df["topics_top3"].dropna()
            .str.split(",")
            .explode()
            .str.strip()
        )
        top_topics = topics.value_counts().head(10).reset_index()
        top_topics.columns = ["topic", "count"]
        fig = px.bar(top_topics, x="count", y="topic", orientation="h", title="Top 10 tópicos (LLM)")
        st.plotly_chart(fig, use_container_width=True)

    # tabela detalhada
    st.subheader("Tabela de reviews enriquecidas (amostra)")
    show_cols = [c for c in [
        "category_en","score","sentiment_label","sentiment_score",
        "complaint_severity","complaint_reason","expectation_mismatch",
        "delivery_delay_days","experience_summary","comment_message"
    ] if c in df.columns]
    st.dataframe(df[show_cols].head(30), use_container_width=True)
