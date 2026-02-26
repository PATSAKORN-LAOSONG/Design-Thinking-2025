import streamlit as st
import pandas as pd

st.set_page_config(page_title="ระบบประเมินระดับความดันโลหิต", page_icon="🩺")

st.title("🩺 ระบบประเมินระดับความดันโลหิต")
st.write("กรอกค่าความดันโลหิตของคุณ ระบบจะประเมินระดับตามเกณฑ์มาตรฐาน")

# โหลดไฟล์ตารางจาก CSV
df = pd.read_csv("table_1.csv")

# แปลระดับเป็นภาษาไทย
thai_translation = {
    "NORMAL": "ระดับปกติ",
    "ELEVATED": "ระดับค่อนข้างสูง",
    "STAGE 1": "ความดันโลหิตสูง ระยะที่ 1",
    "STAGE 2": "ความดันโลหิตสูง ระยะที่ 2",
    "SEVERE": "ภาวะความดันสูงรุนแรง",
    "EMERGENCY": "ภาวะฉุกเฉิน ควรพบแพทย์ทันที"
}

# คำแนะนำสุขภาพ
advice_text = {
    "NORMAL": "รักษาพฤติกรรมสุขภาพที่ดี ออกกำลังกายสม่ำเสมอ",
    "ELEVATED": "ควรลดเค็ม ลดอาหารมัน และควบคุมน้ำหนัก",
    "STAGE 1": "ควรปรึกษาแพทย์และปรับพฤติกรรมการใช้ชีวิต",
    "STAGE 2": "ควรพบแพทย์เพื่อตรวจและรับคำแนะนำเพิ่มเติม",
    "SEVERE": "ควรพบแพทย์โดยเร็ว",
    "EMERGENCY": "ควรไปโรงพยาบาลทันที"
}

# ฟังก์ชันแปลเงื่อนไขข้อความในไฟล์
def check_condition(value, condition_text):
    condition_text = str(condition_text).upper()

    if "LESS THAN" in condition_text:
        num = int(condition_text.split()[-1])
        return value < num

    elif "-" in condition_text:
        parts = condition_text.split("-")
        low = int(parts[0].strip())
        high = int(parts[1].strip())
        return low <= value <= high

    elif "OR HIGHER" in condition_text:
        num = int(condition_text.split()[0])
        return value >= num

    elif "HIGHER THAN" in condition_text:
        num = int(condition_text.split()[-1])
        return value > num

    return False


# รับค่าจากผู้ใช้
systolic = st.number_input("ค่า SYSTOLIC (ค่าความดันตัวบน)", min_value=0)
diastolic = st.number_input("ค่า DIASTOLIC (ค่าความดันตัวล่าง)", min_value=0)

if st.button("🔎 ตรวจสอบระดับความดัน"):

    if systolic == 0 or diastolic == 0:
        st.warning("กรุณากรอกค่าความดันให้ครบถ้วน")
    else:
        result = None

        for index, row in df.iterrows():

            if pd.isna(row["SYSTOLIC mm Hg (top/upper number)"]):
                continue

            sys_condition = row["SYSTOLIC mm Hg (top/upper number)"]
            dia_condition = row["DIASTOLIC mm Hg (bottom/lower number)"]
            logic = str(row["and/or"]).lower()

            sys_match = check_condition(systolic, sys_condition)
            dia_match = check_condition(diastolic, dia_condition)

            if logic == "and":
                if sys_match and dia_match:
                    result = row["BLOOD PRESSURE CATEGORY"]
                    break

            elif logic == "or":
                if sys_match or dia_match:
                    result = row["BLOOD PRESSURE CATEGORY"]
                    break

            elif "and/or" in logic:
                if sys_match or dia_match:
                    result = row["BLOOD PRESSURE CATEGORY"]
                    break

        if result:

            thai_result = thai_translation.get(result.upper(), "ไม่พบคำแปล")
            advice = advice_text.get(result.upper(), "")

            st.markdown("---")
            st.markdown("## 📊 ผลการประเมิน")

            # แสดงสีตามระดับ
            if result.upper() == "NORMAL":
                st.success(f"🟢 {thai_result}")
            elif result.upper() == "ELEVATED":
                st.info(f"🟡 {thai_result}")
            elif result.upper() == "STAGE 1":
                st.warning(f"🟠 {thai_result}")
            else:
                st.error(f"🔴 {thai_result}")

            st.write(f"**ระดับภาษาอังกฤษ:** {result}")
            st.write(f"💡 คำแนะนำ: {advice}")

        else:
            st.error("ไม่พบระดับที่ตรงเงื่อนไข")
