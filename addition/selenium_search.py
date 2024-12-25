import json
import time
from selenium.common import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--fullscreen')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def wait_element(browser, delay=3, by=By.TAG_NAME, value=None):
    try: 
        return WebDriverWait(browser, delay).until(
            expected_conditions.presence_of_element_located((by, value))
        )
    except TimeoutException:
        return None

driver.maximize_window()
driver.get("https://dtf.ru/games")
time.sleep(1)

search_button = wait_element(driver, by=By.CSS_SELECTOR, value='button.search__button')
search_button.click()  # нажатие на кнопку
time.sleep(1)
search_input = wait_element(driver, by=By.CSS_SELECTOR, value='input.text-input')
search_input.send_keys('папич', Keys.ENTER)
time.sleep(10)

driver.close()
