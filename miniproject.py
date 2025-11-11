import streamlit as st
import pandas as pd
import os

# ✅ Use Streamlit’s temp directory to avoid permission issues
FILENAME = os.path.join(os.getcwd(), 'expense_data.csv')

def initialize_file():
    if not os.path.exists(FILENAME):
        df = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])
        df.to_csv(FILENAME, index=False)

def add_expense(date, amount, category, description):
    df = pd.read_csv(FILENAME)
    new_row = {'Date': date, 'Amount': amount, 'Category': category, 'Description': description}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FILENAME, index=False)

def view_expenses():
    df = pd.read_csv(FILENAME)
    return df

# --- STREAMLIT APP ---
st.set_page_config(page_title="Expense Tracker", page_icon="💰")
st.title("💰 Expense Tracker Web App")

initialize_file()

salary = st.number_input("Enter your Monthly Salary (₹):", min_value=0.0, format="%.2f")

st.header("➕ Add Expense")
date = st.date_input("Date")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
category = st.text_input("Category")
description = st.text_area("Description (optional)")

if st.button("Add Expense"):
    add_expense(date, amount, category, description)
    st.success(f"Added expense: ₹{amount:.2f}")

df = view_expenses()
if not df.empty:
    st.header("📜 All Expenses")
    st.dataframe(df)

    total = df['Amount'].sum()
    st.write(f"### 💵 Total Expenses: ₹{total:.2f}")
    if salary > 0:
        balance = salary - total
        if balance < 0:
            st.error("⚠️ You have exceeded your salary limit!")
        else:
            st.success(f"Remaining Balance: ₹{balance:.2f}")
else:
    st.info("No expenses found yet.")

