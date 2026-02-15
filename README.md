# Design-Thinking-2025
<img width="1011" height="477" alt="image" src="https://github.com/user-attachments/assets/4c80075f-ab1f-4fa8-8a7e-2a7d14a89749" />

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. ตั้งค่า Chrome Options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # เปิดถ้าไม่ต้องการให้ browser แสดง

# 2. เริ่มต้น WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 3. เข้าเว็บเป้าหมาย
    url = "https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings"
    driver.get(url)

    # รอให้หน้าเว็บโหลดจนเจอ h1
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )

    # 4. ดึงหัวข้อหลัก (H1)
    title = driver.find_element(By.TAG_NAME, "h1").text
    print("หัวข้อบทความ:")
    print(title)
    print("=" * 60)

    # 5. ดึงหัวข้อย่อย (H2)
    subtitles = driver.find_elements(By.TAG_NAME, "h2")

    print("\nหัวข้อย่อยในบทความ:\n")
    for sub in subtitles:
        if sub.text.strip():
            print("-", sub.text)

    # 6. ดึงย่อหน้าเนื้อหา
    paragraphs = driver.find_elements(By.TAG_NAME, "p")

    print("\nตัวอย่างเนื้อหาบางส่วน:\n")
    for p in paragraphs[:5]:
        if p.text.strip():
            print(p.text)
            print("-" * 40)

    # 7. ดึงข้อมูลจากตารางทั้งหมด
    tables = driver.find_elements(By.TAG_NAME, "table")

    print("\nข้อมูลจากตาราง:\n")

    import csv
    
    for table_index, table in enumerate(tables, start=1):
        print(f"\nตารางที่ {table_index}")
        print("-" * 60)

        rows = table.find_elements(By.TAG_NAME, "tr")
        table_data = []

        for row in rows:
            headers = row.find_elements(By.TAG_NAME, "th")
            cols = row.find_elements(By.TAG_NAME, "td")

            all_cells = headers + cols
            row_data = [cell.text.strip() for cell in all_cells]

            if any(row_data):
                table_data.append(row_data)
                print(" | ".join(row_data))

        # write this table to csv
        if table_data:
            csv_filename = f"table_{table_index}.csv"
            try:
                with open(csv_filename, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerows(table_data)
                print(f"ข้อมูลตารางถูกบันทึกไปยัง {csv_filename}")
            except Exception as e:
                print(f"ไม่สามารถเขียนไฟล์ {csv_filename}: {e}")

finally:
    driver.quit()
