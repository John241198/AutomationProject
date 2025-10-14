from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def SetExplicit(page, timeout_s, element, expectedCondition, locatorType='css'):
    # Map locator type
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

    # Choose expected condition
    if expectedCondition == "visibleOfElementLocated":
        condition = EC.visibility_of_element_located
    elif expectedCondition == "invisibleOfElementLocated":
        condition = EC.invisibility_of_element_located
    elif expectedCondition == "clickable":
        condition = EC.element_to_be_clickable
    else:
        raise ValueError(f"Unknown expectedCondition: {expectedCondition}")

    # Apply wait
    element = WebDriverWait(page, timeout_s).until(condition(locator))
    return element


def EnterValue(page, by_type, locator, value):
    element = page.find_element(by_type, locator)
    page.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()
    element.clear()
    element.send_keys(value)
    return element