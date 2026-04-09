import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Company Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2920/2920323.png", width=80)
    st.title("Navigation")
    st.markdown("---")
    
    # Date filter
    st.subheader("📅 Filters")
    date_range = st.date_input(
        "Select Date Range",
        value=(datetime.now().date(), datetime.now().date()),
        help="Filter data by date range"
    )
    
    st.markdown("---")
    st.info("💡 Tip: Use the sidebar to navigate between pages and apply filters.")
    
    # Footer
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Main page content
st.title("📊 Company Dashboard")
st.markdown("### Welcome to your business intelligence platform!")

st.markdown("""
This dashboard provides comprehensive insights into your company's performance across different departments.
Navigate using the sidebar to explore:
- **Sales**: Track revenue, trends, and sales performance
- **Finance**: Monitor budgets, expenses, and financial metrics
""")

st.markdown("---")

# Quick stats overview
st.subheader("🎯 Quick Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Revenue",
        value="$1.2M",
        delta="+12.5%",
        help="Year-to-date revenue"
    )

with col2:
    st.metric(
        label="Active Projects",
        value="24",
        delta="+3",
        help="Currently active projects"
    )

with col3:
    st.metric(
        label="Team Members",
        value="48",
        delta="+2",
        help="Active team members"
    )

with col4:
    st.metric(
        label="Customer Satisfaction",
        value="94%",
        delta="+2.1%",
        help="Average satisfaction score"
    )

st.markdown("---")

# Recent activity section
st.subheader("📈 Recent Activity")
activity_data = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=7, freq="D"),
    "Sales": [12000, 15000, 13500, 18000, 16500, 19000, 17500],
    "Expenses": [8000, 9500, 8800, 10200, 9800, 11000, 10500]
})

tab1, tab2 = st.tabs(["📊 Chart", "📋 Data"])

with tab1:
    st.line_chart(activity_data.set_index("Date"))

with tab2:
    st.dataframe(activity_data, use_container_width=True)

# Call to action
st.markdown("---")
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("📥 Export Report", use_container_width=True):
        st.success("Report exported successfully!")

with col_btn2:
    if st.button("📧 Share Dashboard", use_container_width=True):
        st.success("Dashboard link copied to clipboard!")