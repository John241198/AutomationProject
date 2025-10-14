
from selenium import webdriver
import helper
import time
import logging
from selenium.webdriver.common.by import By


logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler("automation_log.txt")
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(file_formatter)
logger.addHandler(console_handler)

drive = webdriver.Firefox()
drive.get('https://the-internet.herokuapp.com/')
logging.info("Opened the website: https://the-internet.herokuapp.com/")
start_time = time.time()
helper.SetExplicit(drive, timeout_s=20, element="content", expectedCondition="visibleOfElementLocated",locatorType="id")
time.sleep(10)
end_time = time.time()
duration = round(end_time - start_time, 2)
print(f"Wait duration: {duration} seconds")
logging.info(f"Explicit wait completed in {duration} seconds for element 'content'.")
drive.execute_script("document.getElementsByTagName('a')[21].click()")
helper.SetExplicit(drive, timeout_s=20, element="login", expectedCondition="visibleOfElementLocated",locatorType="id")
helper.EnterValue(drive, By.ID, "username", "tomsmith")
helper.EnterValue(drive, By.ID, "password", "SuperSecretPassword!")
drive.find_element(By.CLASS_NAME, "radius").click()
time.sleep(10)
alert = drive.switch_to.alert
logging.info("Alert says:", alert.text)
alert.accept()
loginVal= drive.execute_script("document.getElementsByTagName('h4')[0].textContent")
if "Secure Area" not in loginVal:raise Exception("Secure Area is not present.")
else:logging.info("Login successfully - %s"%loginVal)
drive.execute_script("document.getElementsByTagName('a')[2].click()")
helper.SetExplicit(drive, timeout_s=20, element="login", expectedCondition="visibleOfElementLocated",locatorType="id")
logoutVal = drive.execute_script("document.getElementsByTagName('h2')[0].textContent")
if 'Login' not in loginVal:raise Exception("Login Page is not present.")
else:logging.info("Logout successfully - %s reached as expected!"%logoutVal)
drive.quit()
logging.info("Browser closed")


