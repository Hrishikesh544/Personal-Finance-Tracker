import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import os
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Personal Finance Tracker", layout="wide")

# --- DATA PERSISTENCE ---
DATA_FILE = "finance_master.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    return pd.DataFrame(columns=['ID', 'Date', 'Account', 'Category', 'Description', 'Amount', 'Type', 'Is_Recurring'])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# --- SIDEBAR: INPUT & CONTROLS ---
st.sidebar.header("💳 Financial Input")

with st.sidebar.form("entry_form", clear_on_submit=True):
    date = st.date_input("Transaction Date", datetime.date.today())
    t_type = st.selectbox("Type", ["Expense", "Income"])
    account = st.selectbox("Account/Wallet", ["Bank Account", "Cash", "Credit Card", "Digital Wallet"])
    category = st.selectbox("Category", ["Food", "Rent", "Travel", "Utilities", "Shopping", "Salary", "Investment", "EMI/Subscription", "Other"])
    desc = st.text_input("Merchant/Description")
    amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
    recurring = st.checkbox("Is this a recurring payment?")
    submit = st.form_submit_button("Log Transaction")

if submit and amount > 0:
    # Generate a unique ID based on timestamp
    new_id = int(datetime.datetime.now().timestamp())
    new_row = pd.DataFrame([[new_id, pd.to_datetime(date), account, category, desc, amount, t_type, recurring]], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    st.sidebar.success("Transaction Logged!")
    st.rerun()

# --- NEW: DELETE & ACCOUNT MANAGEMENT ---
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Data Management")

if not df.empty:
    # 1. Manual Record Deletion
    st.sidebar.subheader("🗑️ Delete Record")
    id_to_delete = st.sidebar.number_input("Enter ID to Remove", min_value=0, step=1)
    if st.sidebar.button("Delete Selected ID"):
        if id_to_delete in df['ID'].values:
            df = df[df['ID'] != id_to_delete]
            save_data(df)
            st.sidebar.warning(f"ID {id_to_delete} removed.")
            st.rerun()
        else:
            st.sidebar.error("ID not found in logs.")

    # 2. Account-Specific Views
    st.sidebar.subheader("📂 Account Filter")
    view_option = st.sidebar.multiselect("Select Accounts to View", 
                                        options=df['Account'].unique(),
                                        default=df['Account'].unique())
    display_df = df[df['Account'].isin(view_option)]
else:
    display_df = df

if st.sidebar.button("🔥 Factory Reset (Delete All)"):
    if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
    st.rerun()

# --- DASHBOARD LOGIC ---
st.title("📊 Financial Intelligence Dashboard")

if df.empty:
    st.info("No data found. Start logging transactions in the sidebar.")
else:
    # A. KEY METRICS (UPDATED WITH ARROWS)
    curr_month = datetime.date.today().month
    last_month = curr_month - 1 if curr_month > 1 else 12
    
    # Filter data for current vs last month
    m_df = display_df[display_df['Date'].dt.month == curr_month]
    last_m_df = display_df[display_df['Date'].dt.month == last_month]
    
    # Calculate Current Totals
    total_income = m_df[m_df['Type'] == 'Income']['Amount'].sum()
    total_expense = m_df[m_df['Type'] == 'Expense']['Amount'].sum()

    # Calculate Last Month Totals
    last_income = last_m_df[last_m_df['Type'] == 'Income']['Amount'].sum()
    last_expense = last_m_df[last_m_df['Type'] == 'Expense']['Amount'].sum()

    # Calculate Differences (Deltas)
    income_delta = total_income - last_income
    expense_delta = total_expense - last_expense
    
    col1, col2, col3 = st.columns(3)
    
    # Income: Normal Color (Green = Up, Red = Down)
    col1.metric("Selected Account Income", f"₹{total_income:,.0f}", delta=f"{income_delta:,.0f}", delta_color="normal")
    
    # Expense: Inverse Color (Red = Up, Green = Down)
    col2.metric("Selected Account Expense", f"₹{total_expense:,.0f}", delta=f"{expense_delta:,.0f}", delta_color="inverse")
    
    col3.metric("Net Surplus", f"₹{(total_income - total_expense):,.0f}")

    # B. MULTI-ACCOUNT VIEW (Visual)
    st.markdown("---")
    st.subheader("🏦 Consolidated Bank & Wallet Balances")
    
    # Calculate balance per account: Income - Expense
    acc_logic = display_df.copy()
    acc_logic['Math_Amount'] = np.where(acc_logic['Type'] == 'Income', acc_logic['Amount'], -acc_logic['Amount'])
    balance_df = acc_logic.groupby('Account')['Math_Amount'].sum().reset_index()
    
    fig_acc = px.bar(balance_df, x='Account', y='Math_Amount', 
                     color='Math_Amount', color_continuous_scale='RdYlGn',
                     labels={'Math_Amount': 'Current Balance (₹)'})
    st.plotly_chart(fig_acc, use_container_width=True)

    # C. RECENT LOGS (With ID for Deletion)
    st.markdown("---")
    st.subheader("📑 Transaction Logs")
    st.write("Reference the **ID** column to manually delete a record in the sidebar.")
    st.dataframe(display_df.sort_values(by='Date', ascending=False), use_container_width=True)

    # D. CATEGORY ANALYTICS
    st.markdown("---")
    g1, g2 = st.columns(2)
    with g1:
        st.write("**Expense Distribution**")
        fig_pie = px.pie(display_df[display_df['Type']=='Expense'], values='Amount', names='Category', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    with g2:
        st.write("**Cash Flow Trend**")
        trend = display_df.groupby(['Date', 'Type'])['Amount'].sum().reset_index()
        fig_area = px.area(trend, x='Date', y='Amount', color='Type', markers=True)
        st.plotly_chart(fig_area, use_container_width=True)