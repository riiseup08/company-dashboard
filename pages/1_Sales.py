import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.title("📊 Filters")
    st.markdown("---")
    
    # Date range filter
    date_range = st.date_input(
        "Select Date Range",
        value=(datetime(2024, 1, 1).date(), datetime.now().date()),
        help="Filter sales data by date range"
    )
    
    # Region filter
    regions = ["All", "North", "South", "East", "West"]
    selected_region = st.selectbox("Select Region", regions)
    
    # Product category filter
    categories = ["All", "Electronics", "Clothing", "Food", "Services"]
    selected_category = st.multiselect("Select Categories", categories[1:], default=categories[1:])
    
    st.markdown("---")
    st.info("💡 Use filters to customize your view")

# Load sample data
@st.cache_data
def load_sales_data():
    """Load and prepare sales data"""
    data = {
        "Date": pd.date_range(start="2024-01-01", periods=90, freq="D"),
        "Region": ["North", "South", "East", "West"] * 22 + ["North", "South"],
        "Category": ["Electronics", "Clothing", "Food", "Services"] * 22 + ["Electronics", "Clothing"],
        "Product": [f"Product_{i%10}" for i in range(90)],
        "Units_Sold": [150, 120, 180, 90, 200, 160, 140, 110] * 11 + [150, 120],
        "Revenue": [45000, 36000, 54000, 27000, 60000, 48000, 42000, 33000] * 11 + [45000, 36000],
        "Cost": [30000, 24000, 36000, 18000, 40000, 32000, 28000, 22000] * 11 + [30000, 24000],
        "Customer_ID": [f"CUST_{i:04d}" for i in range(1, 91)]
    }
    df = pd.DataFrame(data)
    df["Profit"] = df["Revenue"] - df["Cost"]
    df["Profit_Margin"] = ((df["Profit"] / df["Revenue"]) * 100).round(2)
    return df

df = load_sales_data()

# Apply filters
if selected_region != "All":
    df = df[df["Region"] == selected_region]
if selected_category:
    df = df[df["Category"].isin(selected_category)]

# Main content
st.title("💰 Sales Dashboard")
st.markdown("### Track your sales performance and revenue trends")

st.markdown("---")

# KPI Metrics
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
avg_margin = df["Profit_Margin"].mean()
total_units = df["Units_Sold"].sum()

with kpi1:
    st.metric(
        label="Total Revenue",
        value=f"${total_revenue:,.0f}",
        delta="+8.2%",
        help="Total revenue for selected period"
    )

with kpi2:
    st.metric(
        label="Total Profit",
        value=f"${total_profit:,.0f}",
        delta="+12.5%",
        help="Total profit after costs"
    )

with kpi3:
    st.metric(
        label="Avg Profit Margin",
        value=f"{avg_margin:.1f}%",
        delta="+2.3%",
        help="Average profit margin percentage"
    )

with kpi4:
    st.metric(
        label="Units Sold",
        value=f"{total_units:,}",
        delta="+15.7%",
        help="Total units sold"
    )

st.markdown("---")

# Charts section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue Trend")
    daily_revenue = df.groupby("Date")["Revenue"].sum().reset_index()
    fig_trend = px.line(
        daily_revenue, 
        x="Date", 
        y="Revenue",
        title="Daily Revenue Trend",
        markers=True
    )
    fig_trend.update_layout(hovermode="x unified")
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.subheader("📊 Sales by Category")
    category_sales = df.groupby("Category")["Revenue"].sum().reset_index()
    fig_pie = px.pie(
        category_sales,
        values="Revenue",
        names="Category",
        title="Revenue Distribution by Category",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Regional performance
st.markdown("---")
st.subheader("🌍 Regional Performance")
regional_data = df.groupby("Region").agg({
    "Revenue": "sum",
    "Profit": "sum",
    "Units_Sold": "sum"
}).reset_index()

fig_map = px.bar(
    regional_data,
    x="Region",
    y="Revenue",
    color="Profit",
    title="Revenue by Region (colored by Profit)",
    labels={"Revenue": "Revenue ($)", "Profit": "Profit ($)"}
)
st.plotly_chart(fig_map, use_container_width=True)

# Data table
st.markdown("---")
st.subheader("📋 Detailed Sales Data")

tab1, tab2 = st.tabs(["Summary", "Raw Data"])

with tab1:
    summary = df.groupby("Category").agg({
        "Revenue": ["sum", "mean"],
        "Profit": ["sum", "mean"],
        "Units_Sold": "sum",
        "Profit_Margin": "mean"
    }).round(2)
    st.dataframe(summary, use_container_width=True)

with tab2:
    st.dataframe(df, use_container_width=True)

# Export functionality
st.markdown("---")
col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name='sales_data.csv',
        mime='text/csv',
        use_container_width=True
    )

with col_exp2:
    if st.button("📧 Share Report", use_container_width=True):
        st.success("Report link copied to clipboard!")