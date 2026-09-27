import streamlit as st
import sqlite3
import random
import hashlib
from datetime import datetime
import pandas as pd

# ============================================================
# BANKING SYSTEM - STREAMLIT MINI PROJECT
# Single-file application
# ============================================================

st.set_page_config(
    page_title="Banking System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_NAME = "banking_system.db"


# ------------------------- DATABASE --------------------------

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            pin_hash TEXT NOT NULL,
            balance REAL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL DEFAULT 0,
            related_account TEXT,
            description TEXT,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_database()


# ------------------------- HELPERS ---------------------------

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


def generate_account_number():
    conn = get_connection()
    while True:
        number = str(random.randint(1000000000, 9999999999))
        exists = conn.execute(
            "SELECT account_number FROM accounts WHERE account_number = ?",
            (number,)
        ).fetchone()
        if not exists:
            conn.close()
            return number


def get_account(account_number):
    conn = get_connection()
    account = conn.execute(
        "SELECT * FROM accounts WHERE account_number = ?",
        (account_number,)
    ).fetchone()
    conn.close()
    return account


def add_transaction(account_number, transaction_type, amount=0,
                    related_account=None, description=""):
    conn = get_connection()
    conn.execute("""
        INSERT INTO transactions
        (account_number, transaction_type, amount, related_account, description, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        account_number,
        transaction_type,
        amount,
        related_account,
        description,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()


def get_transactions(account_number):
    conn = get_connection()
    rows = conn.execute("""
        SELECT timestamp, transaction_type, amount, related_account, description
        FROM transactions
        WHERE account_number = ?
        ORDER BY id DESC
    """, (account_number,)).fetchall()
    conn.close()
    return rows


def format_currency(value):
    return f"₹{value:,.2f}"


# ------------------------- SESSION ---------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account_number" not in st.session_state:
    st.session_state.account_number = None


def logout():
    st.session_state.logged_in = False
    st.session_state.account_number = None
    st.rerun()


# ------------------------- CSS -------------------------------

st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        margin-bottom: 30px;
    }

    .bank-card {
        padding: 25px;
        border-radius: 18px;
        background: linear-gradient(135deg, #0f172a, #1e3a8a);
        color: white;
        margin-bottom: 20px;
    }

    .account-number {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .balance {
        font-size: 34px;
        font-weight: 800;
        margin-top: 10px;
    }

    div[data-testid="stMetric"] {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 12px;
    }

    .info-box {
        padding: 15px;
        border-radius: 12px;
        background-color: #f1f5f9;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# LOGIN / CREATE ACCOUNT
# ============================================================

if not st.session_state.logged_in:

    st.markdown('<div class="main-title">🏦 Banking System</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Python + Streamlit Mini Project</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["🔐 Login", "➕ Create Account"])

    # ---------------- LOGIN ----------------

    with tab1:
        st.subheader("Login to Your Account")

        with st.form("login_form"):
            account_number = st.text_input(
                "Account Number",
                placeholder="Enter your 10-digit account number"
            )
            pin = st.text_input(
                "PIN",
                type="password",
                placeholder="Enter your PIN"
            )
            login_button = st.form_submit_button(
                "🔐 Login",
                use_container_width=True
            )

        if login_button:
            account_number = account_number.strip()
            account = get_account(account_number)

            if not account:
                st.error("❌ Account not found. Please check your account number.")
            elif account["pin_hash"] != hash_pin(pin):
                st.error("❌ Incorrect PIN.")
            else:
                st.session_state.logged_in = True
                st.session_state.account_number = account_number
                st.success("✅ Login successful!")
                st.rerun()

        st.info("💡 Create an account first if you are a new user.")

    # ---------------- CREATE ACCOUNT ----------------

    with tab2:
        st.subheader("Create New Bank Account")

        with st.form("create_account_form"):
            name = st.text_input("Full Name")
            phone = st.text_input("Phone Number", max_chars=15)
            pin = st.text_input(
                "Create PIN",
                type="password",
                max_chars=6,
                help="Use a 4-6 digit PIN."
            )
            confirm_pin = st.text_input(
                "Confirm PIN",
                type="password",
                max_chars=6
            )

            create_button = st.form_submit_button(
                "🏦 Create Account",
                use_container_width=True
            )

        if create_button:
            name = name.strip()
            phone = phone.strip()

            if not name:
                st.error("Please enter your name.")
            elif not phone:
                st.error("Please enter your phone number.")
            elif not pin.isdigit() or len(pin) < 4 or len(pin) > 6:
                st.error("PIN must contain 4 to 6 digits.")
            elif pin != confirm_pin:
                st.error("PINs do not match.")
            else:
                account_number = generate_account_number()

                conn = get_connection()
                conn.execute("""
                    INSERT INTO accounts
                    (account_number, name, phone, pin_hash, balance, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    account_number,
                    name,
                    phone,
                    hash_pin(pin),
                    0,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                conn.close()

                add_transaction(
                    account_number,
                    "ACCOUNT_CREATED",
                    0,
                    description="Bank account created"
                )

                st.success("🎉 Account created successfully!")

                st.markdown(
                    f"""
                    <div class="bank-card">
                        <div>YOUR ACCOUNT NUMBER</div>
                        <div class="account-number">{account_number}</div>
                        <br>
                        <div>Account Holder</div>
                        <div style="font-size:22px;font-weight:700;">{name}</div>
                        <br>
                        <div>Initial Balance</div>
                        <div class="balance">₹0.00</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.warning(
                    "⚠️ Save your account number. You will need it to log in."
                )


# ============================================================
# LOGGED-IN DASHBOARD
# ============================================================

else:

    account_number = st.session_state.account_number
    account = get_account(account_number)

    if not account:
        logout()
        st.stop()

    # ---------------- SIDEBAR ----------------

    with st.sidebar:
        st.title("🏦 Banking System")

        st.success(f"Logged in as\n\n**{account['name']}**")

        st.write("**Account Number**")
        st.code(account_number)

        st.divider()

        menu = st.radio(
            "Account Menu",
            [
                "🏠 Dashboard",
                "💰 Deposit",
                "💸 Withdraw",
                "🔄 Transfer",
                "📜 Transaction History",
                "🔑 Change PIN"
            ]
        )

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            logout()

    # ---------------- REFRESH ACCOUNT ----------------

    account = get_account(account_number)

    # ---------------- DASHBOARD ----------------

    if menu == "🏠 Dashboard":

        st.title("🏠 Account Dashboard")

        st.markdown(
            f"""
            <div class="bank-card">
                <div>ACCOUNT HOLDER</div>
                <div style="font-size:28px;font-weight:700;">
                    {account['name']}
                </div>
                <br>
                <div>ACCOUNT NUMBER</div>
                <div class="account-number">{account_number}</div>
                <br>
                <div>AVAILABLE BALANCE</div>
                <div class="balance">{format_currency(account['balance'])}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        transactions = get_transactions(account_number)

        deposits = sum(
            float(t["amount"]) for t in transactions
            if t["transaction_type"] == "DEPOSIT"
        )

        withdrawals = sum(
            float(t["amount"]) for t in transactions
            if t["transaction_type"] == "WITHDRAW"
        )

        transfers_sent = sum(
            float(t["amount"]) for t in transactions
            if t["transaction_type"] == "TRANSFER_SENT"
        )

        col1.metric("Current Balance", format_currency(account["balance"]))
        col2.metric("Total Deposits", format_currency(deposits))
        col3.metric("Total Withdrawals", format_currency(withdrawals))

        st.subheader("📌 Quick Information")

        st.info(
            "Use the sidebar to deposit money, withdraw money, transfer funds, "
            "view your transaction history, or change your PIN."
        )

        if transactions:
            st.subheader("🕐 Recent Activity")

            recent = transactions[:5]

            data = []
            for t in recent:
                data.append({
                    "Date & Time": t["timestamp"],
                    "Type": t["transaction_type"],
                    "Amount": format_currency(t["amount"]),
                    "Related Account": t["related_account"] or "-",
                    "Description": t["description"]
                })

            st.dataframe(
                pd.DataFrame(data),
                use_container_width=True,
                hide_index=True
            )

    # ---------------- DEPOSIT ----------------

    elif menu == "💰 Deposit":

        st.title("💰 Deposit Money")

        st.write(
            f"Current Balance: **{format_currency(account['balance'])}**"
        )

        with st.form("deposit_form"):
            amount = st.number_input(
                "Enter Deposit Amount (₹)",
                min_value=1.0,
                step=100.0,
                format="%.2f"
            )

            deposit_button = st.form_submit_button(
                "➕ Deposit Money",
                use_container_width=True
            )

        if deposit_button:

            if amount <= 0:
                st.error("Deposit amount must be greater than zero.")
            else:
                new_balance = account["balance"] + amount

                conn = get_connection()
                conn.execute(
                    "UPDATE accounts SET balance = ? WHERE account_number = ?",
                    (new_balance, account_number)
                )
                conn.commit()
                conn.close()

                add_transaction(
                    account_number,
                    "DEPOSIT",
                    amount,
                    description="Cash deposited"
                )

                st.success(
                    f"✅ {format_currency(amount)} deposited successfully!"
                )
                st.info(
                    f"New Balance: **{format_currency(new_balance)}**"
                )
                st.rerun()

    # ---------------- WITHDRAW ----------------

    elif menu == "💸 Withdraw":

        st.title("💸 Withdraw Money")

        st.write(
            f"Available Balance: **{format_currency(account['balance'])}**"
        )

        with st.form("withdraw_form"):
            amount = st.number_input(
                "Enter Withdrawal Amount (₹)",
                min_value=1.0,
                step=100.0,
                format="%.2f"
            )

            withdraw_button = st.form_submit_button(
                "➖ Withdraw Money",
                use_container_width=True
            )

        if withdraw_button:

            if amount <= 0:
                st.error("Withdrawal amount must be greater than zero.")
            elif amount > account["balance"]:
                st.error(
                    "❌ Insufficient balance. Withdrawal cannot be completed."
                )
            else:
                new_balance = account["balance"] - amount

                conn = get_connection()
                conn.execute(
                    "UPDATE accounts SET balance = ? WHERE account_number = ?",
                    (new_balance, account_number)
                )
                conn.commit()
                conn.close()

                add_transaction(
                    account_number,
                    "WITHDRAW",
                    amount,
                    description="Cash withdrawn"
                )

                st.success(
                    f"✅ {format_currency(amount)} withdrawn successfully!"
                )
                st.info(
                    f"Remaining Balance: **{format_currency(new_balance)}**"
                )
                st.rerun()

    # ---------------- TRANSFER ----------------

    elif menu == "🔄 Transfer":

        st.title("🔄 Transfer Money")

        st.write(
            f"Your Balance: **{format_currency(account['balance'])}**"
        )

        with st.form("transfer_form"):
            receiver = st.text_input(
                "Receiver Account Number",
                placeholder="Enter receiver's account number"
            )

            amount = st.number_input(
                "Transfer Amount (₹)",
                min_value=1.0,
                step=100.0,
                format="%.2f"
            )

            transfer_button = st.form_submit_button(
                "🔄 Transfer Money",
                use_container_width=True
            )

        if transfer_button:

            receiver = receiver.strip()
            receiver_account = get_account(receiver)

            if not receiver:
                st.error("Please enter receiver account number.")
            elif receiver == account_number:
                st.error("❌ You cannot transfer money to your own account.")
            elif not receiver_account:
                st.error("❌ Receiver account not found.")
            elif amount <= 0:
                st.error("Transfer amount must be greater than zero.")
            elif amount > account["balance"]:
                st.error("❌ Insufficient balance.")
            else:

                sender_new_balance = account["balance"] - amount
                receiver_new_balance = receiver_account["balance"] + amount

                conn = get_connection()

                # Update sender
                conn.execute(
                    "UPDATE accounts SET balance = ? WHERE account_number = ?",
                    (sender_new_balance, account_number)
                )

                # Update receiver
                conn.execute(
                    "UPDATE accounts SET balance = ? WHERE account_number = ?",
                    (receiver_new_balance, receiver)
                )

                conn.commit()
                conn.close()

                add_transaction(
                    account_number,
                    "TRANSFER_SENT",
                    amount,
                    related_account=receiver,
                    description=f"Transfer sent to {receiver_account['name']}"
                )

                add_transaction(
                    receiver,
                    "TRANSFER_RECEIVED",
                    amount,
                    related_account=account_number,
                    description=f"Transfer received from {account['name']}"
                )

                st.success(
                    f"✅ {format_currency(amount)} transferred successfully!"
                )

                st.info(
                    f"New Balance: **{format_currency(sender_new_balance)}**"
                )

                st.rerun()

    # ---------------- TRANSACTION HISTORY ----------------

    elif menu == "📜 Transaction History":

        st.title("📜 Transaction History")

        transactions = get_transactions(account_number)

        if not transactions:
            st.info("No transactions found.")
        else:

            data = []

            for t in transactions:
                data.append({
                    "Date & Time": t["timestamp"],
                    "Transaction Type": t["transaction_type"],
                    "Amount": format_currency(t["amount"]),
                    "Related Account": t["related_account"] or "-",
                    "Description": t["description"]
                })

            df = pd.DataFrame(data)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇️ Download Transaction History",
                data=csv,
                file_name=f"{account_number}_transactions.csv",
                mime="text/csv",
                use_container_width=True
            )

    # ---------------- CHANGE PIN ----------------

    elif menu == "🔑 Change PIN":

        st.title("🔑 Change PIN")

        with st.form("change_pin_form"):

            old_pin = st.text_input(
                "Current PIN",
                type="password",
                max_chars=6
            )

            new_pin = st.text_input(
                "New PIN",
                type="password",
                max_chars=6
            )

            confirm_new_pin = st.text_input(
                "Confirm New PIN",
                type="password",
                max_chars=6
            )

            change_button = st.form_submit_button(
                "🔑 Change PIN",
                use_container_width=True
            )

        if change_button:

            if account["pin_hash"] != hash_pin(old_pin):
                st.error("❌ Current PIN is incorrect.")
            elif not new_pin.isdigit() or len(new_pin) < 4 or len(new_pin) > 6:
                st.error("New PIN must contain 4 to 6 digits.")
            elif new_pin != confirm_new_pin:
                st.error("New PINs do not match.")
            elif new_pin == old_pin:
                st.error("New PIN must be different from the old PIN.")
            else:

                conn = get_connection()
                conn.execute(
                    "UPDATE accounts SET pin_hash = ? WHERE account_number = ?",
                    (hash_pin(new_pin), account_number)
                )
                conn.commit()
                conn.close()

                add_transaction(
                    account_number,
                    "PIN_CHANGED",
                    0,
                    description="Account PIN changed"
                )

                st.success("✅ PIN changed successfully!")

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.caption(
    "Banking System Mini Project | Built with Python, Streamlit, SQLite, "
    "Random, Datetime, Lists, Dictionaries, Functions and Conditional Logic"
)
