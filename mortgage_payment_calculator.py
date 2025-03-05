import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.image("image.png")
st.title("Mortgage Payment Calculator")
st.write("### Enter Loan Details")

col1, col2 = st.columns(2)

# User Inputs
home_price = col1.number_input("Home Price ($)", min_value=0, value=500000)
down_payment = col1.number_input("Down Payment ($)", min_value=0, value=100000)
annual_interest_rate = col2.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.5)
loan_duration_years = col2.number_input("Loan Term (Years)", min_value=1, value=30)

# Loan Calculations
loan_principal = home_price - down_payment
monthly_interest_rate = (annual_interest_rate / 100) / 12
total_payments = loan_duration_years * 12

if loan_principal <= 0:
    st.error("Loan principal must be greater than zero! Adjust Home Price or Down Payment.")
    st.stop()

if monthly_interest_rate == 0:
    # If interest rate is 0%, divide loan amount evenly over the term
    monthly_payment = loan_principal / total_payments
else:
    # Standard mortgage formula
    monthly_payment = (
        loan_principal
        * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments)
        / ((1 + monthly_interest_rate) ** total_payments - 1)
    )

# Overall Payment Breakdown
total_repayment = monthly_payment * total_payments
total_interest_paid = total_repayment - loan_principal

st.write("### Mortgage Summary")

col1, col2, col3 = st.columns(3)

col1.metric(label="Monthly Payment", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Repayment", value=f"${total_repayment:,.0f}")
col3.metric(label="Total Interest Paid", value=f"${total_interest_paid:,.0f}")

# Generate Payment Schedule
payment_schedule = []
remaining_balance = loan_principal

for month in range(1, total_payments + 1):
    if monthly_interest_rate == 0:
        # No interest, just straight principal reduction
        principal_payment = loan_principal / total_payments
        interest_payment = 0
    else:
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment

    remaining_balance -= principal_payment
    year_number = math.ceil(month / 12)
    payment_schedule.append([month, monthly_payment, principal_payment, interest_payment, remaining_balance, year_number])

df_schedule = pd.DataFrame(
    payment_schedule,
    columns=["Month", "Monthly Payment", "Principal Paid", "Interest Paid", "Remaining Balance", "Year"]
)

st.write("#### Remaining Loan Balance Over Time")
yearly_balance = df_schedule.groupby("Year")["Remaining Balance"].min()
st.line_chart(yearly_balance, color="#ff725e")