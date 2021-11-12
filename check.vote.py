# import schedule
import time
import yaml
import datetime
import random
# import getpass
import random


from threading import Timer
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

credentials = yaml.load(open('config.yml'))
timeout = 3
hour = random.randint(7,12)
minute = random.randint(0,59)



def get_driver():
    chrome_options = Options()
    # # 關閉通知(是否顯示通知)
    prefs = {
        'profile.default_content_setting_values':
        {
            'notifications':2
        }
    }
    chrome_options.add_experimental_option('prefs', prefs)
    
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("window-size=1024,768")
    chrome_options.add_argument('headless')                 # 瀏覽器不提供可視化頁面
    chrome_options.add_argument('no-sandbox')               # 以最高權限運行
    chrome_options.add_argument('--start-maximized')        # 縮放縮放（全屏窗口）設置元素比較準確
    chrome_options.add_argument('--disable-gpu')            # 谷歌文檔說明需要加上這個屬性來規避bug
    chrome_options.add_argument('--window-size=1920,1080')  # 設置瀏覽器按鈕（窗口大小）
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options = chrome_options, executable_path = 'chromedriver')

    url = credentials['ro_url']
    ro_url = url
    driver.get(ro_url)

    return driver


def check_vote():    
    try:
        driver = get_driver()
        now = datetime.datetime.now()
        print(now)
        get_vote(driver)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[3]/input').send_keys('106')
        time.sleep(10)
        get_vote(driver)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[3]/input').clear()
        time.sleep(10)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[3]/input').send_keys('26')
        time.sleep(10)
        get_vote(driver)

                
    finally:
        time.sleep(3)
        driver.quit()

def get_vote(driver):
    choose = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[2]/div[2]')
    choose.click()
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__active--1YiWY')))
    choose_title = choose.text
    print('click %s'%choose_title)

    time.sleep(5)
    vote = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div[1]/div/div[5]')
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__title--2JLqT')))
    work = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div[1]/div/div[2]')
    name = work.text
    print(name)

    vote = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div[1]/div/div[6]/div[1]/span')
    currently = vote.text
    print(currently)



if __name__ == '__main__':
    check_vote()