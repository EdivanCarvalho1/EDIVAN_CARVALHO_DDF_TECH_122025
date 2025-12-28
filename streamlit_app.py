import streamlit as st
import pandas as pd
import glob
import plotly.express as px

BASE_PATH = "./data/cdm_gold/"

def read_gold(folder):
    files = glob.glob(f"{BASE_PATH}/{folder}/*.csv")
    return pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

st.set_page_config(
    page_title="Olist Analytics",
    layout="wide"
)

st.title("Brazilian E-Commerce Public Dashboard")
st.markdown("Pipeline Medallion + Spark + BI")

kpi = read_gold("kpi_global")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Pedidos", int(kpi["total_orders"][0]))
col2.metric("Total Clientes", int(kpi["total_customers"][0]))
col3.metric("Receita Total", f"R$ {kpi['total_revenue'][0]:,.2f}")
col4.metric("Ticket Médio", f"R$ {kpi['avg_ticket'][0]:,.2f}")

revenue_month = read_gold("revenue_monthly")
revenue_month["month"] = pd.to_datetime(revenue_month["month"])

fig = px.line(
    revenue_month,
    x="month",
    y="revenue",
    title="Evolução Mensal do Faturamento"
)

st.plotly_chart(fig, use_container_width=True)

rev_cat = read_gold("revenue_category")

fig = px.bar(
    rev_cat,
    x="revenue",
    y="category_en",
    orientation="h",
    title="Top 10 Categorias por Faturamento"
)

st.plotly_chart(fig, use_container_width=True)

review_cat = read_gold("review_category")

fig = px.scatter(
    review_cat,
    x="total_orders",
    y="avg_review_score",
    size="total_orders",
    hover_name="category_en",
    title="Avaliação x Volume de Pedidos"
)

st.plotly_chart(fig, use_container_width=True)

rev_state = read_gold("revenue_state")

fig = px.bar(
    rev_state,
    x="state",
    y="revenue",
    title="Top 10 Receita por Estado"
)

st.plotly_chart(fig, use_container_width=True)
