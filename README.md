# 🏦 Banking System – Streamlit Mini Project

A simple **Banking System web application** developed using **Python and Streamlit**. The project simulates basic banking operations such as account creation, secure login, deposits, withdrawals, money transfers, transaction history, and PIN management.

## 📌 Project Overview

This project demonstrates how fundamental Python programming concepts can be combined to create a real-world banking application.

The application provides a simple and interactive web interface using Streamlit and stores account and transaction information using SQLite.

## ✨ Features

* 🏦 Create a new bank account
* 🔐 Login using Account Number and PIN
* 💰 Check account balance
* ➕ Deposit money
* ➖ Withdraw money
* 🔄 Transfer money between accounts
* 📜 View transaction history
* 🔑 Change account PIN
* 🚪 Logout
* 📥 Download transaction history as CSV
* 🔒 PINs are stored using SHA-256 hashing
* 🗄️ SQLite database for account and transaction storage
* 📊 Interactive Streamlit dashboard

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **SQLite**
* **Pandas**
* **Hashlib**
* **Random**
* **Datetime**

## 📂 Project Structure

```text
banking-system-streamlit/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

The SQLite database is automatically created when the application runs.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Rajkumar200526/banking-system-streamlit.git
```

### 2. Navigate to the project folder

```bash
cd banking-system-streamlit
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

Usually the local URL is:

```text
http://localhost:8501
```

## 🚀 How to Use

### Step 1 – Create an Account

Enter:

* Full Name
* Phone Number
* PIN
* Confirm PIN

After successful registration, the system generates a unique account number.

### Step 2 – Login

Use:

* Account Number
* PIN

to access the banking dashboard.

### Step 3 – Perform Banking Operations

After logging in, users can:

1. Check Balance
2. Deposit Money
3. Withdraw Money
4. Transfer Money
5. View Transaction History
6. Change PIN
7. Logout

## 💾 Database

The application uses **SQLite** to store:

### Accounts

* Account Number
* Name
* Phone Number
* PIN Hash
* Balance
* Account Creation Date

### Transactions

* Transaction ID
* Account Number
* Transaction Type
* Amount
* Related Account
* Description
* Date and Time

The database file is generated automatically when the application starts.

## 🔐 Security

The project does not store PINs directly as plain text.

PINs are converted into a SHA-256 hash before being stored in the database.

> **Note:** This is an educational mini project and is not intended for use as a production banking application.

## ☁️ Deployment

This application can be deployed using **Streamlit Community Cloud**.

Basic deployment steps:

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect the GitHub repository.
4. Select `app.py` as the main application file.
5. Deploy the application.

## 🎯 Project Objective

The main objective of this project is to combine Python concepts such as:

* Variables and data types
* Conditional statements
* Loops
* Functions
* Lists and dictionaries
* String operations
* Modules
* Database operations

into a functional real-world application.

## 🌍 Real-World Connection

The project demonstrates a simplified version of operations commonly found in banking applications, including:

* Account management
* Authentication
* Balance management
* Money transactions
* Transaction records

## 👨‍💻 Author

**A. Raj Kumar**

B.Tech – Computer Science and Engineering (AI & ML)

GitHub:
https://github.com/Rajkumar200526

## 📜 License

This project was created for educational and academic purposes.
