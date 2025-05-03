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

try:
    # ใช้ WebDriverWait เพื่อรอให้ element ปรากฏ
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "user-name"))
    )
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )

    # กรอกข้อมูล
    username.send_keys("standard_user")
    password.send_keys("secret_sauce")

    # คลิกปุ่ม Login
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    # ตรวจสอบว่าการ Login สำเร็จ
    if "inventory.html" in driver.current_url:
        logging.info("passed")
    else:
        logging.error("failed")

except Exception as e:
    logging.error(f"Test encountered an error: {str(e)}")

finally:
    # ปิดเว็บเบราว์เซอร์
    driver.quit()