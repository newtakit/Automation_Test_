import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ตั้งค่า Logging
logging.basicConfig(filename="test_log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Login test started")

# เปิดเว็บเบราว์เซอร์
driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com/")

# ข้อมูลล็อกอินสำหรับทดสอบ
test_cases = [
    ("standard_user", "secret_sauce"),  # ✅ ถูกต้อง
    ("wrong_user", "secret_sauce"),     # ❌ Username ผิด
    ("standard_user", "wrong_pass"),    # ❌ Password ผิด
    ("wrong_user", "wrong_pass")        # ❌ ทั้งคู่ผิด
]

try:
    for username_data, password_data in test_cases:
        # ใช้ WebDriverWait เพื่อรอให้ element ปรากฏ
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "user-name"))
        )
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        # กรอกข้อมูล
        username.clear()
        password.clear()
        username.send_keys(username_data)
        password.send_keys(password_data)

        # คลิกปุ่ม Login
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        # ตรวจสอบผลลัพธ์
        if "inventory.html" in driver.current_url:
            logging.info(f"✅ Login success with Username: {username_data}, Password: {password_data}")
        else:
            logging.error(f"❌ Login failed with Username: {username_data}, Password: {password_data}")

        # รีเฟรชหน้าเว็บเพื่อทดสอบกรณีถัดไป
        driver.get("https://www.saucedemo.com/")

except Exception as e:
    logging.error(f"Test encountered an error: {str(e)}")

finally:
    # ปิดเว็บเบราว์เซอร์
    driver.quit()