import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Finance", layout="wide")
st.title("💰 Finance Dashboard")

@st.cache_data
def load_data():
    return pd.DataFrame({
        "category": ["Salaries","Marketing","Operations","IT","Rent"],
        "budget":   [500000, 80000, 120000, 60000, 90000],
        "actual":   [510000, 72000, 135000, 58000, 90000]
    })

df = load_data()
df["variance"]    = df["actual"] - df["budget"]
df["variance_%"]  = ((df["actual"] - df["budget"]) / df["budget"] * 100).round(1)

# ── KPIs ───────────────────────────────────────────────────────────────────
k1, k2, k3 = st.columns(3)
k1.metric("Total Budget", f"${df['budget'].sum():,.0f}")
k2.metric("Total Actual", f"${df['actual'].sum():,.0f}",
          delta=f"${df['variance'].sum():,.0f}")
k3.metric("Over Budget Categories",
          len(df[df["variance"] > 0]))

st.markdown("---")

# ── Budget vs Actual chart ─────────────────────────────────────────────────
fig = px.bar(df, x="category", y=["budget", "actual"],
             barmode="group", title="Budget vs Actual by Category")
st.plotly_chart(fig, use_container_width=True)

# ── Variance table ─────────────────────────────────────────────────────────
st.subheader("Variance Analysis")
st.dataframe(
    df.style.applymap(
        lambda v: "color: red" if isinstance(v, float) and v > 0 else "color: green",
        subset=["variance"]
    ),
    use_container_width=True
)
