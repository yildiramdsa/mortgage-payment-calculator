import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Mortgage Payment Calculator")
st.write("### Enter Loan Details")

col1, col2 = st.columns(2)

home_price = col1.number_input("Home Price ($)", min_value=0, value=0)
down_payment = col1.number_input("Down Payment ($)", min_value=0, value=0)
annual_interest_rate = col2.number_input("Annual Interest Rate (%)", min_value=0.0, value=0.0)
loan_duration_years = col2.number_input("Loan Term (Years)", min_value=1, value=1)