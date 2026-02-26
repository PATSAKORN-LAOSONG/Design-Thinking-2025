import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="ระบบประเมินความดัน", layout="centered")

st.title("🩺 ระบบประเมินระดับความดันโลหิต")
st.write("กรอกค่าความดันโลหิต ระบบจะประเมินระดับตามเกณฑ์จากไฟล์ CSV")

# ===============================
# โหลดไฟล์ CSV
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("table_1.csv")

    # ลบช่องว่างหัวคอลัมน์
    df.columns = df.columns.str.strip()

    return df

df = load_data()

# ===============================
# ตรวจสอบคอลัมน์
# ===============================
if len(df.columns) < 3:
    st.error("ไฟล์ CSV ต้องมีอย่างน้อย 3 คอลัมน์")
    st.stop()

category_col = df.columns[0]
sys_col = df.columns[1]
dia_col = df.columns[2]

# ===============================
# ฟังก์ชันแปลงช่วงค่า
# ===============================
def parse_range(value):
    if pd.isna(value):
        return (np.nan, np.nan)

    value = str(value).strip()

    try:
        if ">=" in value:
            num = int(value.replace(">=", "").strip())
            return (num, float("inf"))

        if "-" in value:
            low, high = value.split("-")
            return (int(low.strip()), int(high.strip()))

        if "<" in value:
            num = int(value.replace("<", "").strip())
            return (0, num - 1)

    except:
        return (np.nan, np.nan)

    return (np.nan, np.nan)

# ===============================
# สร้างช่วงตัวเลข
# ===============================
df[["Sys_min", "Sys_max"]] = df[sys_col].apply(lambda x: pd.Series(parse_range(x)))
df[["Dia_min", "Dia_max"]] = df[dia_col].apply(lambda x: pd.Series(parse_range(x)))

# ===============================
# รับค่าผู้ใช้
# ===============================
sys = st.number_input("ค่า SYSTOLIC (ตัวบน)", 0, 300, 120)
dia = st.number_input("ค่า DIASTOLIC (ตัวล่าง)", 0, 200, 80)

# ===============================
# ตรวจสอบระดับ
# ===============================
if st.button("🔍 ตรวจสอบระดับความดัน"):

    st.subheader("📊 ผลการประเมิน")

    if sys >= 180 or dia >= 120:
        result = "Hypertensive Crisis"
        st.error("⚠️ ระดับอันตรายมาก ควรพบแพทย์ทันที")

    elif sys >= 140 or dia >= 90:
        result = "Hypertension Stage 2"
        st.error("⚠️ ความดันสูงระดับ 2 ควรปรึกษาแพทย์")

    elif sys >= 130 or dia >= 80:
        result = "Hypertension Stage 1"
        st.warning("ควรควบคุมอาหารและติดตามอาการ")

    elif sys >= 120 and dia < 80:
        result = "Elevated"
        st.info("ความดันเริ่มสูง ควรปรับพฤติกรรม")

    else:
        result = "Normal"
        st.success("อยู่ในระดับปกติ")

    st.success(f"ระดับความดันของคุณคือ: **{result}**")
