from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time

# สร้าง WebDriver (ในที่นี้ใช้ ChromeDriver)
driver = webdriver.Chrome()

# เตรียมไฟล์ CSV สำหรับบันทึกผลลัพธ์
csv_file = 'test_results.csv'
fields = ['Test Case ID', 'Description', 'Result', 'Details']

# ฟังก์ชันสำหรับเขียนผลลัพธ์ลงไฟล์ CSV
def write_to_csv(data):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# เขียน Header ลงไฟล์ (ครั้งแรก)
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(fields)

try:
    # เปิดเว็บ Google
    driver.get("https://www.google.com")
    driver.maximize_window()

    # Test Case 1: ตรวจสอบการเปิดหน้า Google
    try:
        assert "Google" in driver.title
        write_to_csv(['TC001', 'Open Google Homepage', 'PASS', 'Page title is correct'])
    except AssertionError:
        write_to_csv(['TC001', 'Open Google Homepage', 'FAIL', 'Page title is incorrect'])

    # Test Case 2: ค้นหาข้อความ
    try:
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Selenium Python")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # รอผลการค้นหาโหลด
        results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        assert len(results) > 0  # ตรวจสอบว่ามีผลการค้นหา
        write_to_csv(['TC002', 'Search for Selenium Python', 'PASS', f'Found {len(results)} results'])
    except Exception as e:
        write_to_csv(['TC002', 'Search for Selenium Python', 'FAIL', str(e)])

finally:
    # ปิดเบราว์เซอร์
    driver.quit()
    print(f"Test results saved to {csv_file}")