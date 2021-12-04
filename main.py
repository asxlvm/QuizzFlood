from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import threading, random, string, psutil

URL = "https://joinmyquiz.com"
JOINXPATH = "//input[@placeholder='Enter a join code']"
NAMEXPATH = "//input[@placeholder='Enter your name']"
STARTXPATH = "//button[@class='primary-button start-game']"

CODE = ""
NAME = ""
NUMTHREADS = 2
REQPERTHREAD = 15

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-extensions')
#chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(options=chrome_options)
# driver.get('https://joinmyquiz.com')
# el = WebDriverWait(driver, 10, 1).until(
#         EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter a join code']"))
# )
# print(el.get_attribute("placeholder"))
# el.send_keys(CODE)
# el.send_keys(Keys.RETURN)
# enter_name = WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your name']")))
# rand = "".join([str(random.choice(string.digits)) for _ in range(5)])
# print(enter_name.get_attribute("placeholder"))
# enter_name.send_keys(Keys.CONTROL+"A")
# enter_name.send_keys("LMAO BOZO - " + rand)
# enter_name.send_keys(Keys.RETURN)
#
# start = WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.XPATH, "//button[@class='primary-button start-game']")))
# print(start.get_attribute("value"))
# print(driver.current_url)
# driver.execute_script("""fetch("https://raw.githubusercontent.com/gbaranski/quizizz-cheat/master/dist/bundle.js").then((res) => res.text().then((t) => eval(t)))""")

def gen_code():
    """
    Generates a random 7 letters long unsecure code using a list comprehension and random.choice with string's constants containing every lowercase letter and 2x every digit
    """
    return "".join([str(random.choice(string.digits * 2 + string.ascii_lowercase)) for _ in range(7)]) 

class BotInstance:
    def __init__(self, num, code, name, driver, torun):
        self.num = num
        self.code = code
        self.base_name = name
        self.name = name + f" - {gen_code()}"
        self.driver = driver
        self.to_run = torun
        self.ran = 0

    def error(self, where) -> str:
        return f"Bot {self.num} ({self.name}) failed at {where}: "

    def status(self, where) -> str:
        return f"Bot {self.num} ({self.name}) finished {where}: "

    def join(self) -> bool:
        try:
            self.driver.get(URL)

            inputbar = WebDriverWait(self.driver, 10, 1).until(EC.presence_of_element_located((By.XPATH, JOINXPATH)))
            inputbar.send_keys(self.code)
            inputbar.send_keys(Keys.RETURN)
            print(f"{self.status('joining')}")

            return True
        except Exception as e:
            print(f"{self.error('join')}{e}")
            return False

    def start(self) -> bool:
        try:
            inputbar = WebDriverWait(self.driver, 10, 1).until(EC.presence_of_element_located((By.XPATH, NAMEXPATH)))
            inputbar.send_keys(Keys.CONTROL + "A")
            inputbar.send_keys(self.name)
            inputbar.send_keys(Keys.RETURN)
            print(f"{self.status('starting')}")

            return True
        except Exception as e:
            print(f"{self.error('start')}{e}")
            return False

    def do_all(self):
        for _ in range(self.to_run):
            if self.join() is True:
                self.start()
            self.ran += 1
            self.name = self.base_name + f" - {gen_code()}"
        self.quit()
            

    def quit(self) -> None:
        try:
            self.driver.quit()
        except:
            return

def main():
    global CODE, NAME, NUMTHREADS, REQPERTHREAD
    bots = []
    threads = []

    print("[insert huge colorful WoT edgy banner]")

    if CODE == "":
        CODE = input("What is the desired code to flood?").split()[0]

    if NAME == "":
        NAME = input("What name should be used for every bot?")

    if NUMTHREADS < 1:
        NUMTHREADS = int(input("How many threads should the program use? (How many browsers will open at once, recommended not to do more than 5-10)"))

    if REQPERTHREAD < 1:
        REQPERTHREAD = int(input("How many times should a bot join through the same thread? (Choose this based on how much bots you want to have, if you have 10 threads and select 10 requests per thread, then the final count of bots will be 100."))

    for i in range(NUMTHREADS):
        #d = webdriver.Firefox(executable_path="geckodriver")
        d = webdriver.Chrome(options = chrome_options)
        #d.set_window_size(1120, 550)
        bots.append(BotInstance(i, CODE, NAME, d, REQPERTHREAD))

    for b in bots:
        threads.append(threading.Thread(target=b.do_all))

    for t in threads:
        t.start()

if __name__ == "__main__":
    main()

