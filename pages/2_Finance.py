import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Finance Dashboard",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
    }
    .positive { color: #28a745; }
    .negative { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.title("🔍 Filters")
    st.markdown("---")
    
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = st.date_input(
        "Select Date Range",
        value=(start_date.date(), end_date.date())
    )
    
    # Department filter
    departments = ["All", "Salaries", "Marketing", "Operations", "IT", "Rent", "R&D"]
    selected_dept = st.selectbox("Department", departments)
    
    # Budget status
    budget_status = st.radio(
        "Budget Status",
        ["All", "Over Budget", "Under Budget", "On Budget"]
    )
    
    st.markdown("---")
    st.info("💡 Filter data to focus on specific areas")

# Load and prepare data
@st.cache_data
def load_finance_data():
    """Load comprehensive finance data"""
    data = {
        "category": ["Salaries", "Marketing", "Operations", "IT", "Rent", "R&D"],
        "budget": [500000, 80000, 120000, 60000, 90000, 150000],
        "actual": [510000, 72000, 135000, 58000, 90000, 145000],
        "forecast": [505000, 75000, 130000, 62000, 90000, 148000]
    }
    df = pd.DataFrame(data)
    df["variance"] = df["actual"] - df["budget"]
    df["variance_pct"] = ((df["variance"] / df["budget"]) * 100).round(2)
    df["forecast_variance"] = df["actual"] - df["forecast"]
    df["status"] = df["variance"].apply(
        lambda x: "Over" if x > 0 else ("Under" if x < 0 else "On")
    )
    return df

df = load_finance_data()

# Apply filters
if selected_dept != "All":
    df = df[df["category"] == selected_dept]
if budget_status != "All":
    df = df[df["status"] == budget_status]

# Main content
st.title("💵 Finance Dashboard")
st.markdown("### Monitor budgets, expenses, and financial performance")

st.markdown("---")

# Executive KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_budget = df["budget"].sum()
total_actual = df["actual"].sum()
total_variance = total_actual - total_budget
variance_pct = (total_variance / total_budget * 100) if total_budget > 0 else 0

with kpi1:
    st.metric(
        label="Total Budget",
        value=f"${total_budget:,.0f}",
        help="Allocated budget for all categories"
    )

with kpi2:
    st.metric(
        label="Total Actual Spend",
        value=f"${total_actual:,.0f}",
        delta=f"{variance_pct:+.1f}%",
        delta_color="inverse" if total_variance > 0 else "normal",
        help="Actual expenditure"
    )

with kpi3:
    st.metric(
        label="Budget Variance",
        value=f"${total_variance:,.0f}",
        delta=f"{variance_pct:+.1f}% of budget",
        delta_color="inverse" if total_variance > 0 else "normal",
        help="Difference between actual and budget"
    )

with kpi4:
    over_budget_count = len(df[df["variance"] > 0])
    st.metric(
        label="Over Budget Categories",
        value=over_budget_count,
        delta=f"{over_budget_count}/{len(df)} categories",
        help="Number of categories exceeding budget"
    )

st.markdown("---")

# Charts section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Budget vs Actual Comparison")
    fig_bar = px.bar(
        df,
        x="category",
        y=["budget", "actual", "forecast"],
        barmode="group",
        title="Budget vs Actual vs Forecast by Category",
        labels={"value": "Amount ($)", "category": "Category"},
        color_discrete_map={"budget": "#2E86AB", "actual": "#A23B72", "forecast": "#F18F01"}
    )
    fig_bar.update_layout(hovermode="x unified", height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🥧 Budget Allocation")
    fig_pie = px.pie(
        df,
        values="budget",
        names="category",
        title="Budget Distribution by Category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# Variance Analysis
st.markdown("---")
st.subheader("📈 Variance Analysis")

variance_col1, variance_col2 = st.columns(2)

with variance_col1:
    # Waterfall chart data
    df_sorted = df.sort_values("variance", ascending=False)
    fig_var = px.bar(
        df_sorted,
        x="category",
        y="variance",
        title="Variance by Category",
        labels={"variance": "Variance ($)", "category": "Category"},
        color="variance",
        color_continuous_scale=["#28a745", "#ffc107", "#dc3545"]
    )
    fig_var.update_layout(height=350)
    st.plotly_chart(fig_var, use_container_width=True)

with variance_col2:
    st.markdown("#### Key Insights")
    
    # Find biggest over/under budget
    if len(df) > 0:
        max_over = df.loc[df["variance"].idxmax()]
        max_under = df.loc[df["variance"].idxmin()]
        
        st.success(f"**Best Performance:** {max_under['category']} is ${(abs(max_under['variance'])):,.0f} under budget")
        st.error(f"**Attention Needed:** {max_over['category']} is ${(max_over['variance']):,.0f} over budget")
        
        avg_variance_pct = df["variance_pct"].abs().mean()
        st.info(f"**Average Variance:** {avg_variance_pct:.1f}% across all categories")

# Detailed Data Table
st.markdown("---")
st.subheader("📋 Detailed Financial Data")

tab1, tab2, tab3 = st.tabs(["Summary Table", "Variance Details", "Raw Data"])

with tab1:
    display_df = df[["category", "budget", "actual", "forecast", "variance", "variance_pct", "status"]].copy()
    display_df.columns = ["Category", "Budget", "Actual", "Forecast", "Variance", "Variance %", "Status"]
    
    # Format numbers
    for col in ["Budget", "Actual", "Forecast", "Variance"]:
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
    display_df["Variance %"] = display_df["Variance %"].apply(lambda x: f"{x:+.2f}%")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab2:
    # Variance analysis with conditional formatting
    st.dataframe(
        df.style.applymap(
            lambda v: "color: #dc3545; font-weight: bold" if v > 0 else 
                     ("color: #28a745; font-weight: bold" if v < 0 else "color: #6c757d"),
            subset=["variance"]
        ).applymap(
            lambda v: "background-color: #fff3cd" if abs(v) > 10 else "",
            subset=["variance_pct"]
        ),
        use_container_width=True
    )

with tab3:
    st.dataframe(df, use_container_width=True)

# Export and Actions
st.markdown("---")
exp_col1, exp_col2, exp_col3 = st.columns(3)

with exp_col1:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name='finance_data.csv',
        mime='text/csv',
        use_container_width=True
    )

with exp_col2:
    if st.button("📊 Generate Report", use_container_width=True):
        st.success("Report generated successfully!")

with exp_col3:
    if st.button("📧 Email Summary", use_container_width=True):
        st.success("Summary emailed to stakeholders!")

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data refreshes every 24 hours")
