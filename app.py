import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Tracker", layout="centered")

st.title("💰 Personal Finance Tracker")

# Load data
df = pd.read_csv("finance_data.csv")

st.subheader("📊 Finance Data")
st.dataframe(df)

# Summary
st.subheader("📈 Summary")
total_income = df[df["Amount"] > 0]["Amount"].sum()
total_expense = df[df["Amount"] < 0]["Amount"].sum()

st.metric("Total Income", f"₹{total_income}")
st.metric("Total Expense", f"₹{abs(total_expense)}")

# Pie chart
st.subheader("🧾 Expense Breakdown")
expense_df = df[df["Amount"] < 0]
fig, ax = plt.subplots()
expense_df.groupby("Category")["Amount"].sum().abs().plot(
    kind="pie", autopct="%1.1f%%", ax=ax
)
st.pyplot(fig)
