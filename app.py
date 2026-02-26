import streamlit as st
import pandas as pd

st.title("🩺 ระบบประเมินระดับความดันโลหิต")

@st.cache_data
def load_data():
    df = pd.read_csv("table_1.csv")
    
    # ลบช่องว่างหัวคอลัมน์
    df.columns = df.columns.str.strip()
    
    return df

df = load_data()

# แสดงชื่อคอลัมน์ (debug ได้เลย)
# st.write(df.columns)

# -----------------------
# ตรวจสอบว่ามีคอลัมน์อะไรบ้าง
# -----------------------
required_cols = df.columns.tolist()

if len(required_cols) < 3:
    st.error("ไฟล์ CSV ต้องมีอย่างน้อย 3 คอลัมน์")
    st.stop()

category_col = required_cols[0]
sys_col = required_cols[1]
dia_col = required_cols[2]

# -----------------------
# แปลงช่วงค่า
# -----------------------
def parse_range(value):
    value = str(value).strip()

    if ">=" in value:
        num = int(value.replace(">=", "").strip())
        return (num, float("inf"))

    if "-" in value:
        low, high = value.split("-")
        return (int(low.strip()), int(high.strip()))

    if "<" in value:
        num = int(value.replace("<", "").strip())
        return (0, num - 1)

    return (None, None)

df[["Sys_min", "Sys_max"]] = df[sys_col].apply(lambda x: pd.Series(parse_range(x)))
df[["Dia_min", "Dia_max"]] = df[dia_col].apply(lambda x: pd.Series(parse_range(x)))

# -----------------------
# รับค่าผู้ใช้
# -----------------------
sys = st.number_input("ค่า SYSTOLIC (ตัวบน)", 0, 300, 120)
dia = st.number_input("ค่า DIASTOLIC (ตัวล่าง)", 0, 200, 80)

if st.button("🔍 ตรวจสอบระดับความดัน"):
    
    matched_rows = []

    for _, row in df.iterrows():
        sys_match = row["Sys_min"] <= sys <= row["Sys_max"]
        dia_match = row["Dia_min"] <= dia <= row["Dia_max"]

        if sys_match or dia_match:
            matched_rows.append(row)

    if matched_rows:
        result = matched_rows[-1][category_col]

        st.subheader("📊 ผลการประเมิน")
        st.success(f"ระดับความดันของคุณคือ: **{result}**")

        if "CRISIS" in str(result).upper():
            st.error("⚠️ ระดับอันตราย ควรพบแพทย์ทันที")
        elif "STAGE 2" in str(result).upper():
            st.error("⚠️ ความดันสูงมาก ควรปรึกษาแพทย์")
        elif "STAGE 1" in str(result).upper():
            st.warning("ควรควบคุมอาหารและติดตามอาการ")
        else:
            st.info("อยู่ในระดับปกติหรือใกล้เคียงปกติ")
    else:
        st.warning("ไม่พบระดับที่ตรงกับข้อมูล")
