from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time, random, string

code = "8848598"

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://joinmyquiz.com')
el = WebDriverWait(driver, 10, 1).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter a join code']"))
)
print(el.get_attribute("placeholder"))
el.send_keys(code)
el.send_keys(Keys.RETURN)
enter_name = WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your name']")))
rand = "".join([str(random.choice(string.digits)) for _ in range(5)])
print(enter_name.get_attribute("placeholder"))
enter_name.send_keys(Keys.CONTROL+"A")
enter_name.send_keys("LMAO BOZO - " + rand)
enter_name.send_keys(Keys.RETURN)

start = WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.XPATH, "//button[@class='primary-button start-game']")))
print(start.get_attribute("value"))
hostlabel = WebDriverWait(driver, 15, 1).until(EC.presence_of_element_located((By.XPATH, "//div[@class='host-player-label']")))
print(hostlabel.get_attribute("value"))
print(driver.current_url)

input()
driver.quit()