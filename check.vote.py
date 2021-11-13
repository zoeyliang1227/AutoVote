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

url = 'https://rox.gnjoy.com.tw/roxfanart?fbclid=IwAR0q-Vxh2FGBrzzmKIE7tHEoVJskCZJkfNxAX3rlP-lEQoCMaaeF5ZXtT9g#_=_'
timeout = 3
hour = random.randint(7,12)
minute = random.randint(0,59)
lib = {}
list=[]



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

    ro_url = url
    driver.get(ro_url)

    return driver


def check_vote():    
    try:
        driver = get_driver()
        now = datetime.datetime.now()
        print(now)
        # get_vote(driver)
        # list_nu = ['106', '26', '36', '46']
        # for i in range(len(list_nu)):
        #     # driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[3]/input').send_keys('106')
        #     driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[3]/input').send_keys(list_nu[i+1])
        #     print(i+1)
        #     time.sleep(10)
        #     get_vote(driver)
        #     driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[3]/input').clear()
        #     time.sleep(10)
            # driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[3]/input').send_keys('26')
            # time.sleep(10)
            # get_vote(driver)
        choose = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[2]/div[2]')
        choose.click()
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__active--1YiWY')))
        choose_title = choose.text
        print('click %s'%choose_title)
        
        time.sleep(5)
        for i in range(1, 9):
            for n in range(1, 9):
                print(n)
                number = driver.find_element(By.XPATH, '//*[@id="root"]/*[name()="div"]/*[name()="div"][4]/*[name()="div"][1]/*[name()="div"][4]/*[name()="div"]/*[name()="div"]['+ str(n) + ']/*[name()="div"]/*[name()="div"][1]/*[name()="span"][2]')
                number_name = number.text
                # print(number_name)
                time.sleep(3)
                work = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div['+ str(n) + ']/div/div[6]/div[1]/span')
                work_name = work.text
                # print(work_name)
                lib[number_name] = work_name
                list.append(work_name)
                # print(lib)
                # print(type(work_name))

            driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div[9]/div/span['+ str(i + 1) + ']').click()
        print(sorted(lib.keys()))
                
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
    lib[name] = currently
    list.append(currently)



if __name__ == '__main__':
    check_vote()