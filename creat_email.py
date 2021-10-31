import time
import yaml
import datetime
import random
import getpass
import sys, os, time
import random


from threading import Timer
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

credentials = yaml.load(open('gmail.yml'))

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
    # chrome_options.add_argument('headless')                 # 瀏覽器不提供可視化頁面
    chrome_options.add_argument('no-sandbox')               # 以最高權限運行
    chrome_options.add_argument('--start-maximized')        # 縮放縮放（全屏窗口）設置元素比較準確
    chrome_options.add_argument('--disable-gpu')            # 谷歌文檔說明需要加上這個屬性來規避bug
    chrome_options.add_argument('--window-size=1920,1080')  # 設置瀏覽器按鈕（窗口大小）
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--incognito")  # 使用無痕模式。用 selenium開瀏覽器已經很乾淨了，但疑心病重的可以用一下

    driver = webdriver.Chrome(options = chrome_options, executable_path = 'chromedriver')

    url = credentials['creat_yahoo']
    creat_email_url = url
    driver.get(creat_email_url)

    return driver

def creat_gmail():    
    driver = get_driver() 
    for i in range(4, 7):
        lastName = credentials['email_login' + str(i) +'']['lastName']
        LN = driver.find_element(By.ID, 'usernamereg-firstName').send_keys(lastName)

        firstName = credentials['email_login' + str(i) +'']['firstName']
        FN = driver.find_element(By.ID, 'usernamereg-lastName').send_keys(firstName)

        username = credentials['email_login' + str(i) +'']['username']
        user = driver.find_element(By.ID, 'usernamereg-yid').send_keys(username)

        password = credentials['email_login' + str(i) +'']['password']
        pwd = driver.find_element(By.ID, 'usernamereg-password').send_keys(password)

        phone = credentials['email_login' + str(i) +'']['phone']
        phe = driver.find_element(By.ID, 'usernamereg-phone').send_keys(phone)

        # 獲取select下拉框的元素
        ele_select = driver.find_element(By.ID, 'usernamereg-month')

        # 獲取下拉框中所有選項元素（element）
        options = Select(ele_select).options
        # print("所有選項元素的列表：%s" % options)
        # for i in options:
        #     print("元素對應的選項：%s"% i.text)

        # 獲取下拉框當前顯示(選中)的元素(element)
        options_selected = Select(ele_select).all_selected_options
        print("-----------------------分隔符---------------------------")
        print(options_selected)
        for j in options_selected:
            print("當前選中的選項(預設項)：%s" % j.text)

        # 選擇value值為2的選項
        month = random.randrange(1,12)
        Select(ele_select).select_by_value(str(month))

        day = random.randrange(1,30)
        driver.find_element(By.ID, 'usernamereg-day').send_keys(str(day))

        year = random.randrange(1975,2009)
        driver.find_element(By.ID, 'usernamereg-year').send_keys(str(year))
        
        driver.find_element(By.ID, 'reg-submit-button').click()

        driver.find_element(By.XPATH, '///*[@id="phone-verify-challenge"]/form/div[2]/button').click()
        driver.quit()



if __name__ == '__main__':
    # ro()
    creat_gmail()