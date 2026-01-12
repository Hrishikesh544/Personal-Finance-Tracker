#  Financial Intelligence Dashboard

A comprehensive, full-stack Personal Finance Intelligence tool built with **Python**, **Streamlit**, and **Pandas**. This application provides real-time insights into spending habits, income trends, and multi-account balances without the need for a complex database setup.

##  Key Features

### 1. Income & Expense Tracking
- **Manual Logging:** Add transactions with specific categories, dates, and descriptions.
- **Data Persistence:** All records are saved locally in `finance_master.csv` for persistent storage across sessions.
- **Unique ID Management:** Every transaction is assigned a unique Unix-timestamp-based ID for precise tracking.

### 2. Multi-Account Support
- **Account-Specific Views:** Switch between or consolidate views for **Bank Accounts**, **Cash**, **Credit Cards**, and **Digital Wallets**.
- **Consolidated Balance:** A real-time bar chart calculates the net surplus across all accounts using signed-amount logic.

### 3. Visual Analytics & Intelligence
- **Expense Distribution:** Interactive **Pie Charts** (Plotly) to visualize where money is going category-wise.
- **Cash Flow Trends:** **Area Charts** to track the relationship between income and spending over time.
- **Month-over-Month (MoM) Metrics:** - 🟢 **Income:** Green rising arrows for increased earnings.
  - 🔴 **Expenses:** Red rising arrows for increased spending (using inverse delta logic).

### 4. Data Management
- **Manual Deletion:** Remove specific records by referencing their unique ID in the management sidebar.
- **Factory Reset:** A one-click option to clear all financial data and start fresh.
- **Advanced Filtering:** Multi-select filters to isolate specific account data instantly.

##  Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/) (Web Framework)
- **Data Engine:** [Pandas](https://pandas.pydata.org/) (Data Manipulation)
- **Visuals:** [Plotly](https://plotly.com/python/) (Interactive Graphing)
- **Storage:** CSV (Local File I/O)
- **Math:** [NumPy](https://numpy.org/) (Array Logic)

##  Installation & Setup

Ensure you have Python installed, then follow these steps:

1. **Clone the repository:**
  ```bash
   git clone [https://github.com/Hrishikesh544/financial-intelligence.git](https://github.com/Hrishikesh544/financial-intelligence.git)
   cd financial-intelligence
  ```

2. **Install Dependencies:**
   ```bash
   pip install streamlit pandas plotly numpy
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
  ```
