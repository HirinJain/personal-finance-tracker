import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Tracker", layout="centered")

st.title("💰 Personal Finance Tracker")

# Load data
df = pd.read_csv("finance_data.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

st.subheader("📊 All Transactions")
st.dataframe(df)

# Summary metrics
income = df[df["Amount"] > 0]["Amount"].sum()
expense = df[df["Amount"] < 0]["Amount"].sum()

col1, col2 = st.columns(2)
col1.metric("Total Income", f"₹ {income}")
col2.metric("Total Expense", f"₹ {abs(expense)}")

st.metric("Net Balance", f"₹ {income + expense}")

# Expense breakdown
st.subheader("🧾 Expense Breakdown by Category")
expense_df = df[df["Amount"] < 0]

if not expense_df.empty:
    fig, ax = plt.subplots()
    expense_df.groupby("Category")["Amount"].sum().abs().plot(
        kind="pie", autopct="%1.1f%%", ax=ax
    )
    st.pyplot(fig)
else:
    st.info("No expense data available")

# Monthly trend
st.subheader("📈 Monthly Expense Trend")
monthly = df[df["Amount"] < 0].groupby(df["Date"].dt.to_period("M"))["Amount"].sum()

if not monthly.empty:
    st.line_chart(monthly.abs())
