# taxi_tracker.py

import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Taxi Income Tracker", layout="centered")

st.title("🚖 บันทึกรายได้คนขับ Taxi App")

# Load หรือสร้างไฟล์ข้อมูล
if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv")
else:
    df = pd.DataFrame(columns=["วันที่", "รายได้", "ค่าน้ำมัน", "ค่าอาหาร", "กำไร"])

# --- ฟอร์มกรอกข้อมูล ---
with st.form("income_form"):
    date = st.date_input("📅 วันที่", datetime.today())
    income = st.number_input("💰 รายได้วันนี้ (บาท)", min_value=0)
    fuel = st.number_input("⛽ ค่าน้ำมัน (บาท)", min_value=0)
    food = st.number_input("🍜 ค่าอาหาร/อื่นๆ (บาท)", min_value=0)
    submitted = st.form_submit_button("บันทึกข้อมูล")

    if submitted:
        profit = income - fuel - food
        new_data = pd.DataFrame([[date, income, fuel, food, profit]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv("data.csv", index=False)
        st.success("✅ บันทึกเรียบร้อยแล้ว!")

# --- สรุปข้อมูล ---
if not df.empty:
    st.subheader("📊 สรุปรายได้ล่าสุด")
    st.dataframe(df.tail(7))

    st.metric("💵 รายได้รวม", f"{df['รายได้'].sum():,.0f} บาท")
    st.metric("🧾 ค่าใช้จ่ายรวม", f"{df['ค่าน้ำมัน'].sum() + df['ค่าอาหาร'].sum():,.0f} บาท")
    st.metric("📈 กำไรสุทธิรวม", f"{df['กำไร'].sum():,.0f} บาท")

    # กราฟ
    st.line_chart(df.set_index("วันที่")[["รายได้", "กำไร"]])
