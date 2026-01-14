import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Personal Finance Tracker", layout="centered")
st.title("💰 Personal Finance Tracker")

CSV_FILE = "finance_data.csv"

# Load data safely
def load_data():
    df = pd.read_csv(CSV_FILE)
    df = df[["Date", "Amount", "Category", "Description"]]
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["Date"])
    return df

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

df = load_data()

# SIDEBAR MENU
menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Add Transaction", "View Data"]
)

# DASHBOARD
if menu == "Dashboard":
    income = df[df["Amount"] > 0]["Amount"].sum()
    expense = df[df["Amount"] < 0]["Amount"].sum()
    balance = income + expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"₹{income:.2f}")
    col2.metric("Expense", f"₹{abs(expense):.2f}")
    col3.metric("Balance", f"₹{balance:.2f}")

    st.subheader("🧾 Expense Breakdown")
    expense_df = df[df["Amount"] < 0]
    if not expense_df.empty:
        fig, ax = plt.subplots()
        expense_df.groupby("Category")["Amount"].sum().abs().plot(
            kind="pie", autopct="%1.1f%%", ax=ax
        )
        st.pyplot(fig)

# ADD TRANSACTION
elif menu == "Add Transaction":
    st.subheader("➕ Add New Transaction")

    t_date = st.date_input("Date")
    txn_type = st.selectbox("Transaction Type", ["Income", "Expense"])
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    category = st.text_input("Category")
    description = st.text_input("Description")

    if st.button("Add Transaction"):
        final_amount = amount if txn_type == "Income" else -amount

        new_row = pd.DataFrame([{
            "Date": t_date,
            "Amount": final_amount,
            "Category": category,
            "Description": description
        }])

        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success(f"{txn_type} added successfully!")


# VIEW DATA
elif menu == "View Data":
    st.subheader("📊 All Transactions")
    st.dataframe(df, use_container_width=True)
