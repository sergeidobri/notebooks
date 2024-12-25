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

options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def wait_element(browser, delay=3, by=By.TAG_NAME, value=None):
    try: 
        return WebDriverWait(browser, delay).until(
            expected_conditions.presence_of_element_located((by, value))
        )
    except TimeoutException:
        return None

driver.get("https://dtf.ru/games")
time.sleep(1)

articles = driver.find_elements(by=By.CSS_SELECTOR, value='div.content--short')
links = []
for article in articles:
    link = wait_element(browser=article, by=By.CSS_SELECTOR, value='a.content__link').get_attribute('href')
    links.append(link)

data = []
for link in links:
    driver.get(link)
    title = wait_element(browser=driver, by=By.CSS_SELECTOR, value='h1.content-title').text
    content = wait_element(browser=driver, by=By.CSS_SELECTOR, value='article.content__blocks').text.replace('\"', '\'')
    date = wait_element(browser=driver, by=By.TAG_NAME, value='time').get_attribute('title')
    data.append({
        'link': link,
        'title': title,
        'content': content,
        'date': date
    })
    
with open('data_selenium.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

driver.close()
