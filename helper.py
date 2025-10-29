import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def SetExplicit(page, timeout_s, element, expectedCondition, locatorType='css'):
    if locatorType == 'id':
        locator = (By.ID, element)
    elif locatorType == 'xpath':
        locator = (By.XPATH, element)
    elif locatorType == 'link':
        locator = (By.LINK_TEXT, element)
    elif locatorType == 'partiallink':
        locator = (By.PARTIAL_LINK_TEXT, element)
    elif locatorType == 'name':
        locator = (By.NAME, element)
    elif locatorType == 'class':
        locator = (By.CLASS_NAME, element)
    else:
        locator = (By.CSS_SELECTOR, element)

    if expectedCondition == "visibleOfElementLocated":
        condition = EC.visibility_of_element_located
    elif expectedCondition == "invisibleOfElementLocated":
        condition = EC.invisibility_of_element_located
    elif expectedCondition == "clickable":
        condition = EC.element_to_be_clickable
    else:
        raise ValueError(f"Unknown expectedCondition: {expectedCondition}")

    element = WebDriverWait(page, timeout_s).until(condition(locator))
    return element


def EnterValue(page, by_type, locator, value):
    element = page.find_element(by_type, locator)
    page.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()
    element.clear()
    element.send_keys(value)
    return element


def logInOutValidation(page, userName=None, password=None, logOutCheck=False, errorMessage=None):
    EnterValue(page, By.ID, "username", userName)
    EnterValue(page, By.ID, "password", password)
    page.find_element(By.CLASS_NAME, "radius").click()
    time.sleep(10)
    dataMsg = page.execute_script("return document.getElementById('flash').textContent")
    if errorMessage:
        if errorMessage not in dataMsg:
            raise Exception("Expected error message not occurred!")
        else: logging.info("Correct error validation - %s"%errorMessage)
    else:
        logging.info("Successfully logged in and login message - %s"%dataMsg)
    if logOutCheck:
        page.execute_script("document.getElementsByTagName('a')[2].click()")
        SetExplicit(page, timeout_s=20, element="login", expectedCondition="visibleOfElementLocated", locatorType="id")
        dataMsg = page.execute_script("return document.getElementById('flash').textContent")
        if "logged out" not in dataMsg:raise Exception("Login Page is not present.")
        else:logging.info("Successfully logged out and logout message - %s" % dataMsg)

    return page

def homePageReturn(page, retriveCount):
    for _ in range(retriveCount):page.back()
    SetExplicit(page, timeout_s=20, element="content", expectedCondition="visibleOfElementLocated",
                       locatorType="id")
    return page


def enableCheckbox(page, chkValue=False, index=0):
    if not page.execute_script("return document.getElementsByTagName('input')[%s].checked"%index) and chkValue:
        page.execute_script("return document.getElementsByTagName('input')[%s].click()"%index)
    elif page.execute_script("return document.getElementsByTagName('input')[%s].checked"%index) and not chkValue:
        page.execute_script("return document.getElementsByTagName('input')[%s].click()" % index)

#not worked need to handle
def drag_and_drop_by_coordinate_offset(driver, source_id: str, target_id: str):
    """
    Calculates the exact pixel offset required and performs the drag-and-drop.
    """
    source = driver.find_element(By.ID, source_id)
    target = driver.find_element(By.ID, target_id)

    # 1. Get the current (x, y) coordinates for the elements
    source_location = source.location
    target_location = target.location

    # 2. Calculate the difference (offset) needed to move the source to the target's position.
    # We move the *center* of the source to the *center* of the target.
    # Note: We subtract the source coordinates from the target coordinates.
    x_offset = target_location['x'] - source_location['x']
    y_offset = target_location['y'] - source_location['y']

    # 3. Use the drag_and_drop_by_offset method to move by the calculated offset
    # We subtract 10 pixels from the Y offset as a margin of error for the header/border
    ActionChains(driver).drag_and_drop_by_offset(source, x_offset, y_offset - 10).perform()

# --- Example Usage ---
# drag_and_drop_by_coordinate_offset(driver, "column-a", "column-b")