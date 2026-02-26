import streamlit as st
import pandas as pd

st.set_page_config(page_title="ระบบประเมินระดับความดันโลหิต", page_icon="🩺")

st.title("🩺 ระบบประเมินระดับความดันโลหิต")
st.write("กรอกค่าความดันโลหิตของคุณ ระบบจะประเมินระดับตามเกณฑ์จากไฟล์ CSV")

df = pd.read_csv("table_1.csv")

# จัดลำดับความรุนแรง (มาก → น้อย)
severity_order = {
    "EMERGENCY": 6,
    "SEVERE": 5,
    "STAGE 2": 4,
    "STAGE 1": 3,
    "ELEVATED": 2,
    "NORMAL": 1
}

thai_translation = {
    "NORMAL": "ระดับปกติ",
    "ELEVATED": "ระดับค่อนข้างสูง",
    "STAGE 1": "ความดันโลหิตสูง ระยะที่ 1",
    "STAGE 2": "ความดันโลหิตสูง ระยะที่ 2",
    "SEVERE": "ภาวะความดันสูงรุนแรง",
    "EMERGENCY": "ภาวะฉุกเฉิน ควรพบแพทย์ทันที"
}

def parse_condition(text):
    text = str(text).upper().strip()

    if "LESS THAN" in text:
        num = int(text.split()[-1])
        return (None, num, "<")

    elif "-" in text:
        low, high = text.split("-")
        return (int(low.strip()), int(high.strip()), "range")

    elif "OR HIGHER" in text:
        num = int(text.split()[0])
        return (num, None, ">=")

    elif "HIGHER THAN" in text:
        num = int(text.split()[-1])
        return (num, None, ">")

    return (None, None, None)


def check_value(value, parsed):
    low, high, mode = parsed

    if mode == "<":
        return value < high
    elif mode == "range":
        return low <= value <= high
    elif mode == ">=":
        return value >= low
    elif mode == ">":
        return value > low
    return False


# เรียงตามความรุนแรง
df["severity"] = df["BLOOD PRESSURE CATEGORY"].map(severity_order)
df = df.sort_values(by="severity", ascending=False)

systolic = st.number_input("ค่า SYSTOLIC (ตัวบน)", min_value=0)
diastolic = st.number_input("ค่า DIASTOLIC (ตัวล่าง)", min_value=0)

if st.button("🔎 ตรวจสอบระดับความดัน"):

    if systolic == 0 or diastolic == 0:
        st.warning("กรุณากรอกค่าความดันให้ครบถ้วน")
    else:

        result = None

        for _, row in df.iterrows():

            sys_parsed = parse_condition(row["SYSTOLIC mm Hg (top/upper number)"])
            dia_parsed = parse_condition(row["DIASTOLIC mm Hg (bottom/lower number)"])
            logic = str(row["and/or"]).lower()

            sys_match = check_value(systolic, sys_parsed)
            dia_match = check_value(diastolic, dia_parsed)

            if logic == "and":
                match = sys_match and dia_match
            else:  # or / and/or
                match = sys_match or dia_match

            if match:
                result = row["BLOOD PRESSURE CATEGORY"]
                break

        if result:
            thai_result = thai_translation.get(result.upper(), "")
            st.markdown("## 📊 ผลการประเมิน")

            if severity_order[result.upper()] >= 4:
                st.error(f"🔴 {thai_result}")
            elif severity_order[result.upper()] == 3:
                st.warning(f"🟠 {thai_result}")
            elif severity_order[result.upper()] == 2:
                st.info(f"🟡 {thai_result}")
            else:
                st.success(f"🟢 {thai_result}")

            st.write(f"ระดับภาษาอังกฤษ: {result}")

        else:
            st.error("ไม่พบระดับที่ตรงเงื่อนไข")
