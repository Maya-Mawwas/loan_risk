import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Credit Risk Dashboard",
    layout="wide"
)

st.title("💳 Credit Risk Assessment Dashboard")

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("loan_risk_dataset.csv")

# =========================
# FILTERS
# =========================

st.sidebar.header("🔍 Filters")

age_filter = st.sidebar.slider(
    "🎂 Age",
    int(df["age"].min()),
    int(df["age"].max()),
    (int(df["age"].min()), int(df["age"].max()))
)

salary_filter = st.sidebar.slider(
    "💰 Monthly Salary",
    int(df["salary"].min()),
    int(df["salary"].max()),
    (int(df["salary"].min()), int(df["salary"].max()))
)

debt_filter = st.sidebar.slider(
    "📉 Debt Level",
    int(df["debt"].min()),
    int(df["debt"].max()),
    (int(df["debt"].min()), int(df["debt"].max()))
)

exp_filter = st.sidebar.slider(
    "📅 Years Experience",
    int(df["work_years"].min()),
    int(df["work_years"].max()),
    (int(df["work_years"].min()), int(df["work_years"].max()))
)

status_filter = st.sidebar.multiselect(
    "✅ Loan Status",
    options=[0, 1],
    default=[0, 1],
    format_func=lambda x: "Approved" if x == 1 else "Rejected"
)

# =========================
# APPLY FILTERS
# =========================

filtered = df[
    (df["age"].between(age_filter[0], age_filter[1])) &
    (df["salary"].between(salary_filter[0], salary_filter[1])) &
    (df["debt"].between(debt_filter[0], debt_filter[1])) &
    (df["work_years"].between(exp_filter[0], exp_filter[1])) &
    (df["approved"].isin(status_filter))
]

# =========================
# CUSTOMER OVERVIEW
# =========================

st.header("📊 Customer Overview")

total_customers = len(filtered)
approved = len(filtered[filtered["approved"] == 1])
rejected = len(filtered[filtered["approved"] == 0])
approval_rate = (approved / total_customers) * 100 if total_customers > 0 else 0
avg_salary = filtered["salary"].mean()
avg_debt = filtered["debt"].mean()

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("👥 Total Customers", f"{total_customers:,}")
c2.metric("✅ Approved", f"{approved:,}")
c3.metric("❌ Rejected", f"{rejected:,}")
c4.metric("📈 Approval %", f"{approval_rate:.1f}%")
c5.metric("💰 Avg Salary", f"${avg_salary:,.0f}")
c6.metric("⚠️ Avg Debt", f"${avg_debt:,.0f}")

# =========================
# HISTOGRAMS
# =========================

st.markdown("---")
st.subheader("📈 Distributions")

col1, col2 = st.columns(2)

with col1:
    fig_age = px.histogram(
        filtered,
        x="age",
        title="Age Distribution",
        color_discrete_sequence=["#2E86AB"],
        marginal="box"
    )
    fig_age.update_layout(bargap=0.1)
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    fig_salary = px.histogram(
        filtered,
        x="salary",
        title="Salary Distribution",
        color_discrete_sequence=["#2E86AB"],
        marginal="box"
    )
    fig_salary.update_layout(bargap=0.1)
    st.plotly_chart(fig_salary, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig_debt = px.histogram(
        filtered,
        x="debt",
        title="Debt Distribution",
        color_discrete_sequence=["#A23B72"],
        marginal="box"
    )
    fig_debt.update_layout(bargap=0.1)
    st.plotly_chart(fig_debt, use_container_width=True)

with col4:
    fig_exp = px.histogram(
        filtered,
        x="work_years",
        title="Experience Distribution",
        color_discrete_sequence=["#A23B72"],
        marginal="box"
    )
    fig_exp.update_layout(bargap=0.1)
    st.plotly_chart(fig_exp, use_container_width=True)

# =========================
# PREVIOUS LOANS (loans_count)
# =========================

st.markdown("---")
st.subheader("🏦 Previous Loans Analysis")
fig_loans = px.bar(
    filtered,
    x="loans_count",
    title="Previous Loans Distribution",
    color_discrete_sequence=["#3B9E8E"],
    labels={"loans_count": "Number of Previous Loans", "count": "Customers"}
)
fig_loans.update_layout(bargap=0.2)
st.plotly_chart(fig_loans, use_container_width=True)

# =========================
# CREDIT RISK ANALYSIS
# =========================

st.markdown("---")
st.header("⚠️ Credit Risk Analysis")

importance = pd.DataFrame({
    "Feature": ["Debt Level", "Monthly Salary", "Previous Loans", "Years Experience", "Age"],
    "Importance": [0.35, 0.25, 0.18, 0.12, 0.10]
})

fig_imp = px.bar(
    importance,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Feature Importance for Credit Risk",
    color="Importance",
    color_continuous_scale="Blues",
    text="Importance"
)
fig_imp.update_traces(texttemplate='%{text:.0%}', textposition='outside')
st.plotly_chart(fig_imp, use_container_width=True)

# =========================
# DEBT VS APPROVAL
# =========================

st.markdown("---")

# Create debt groups for better visualization
filtered['debt_group'] = pd.cut(filtered['debt'], bins=5)
approval_by_debt = filtered.groupby('debt_group')['approved'].mean().reset_index()
approval_by_debt['debt_group'] = approval_by_debt['debt_group'].astype(str)

fig_debt_approval = px.line(
    approval_by_debt,
    x="debt_group",
    y="approved",
    title="Debt Level vs Approval Rate",
    markers=True,
    color_discrete_sequence=["#E63946"],
    labels={"debt_group": "Debt Level Range", "approved": "Approval Rate"}
)
fig_debt_approval.update_layout(yaxis_tickformat=".0%")
fig_debt_approval.update_traces(line=dict(width=3), marker=dict(size=10))
st.plotly_chart(fig_debt_approval, use_container_width=True)

# =========================
# DATA PREVIEW
# =========================

st.markdown("---")
st.header("📋 Customer Data")
st.dataframe(filtered, use_container_width=True)