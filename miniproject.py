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

def delete_expense(index):
    df = pd.read_csv(FILENAME)
    df = df.drop(index)
    df.to_csv(FILENAME, index=False)

def edit_expense(index, date, amount, category, description):
    df = pd.read_csv(FILENAME)
    df.loc[index, ['Date', 'Amount', 'Category', 'Description']] = [date, amount, category, description]
    df.to_csv(FILENAME, index=False)

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

    for i, row in df.iterrows():
        with st.expander(f"{row['Date']} | ₹{row['Amount']} - {row['Category']}"):
            st.write(f"**Description:** {row['Description']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"✏️ Edit {i}", key=f"edit_{i}"):
                    with st.form(f"edit_form_{i}"):
                        new_date = st.date_input("Date", pd.to_datetime(row['Date']))
                        new_amount = st.number_input("Amount", value=float(row['Amount']), min_value=0.0, format="%.2f")
                        new_category = st.text_input("Category", value=row['Category'])
                        new_description = st.text_area("Description", value=row['Description'])
                        submit_edit = st.form_submit_button("Save Changes")
                        if submit_edit:
                            edit_expense(i, new_date, new_amount, new_category, new_description)
                            st.success("Expense updated successfully.")
                            st.rerun()

            with col2:
                if st.button(f"🗑️ Delete {i}", key=f"delete_{i}"):
                    delete_expense(i)
                    st.warning("Expense deleted.")
                    st.rerun()

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
