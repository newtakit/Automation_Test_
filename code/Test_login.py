import yaml
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Path ของ ChromeDriver
chrome_driver_path = r"C:/Users/newta/Documents/GitHub/Automation_Test_/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# อ่าน Test Cases จากไฟล์ YAML
with open("Test_case_login.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

test_cases = data.get("Test_cases", [])

# สร้างรายการสำหรับเก็บผลลัพธ์
results = []

try:
    for test_case in test_cases:
        test_id = test_case.get("Test Case ID", "N/A")
        scenario = test_case.get("Test Scenario", "Unknown Scenario")
        steps = test_case.get("Steps", [])
        expected_result = test_case.get("Expected Result", [])

        try:
            # เปิดเว็บ SauceDemo
            driver.get("https://www.saucedemo.com/")

            # รันตาม Test Scenario
            if "Valid Login" in scenario:
                driver.find_element(By.ID, "user-name").send_keys("standard_user")
                driver.find_element(By.ID, "password").send_keys("secret_sauce")
                driver.find_element(By.ID, "login-button").click()

                # ตรวจสอบว่าล็อกอินสำเร็จ
                status = "Passed" if "inventory.html" in driver.current_url else "Failed"
                notes = "Login successful." if status == "Passed" else "Login failed."

            elif "InValid Login" in scenario:
                username = "wrong_user" if "Wrong Username" in scenario else "standard_user"
                password = "wrong_user" if "Wrong Password" in scenario else "secret_sauce"

                driver.find_element(By.ID, "user-name").send_keys(username)
                driver.find_element(By.ID, "password").send_keys(password)
                driver.find_element(By.ID, "login-button").click()

                error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
                expected_error = "Epic sadface" in error_message

                status = "Passed" if expected_error else "Failed"
                notes = error_message if expected_error else "Error message not displayed."

            else:
                status, notes = "Failed", "Unknown test case."

            results.append({
                "Test Case ID": test_id,
                "Test Scenario": scenario,
                "Status": status,
                "Notes": notes
            })

        except Exception as e:
            results.append({"Test Case ID": test_id, "Test Scenario": scenario, "Status": "Failed", "Notes": str(e)})

finally:
    driver.quit()  # ปิด WebDriver

# สร้าง DataFrame และบันทึกลงไฟล์ CSV
df = pd.DataFrame(results)
df.to_csv("test_case_login_report.csv", index=False, encoding="utf-8")

# แสดงข้อมูลรีพอร์ตในรูปแบบตาราง
print("\n=== Test Report Summary ===")
print(df.to_string(index=False))

# บันทึกเป็นไฟล์ Excel
df.to_excel("test_report_login.xlsx", index=False, engine="openpyxl")
print("\nรายงานการทดสอบถูกบันทึกในไฟล์ test_report.csv และ test_report.xlsx")