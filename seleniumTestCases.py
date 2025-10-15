
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import helper
import time
import logging
import os


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
logging.info(f"Wait duration: {duration} seconds")
logging.info(f"Explicit wait completed in {duration} seconds for element 'content'.")

#Test case1 - Form Authentication
logging.info("Test Case1 - Form Authentication")
drive.execute_script("document.getElementsByTagName('a')[21].click()")
helper.SetExplicit(drive, timeout_s=20, element="login", expectedCondition="visibleOfElementLocated",locatorType="id")
helper.logInOutValidation(drive,userName="admin", password="adminPassword", errorMessage="Your username is invalid!")
helper.logInOutValidation(drive,userName="tomsmith", password="SuperSecretPassword!", logOutCheck=True, errorMessage=None)
helper.homePageReturn(drive, retriveCount=3)


#Test case2 - JQuery UI Menus
logging.info("Test Case2 - JQuery UI Menus")
drive.execute_script("document.getElementsByTagName('a')[28].click()")
helper.SetExplicit(drive, timeout_s=20, element="menu", expectedCondition="visibleOfElementLocated",locatorType="id")
drive.find_element(By.ID, "ui-id-3").click()
helper.SetExplicit(drive, timeout_s=20, element="ui-id-8", expectedCondition="visibleOfElementLocated",locatorType="id")
drive.find_element(By.ID, "ui-id-8").click()
helper.SetExplicit(drive, timeout_s=20, element="description", expectedCondition="visibleOfElementLocated",locatorType="class")
drive.execute_script("document.getElementsByTagName('a')[2].click()")
helper.SetExplicit(drive, timeout_s=20, element="menu", expectedCondition="visibleOfElementLocated",locatorType="id")
drive.find_element(By.ID, "ui-id-3").click()
helper.SetExplicit(drive, timeout_s=20, element="ui-id-4", expectedCondition="visibleOfElementLocated",locatorType="id")
drive.find_element(By.ID, "ui-id-4").click()
helper.SetExplicit(drive, timeout_s=20, element="ui-id-5", expectedCondition="visibleOfElementLocated",locatorType="id")
drive.find_element(By.ID, "ui-id-5").click()
time.sleep(10)
drive.switch_to.window('')
helper.SetExplicit(drive, timeout_s=20, element="menu", expectedCondition="visibleOfElementLocated",locatorType="id")
if os.path.exists(os.path.join(r"C:\Users\victor\Downloads", "menu.pdf")):
    logging.info("As expected file as been downloaded!")
else:raise Exception("Issue on downloading the files on menu click.")
drive.get("https://the-internet.herokuapp.com/")

#Test Case3 - Drag and Drop - need to work
logging.info("Test Case3 - Drag and Drop")
drive.execute_script("document.getElementsByTagName('a')[10].click()")
helper.SetExplicit(drive, timeout_s=20, element="columns", expectedCondition="visibleOfElementLocated",locatorType="id")
actions = ActionChains(drive)
source_element = drive.find_element(By.ID, "column-a")
target_element = drive.find_element(By.ID, "column-b")
actions.click_and_hold(source_element).perform()
time.sleep(1)
actions.move_to_element(target_element).perform()
time.sleep(1)
actions.release(target_element).perform()

#actions.drag_and_drop(source_element, target_element).perform()
time.sleep(10)



drive.quit()
logging.info("Browser closed \n")


