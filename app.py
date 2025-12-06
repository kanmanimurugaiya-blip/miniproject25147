# app.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io
import matplotlib.pyplot as plt
import base64
import hashlib

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="Expense Tracker (Full)", page_icon="💰", layout="wide")

BASE_DIR = os.getcwd()
USERS_FILE = os.path.join(BASE_DIR, "users.csv")
DATA_DIR = os.path.join(BASE_DIR, "user_data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ---------------------------
# HELPERS
# ---------------------------

def hash_password(password: str):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_users_file():
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["username", "password_hash"])
        df.to_csv(USERS_FILE, index=False)

def user_file(username):
    safe = username.replace(" ", "_")
    return os.path.join(DATA_DIR, f"{safe}_expenses.csv")

def init_user_file(username):
    fn = user_file(username)
    if not os.path.exists(fn):
        df = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
        df.to_csv(fn, index=False)

def read_user_expenses(username):
    fn = user_file(username)
    if not os.path.exists(fn):
        init_user_file(username)
    return pd.read_csv(fn, parse_dates=["Date"], dayfirst=False)

def save_user_expenses(username, df):
    fn = user_file(username)
    # Ensure Date column is formatted
    df = df.copy()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df.to_csv(fn, index=False)

def add_expense(username, date, amount, category, description):
    df = read_user_expenses(username)
    new_row = {"Date": pd.to_datetime(date).date(), "Amount": float(amount), "Category": category, "Description": description}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_user_expenses(username, df)

def delete_expense(username, idx):
    df = read_user_expenses(username)
    if idx in df.index:
        df = df.drop(idx).reset_index(drop=True)
        save_user_expenses(username, df)

def edit_expense(username, idx, date, amount, category, description):
    df = read_user_expenses(username)
    if idx in df.index:
        df.loc[idx, ["Date", "Amount", "Category", "Description"]] = [pd.to_datetime(date).date(), float(amount), category, description]
        save_user_expenses(username, df)

# ---------------------------
# PDF generation (reportlab)
# ---------------------------

def create_month_summary_pdf(username, df_month, year, month, salary):
    """
    Create a simple PDF summary for the selected month for the given user.
    Requires reportlab (pip install reportlab).
    Returns bytes of PDF.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
    except Exception as e:
        raise RuntimeError("reportlab not installed. Install via `pip install reportlab` to enable PDF export.") from e

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    title = f"Expense Summary - {username} - {month}/{year}"
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, height - 1 * inch, title)

    c.setFont("Helvetica", 11)
    total = df_month["Amount"].sum()
    balance = salary - total if salary is not None else None
    c.drawString(1 * inch, height - 1.4 * inch, f"Total expenses: ₹{total:.2f}")
    if salary is not None:
        c.drawString(1 * inch, height - 1.6 * inch, f"Salary: ₹{salary:.2f}")
        c.drawString(1 * inch, height - 1.8 * inch, f"Remaining balance: ₹{balance:.2f}")

    # Show top categories
    c.drawString(1 * inch, height - 2.2 * inch, "Top categories:")
    cat_sum = df_month.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    y = height - 2.5 * inch
    for cat, amt in cat_sum.items():
        c.drawString(1.1 * inch, y, f"{cat}: ₹{amt:.2f}")
        y -= 0.2 * inch
        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch

    # Add table of transactions (simple)
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, height - 1 * inch, "Transactions")
    c.setFont("Helvetica", 10)
    y = height - 1.4 * inch
    for _, r in df_month.sort_values("Date").iterrows():
        line = f"{r['Date']} | ₹{r['Amount']:.2f} | {r['Category']} | {str(r['Description'])[:60]}"
        c.drawString(1 * inch, y, line)
        y -= 0.18 * inch
        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch

    c.save()
    buffer.seek(0)
    return buffer.read()

# ---------------------------
# UI: Dark mode toggle - simple CSS injection
# ---------------------------

def apply_theme(dark: bool):
    if dark:
        dark_css = """
        <style>
        .stApp { background-color: #0E1117; color: #E6EDF3; }
        .stButton>button { background-color:#1f6feb; color: white; }
        .css-1d391kg { background-color: #0E1117; } /* sidebar */
        .stTextInput>div>input, .stNumberInput>div>input, .stDateInput>div>input, textarea { background-color: #17202A; color: #E6EDF3; }
        .stMarkdown, .css-10trblm, .css-1v0mbdj { color: #E6EDF3; }
        .stExpander { background-color: #0E1117; color: #E6EDF3; border: 1px solid #2B2F33; }
        </style>
        """
        st.markdown(dark_css, unsafe_allow_html=True)
    else:
        st.markdown("", unsafe_allow_html=True)

# ---------------------------
# AUTH (Simple)
# ---------------------------

init_users_file()
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

def sign_up(username, password):
    users = pd.read_csv(USERS_FILE)
    if username in users["username"].values:
        st.error("Username already exists. Please choose another.")
        return False
    pwd_hash = hash_password(password)
    users = pd.concat([users, pd.DataFrame([{"username": username, "password_hash": pwd_hash}])], ignore_index=True)
    users.to_csv(USERS_FILE, index=False)
    init_user_file(username)
    st.success("Signup successful. You can now log in.")
    return True

def log_in(username, password):
    users = pd.read_csv(USERS_FILE)
    if username not in users["username"].values:
        st.error("No such user. Please sign up.")
        return False
    stored_hash = users.loc[users["username"] == username, "password_hash"].iloc[0]
    if hash_password(password) == stored_hash:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success(f"Logged in as {username}")
        return True
    else:
        st.error("Incorrect password.")
        return False

def log_out():
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.experimental_rerun()

# ---------------------------
# MAIN UI
# ---------------------------

# Sidebar: authentication + settings
with st.sidebar:
    st.title("Settings")
    dark_mode = st.checkbox("Dark mode", value=False)
    apply_theme(dark_mode)

    if not st.session_state["logged_in"]:
        st.subheader("Login")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            log_in(login_user.strip(), login_pass)

        st.subheader("Or Sign up")
        su_user = st.text_input("Choose username", key="su_user")
        su_pass = st.text_input("Choose password", type="password", key="su_pass")
        if st.button("Sign up"):
            if su_user.strip() == "" or su_pass == "":
                st.error("Provide username and password.")
            else:
                sign_up(su_user.strip(), su_pass)

        st.info("Your data is stored locally in this folder. Not secure for production use.")
    else:
        st.write(f"Logged in as **{st.session_state['username']}**")
        if st.button("Logout"):
            log_out()

# If not logged in, show a friendly landing page
if not st.session_state["logged_in"]:
    st.markdown("""
    # 💰 Expense Tracker
    Please sign up or log in from the left sidebar to manage your expenses.
    
    Features:
    - Add / Edit / Delete expenses
    - Monthly savings progress bar
    - Category pie chart
    - Auto-sort by date
    - Dark / Light theme
    - Monthly summary PDF download
    """)
    st.stop()

username = st.session_state["username"]
init_user_file(username)

# Top area
st.header(f"💰 Expense Tracker — {username}")

col1, col2 = st.columns([2, 1])
with col2:
    salary = st.number_input("Monthly Salary (₹)", min_value=0.0, format="%.2f", key="salary_input")
    selected_year = st.selectbox("Year", options=sorted(list(range(2020, datetime.now().year + 2))), index=sorted(list(range(2020, datetime.now().year + 2))).index(datetime.now().year))
    selected_month = st.selectbox("Month", options=list(range(1,13)), index=datetime.now().month - 1)
with col1:
    st.markdown("### ➕ Add an expense")
    with st.form("add_expense_form", clear_on_submit=True):
        d = st.date_input("Date", value=datetime.now().date())
        amt = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
        cat = st.text_input("Category", value="General")
        desc = st.text_area("Description (optional)", value="")
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            add_expense(username, d, amt, cat, desc)
            st.success(f"Added ₹{amt:.2f} - {cat}")

# Load data and sort by date (newest first)
df_all = read_user_expenses(username)
if not df_all.empty:
    df_all["Date"] = pd.to_datetime(df_all["Date"]).dt.date
    df_all = df_all.sort_values("Date", ascending=False).reset_index(drop=True)
else:
    df_all = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])

# Filter for selected month/year
df_all["Date_dt"] = pd.to_datetime(df_all["Date"])
df_month = df_all[(df_all["Date_dt"].dt.year == int(selected_year)) & (df_all["Date_dt"].dt.month == int(selected_month))].copy()
df_month = df_month.drop(columns=["Date_dt"])

# Show expenses list (auto-sorted)
st.subheader("📜 All Expenses (Newest first)")
if df_all.empty:
    st.info("No expenses yet. Add one above.")
else:
    for i, row in df_all.iterrows():
        with st.expander(f"{row['Date']} | ₹{row['Amount']} - {row['Category']}"):
            st.write(f"**Description:** {row['Description']}")
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"✏️ Edit {i}", key=f"edit_{i}"):
                    with st.form(f"edit_form_{i}"):
                        new_date = st.date_input("Date", value=pd.to_datetime(row['Date']).date())
                        new_amount = st.number_input("Amount", value=float(row['Amount']), min_value=0.0, format="%.2f")
                        new_category = st.text_input("Category", value=row['Category'])
                        new_description = st.text_area("Description", value=row['Description'])
                        save = st.form_submit_button("Save")
                        if save:
                            edit_expense(username, i, new_date, new_amount, new_category, new_description)
                            st.success("Saved.")
                            st.experimental_rerun()
            with c2:
                if st.button(f"🗑️ Delete {i}", key=f"del_{i}"):
                    delete_expense(username, i)
                    st.warning("Deleted.")
                    st.experimental_rerun()

# Monthly / overall summaries on the right
st.sidebar.subheader("Quick Summary")
total_all = df_all["Amount"].sum() if not df_all.empty else 0.0
st.sidebar.write(f"Total expenses (all time): ₹{total_all:.2f}")

total_month = df_month["Amount"].sum() if not df_month.empty else 0.0
st.sidebar.write(f"Total for {selected_month}/{selected_year}: ₹{total_month:.2f}")

# Savings progress bar for the selected month
st.subheader(f"📈 Monthly Savings - {selected_month}/{selected_year}")
if salary > 0:
    balance = salary - total_month
    # percent saved = remaining / salary *100
    percent_saved = max(0.0, min(100.0, (balance / salary) * 100))
    st.write(f"Salary: ₹{salary:.2f}  |  Spent this month: ₹{total_month:.2f}  |  Remaining: ₹{balance:.2f}")
    st.progress(int(percent_saved))
    # Alerts for 100 INR thresholds
    if balance < 0:
        st.error("❌ You have exceeded your salary for this month!")
    elif balance <= 100:
        st.warning(f"⚠️ Only ₹{balance:.2f} left. Try to save at least ₹100 this month.")
    elif balance < 100:
        # (this branch will be covered by previous, but kept for clarity)
        st.error("⚠️ You should save at least ₹100 this month.")
else:
    st.info("Set your monthly salary on the sidebar to see savings progress.")

# Category pie chart for the selected month (or all if empty)
st.subheader("📊 Category Breakdown (Selected month)")
if df_month.empty:
    st.info("No expenses in this month to chart.")
else:
    cat_sum = df_month.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6,4))
    ax.pie(cat_sum.values, labels=cat_sum.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

# Auto-sort: already sorted when displayed and saved

# PDF Export for selected month
st.subheader("📄 Monthly Summary PDF")
if df_month.empty:
    st.info("No transactions for selected month to generate PDF.")
else:
    try:
        pdf_bytes = create_month_summary_pdf(username, df_month, selected_year, selected_month, salary if salary > 0 else None)
        b64 = base64.b64encode(pdf_bytes).decode()
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{username}_summary_{selected_year}_{selected_month}_{now}.pdf"
        st.download_button("Download PDF Summary", data=pdf_bytes, file_name=filename, mime="application/pdf")
    except RuntimeError as e:
        st.error(str(e))
        st.write("To enable PDF export, install reportlab: `pip install reportlab`")

# Small footer
st.markdown("---")
st.caption("Note: This app stores data locally in CSV files inside the app folder. For real-world use, migrate to a secure database and implement proper password hashing/salting and encryption.")

