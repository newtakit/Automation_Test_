# นำเข้า Libraries ที่จำเป็น
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Path ของ ChromeDriver
chrome_driver_path = r"C:/Users/newta/Documents/GitHub/Automation_Test_/chromedriver.exe"  # ระบุ Path ของ ChromeDriver
service = Service(chrome_driver_path)

# สร้าง WebDriver Instance
driver = webdriver.Chrome(service=service)

# รายการ Test Cases ในรูปแบบ Dictionary
test_cases = [
    {"Test Case ID": 1, "Description": "Test Button Click", "Steps": "Click on button", "Expected Result": "Button clicked successfully", "Element ID": "non_existent_button"},
    {"Test Case ID": 2, "Description": "Test Page Load", "Steps": "Open URL", "Expected Result": "Page loads correctly", "URL": "https://demoqa.com"}
]

# สร้างตัวแปรสำหรับเก็บผลลัพธ์
results = []

try:
    for test_case in test_cases:
        test_id = test_case["Test Case ID"]
        description = test_case["Description"]
        
        try:
            if description == "Test Page Load":
                # ทดสอบการโหลดหน้าเว็บ
                driver.get(test_case["URL"])
                if "DEMOQA" in driver.title:
                    results.append({"Test Case ID": test_id, "Description": description, "Status": "Passed", "Notes": "Page loaded successfully"})
                else:
                    raise Exception("Page title mismatch.")
            
            elif description == "Test Button Click":
                # ทดสอบการคลิกปุ่ม
                button = driver.find_element(By.ID, test_case["Element ID"])
                button.click()
                results.append({"Test Case ID": test_id, "Description": description, "Status": "Passed", "Notes": "Button clicked successfully."})
        
        except Exception as e:
            # จัดการข้อผิดพลาด
            results.append({"Test Case ID": test_id, "Description": description, "Status": "Failed", "Notes": str(e)})

finally:
    # ปิด WebDriver
    driver.quit()

# บันทึกผลลัพธ์ในรูปแบบ DataFrame
df = pd.DataFrame(results)

# สร้างรายงานในรูปแบบ CSV
output_file = "test_report.csv"
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"รายงานการทดสอบถูกบันทึกในไฟล์: {output_file}")

# อ่านและแสดงผลลัพธ์จากไฟล์ CSV
try:
    df_loaded = pd.read_csv(output_file)
    print("\nผลลัพธ์จากไฟล์ CSV:")
    print(df_loaded)
except Exception as e:
    print(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {str(e)}")