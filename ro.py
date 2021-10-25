import json
import time
import yaml
import platform
import os
import datetime
import random
import sched
import pickle


from threading import Timer
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

credentials = yaml.load(open('config.yml'))
# driver = get_driver()
# wait = get_driver()

hour = random.randint(7,12)
minute = random.randint(0,59)

def doSth():
    ro()
    print(u'這個程式要開始瘋狂的運轉啦')

def main(h=hour,m=minute):
    print(h,m)
    while True:
        now = datetime.datetime.now()
        # print(now.hour, now.minute)
        if now.hour == h and now.minute == m:
            break
    
    doSth()

    # 每86400秒（1天），傳送1次
    t = Timer(86400, main)
    t.start()

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
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("window-size=1024,768")
    # chrome_options.add_argument('headless')                 # 瀏覽器不提供可視化頁面
    chrome_options.add_argument('no-sandbox')               # 以最高權限運行
    chrome_options.add_argument('--start-maximized')        # 縮放縮放（全屏窗口）設置元素比較準確
    chrome_options.add_argument('--disable-gpu')            # 谷歌文檔說明需要加上這個屬性來規避bug
    chrome_options.add_argument('--window-size=1920,1080')  # 設置瀏覽器按鈕（窗口大小）
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path = 'chromedriver')
    url = credentials['ro_url']
    ro_url = url
    driver.get(ro_url)

    return driver

driver = get_driver()
wait = WebDriverWait(driver, 1)

def ro():    
    ##登入FB
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__title--1GEE0')))
    for i in range(1):
        try:
            vote()
            login()
            driver.refresh()
            vote()

            done_vote = driver.find_element_by_xpath('//*[@id="useModal__3"]/div/div/div[1]/div[1]')
            done_vote.click()
            print('111')
            done_title = done_vote.text
            if done_title == '作品當天已投過票':
                print(done_title)
                break
            else:
                print(done_title)  

        finally:
            time.sleep(3)
            driver.quit()

def vote():
    choose = driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div[2]/div[2]')
    choose.click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__active--1YiWY')))
    choose_title = choose.text
    print('click %s'%choose_title)

    vote = driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div[1]/div/div[5]').click()
    

def login():
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__title--1v3XO')))
    fb = driver.find_element_by_xpath('//*[@id="useModal__1"]/div/div/div[1]/div[2]').click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_9axz')))
    username = credentials['ro_login']['username']
    user = driver.find_element_by_id('email').send_keys(username)
    password = credentials['ro_login']['password']
    pwd = driver.find_element_by_id('pass').send_keys(password)
    login = driver.find_element_by_id('loginbutton').click()
    print('登入成功')



if __name__ == '__main__':
    ro()