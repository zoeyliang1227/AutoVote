# import schedule
import time
import yaml
import datetime
import random

import pandas as pd
# from bs4 import BeautifulSoup
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
lists=[]



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
    r = driver.get(ro_url)

    return driver


def check_vote(): 
    # df = pd.DataFrame(lib, columns=['編號', '讚數'])

    # with open('ro.csv', 'w') as csvfile:
    #     writer = csv.writer(csvfile)
    #     # writer = csv.DictWriter(csvfile, sorted(lib), delimiter=',')
    #     writer.writerow(['編號', '讚數'])
    try:
        driver = get_driver()
        now = datetime.datetime.now()
        print(now)
        choose = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[2]/div[2]')
        choose.click()
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__active--1YiWY')))
        choose_title = choose.text
        print('click %s'%choose_title)
        time.sleep(5)
        first = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div[1]/div/div[2]')
        first_text = first.text
        print(first_text)
        if first_text == '最初的感動':
            for i in range(1, 9):
                print(i)
                work = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div')
                work_list = work.find_elements(By.CLASS_NAME, 'style-module__work-index--dQ6HD')
                work_len = len(work_list)
                # print(work_len)
                for n in range(1, work_len+1):
                    # print(n)
                    time.sleep(3)
                    number = driver.find_element(By.XPATH, '//*[@id="root"]/*[name()="div"]/*[name()="div"][4]/*[name()="div"][1]/*[name()="div"][4]/*[name()="div"]/*[name()="div"]['+ str(n) + ']/*[name()="div"]/*[name()="div"][1]/*[name()="span"][2]')
                    number_name = number.text
                    # print(number_name)
                    time.sleep(1)
                    work = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div['+ str(n) + ']/div/div[6]/div[1]/span')
                    work_name = work.text
                    # print(work_name)
                    in_work_name = int(work_name)
                    lib[number_name] = in_work_name
                    # lists.append(in_work_name)
                    
                    # for key, value in lib.items():
                    #     writer.writerow([key, value])
                    
                if i == 5:
                    time.sleep(1)
                    driver.find_element(By.XPATH, "//span[text()='下一頁']").click()
                else:
                    if i <= 5:
                        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div[9]/div/span['+ str(i + 1) + ']').click()
                    else:
                        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div[9]/div/span['+ str(i - 5) + ']').click()
            # print(lib)
            # rank = dict(sorted(lib.items(), key=lambda item: item[1], reverse = True))
            # print(rank)
            df = pd.DataFrame(list(lib.items()), columns = ['編號', '讚數'])
            # print(df)
            df_sort = df.sort_values(['讚數'], ascending=False)
            new_df = df_sort.head(10)  #依照欄位內容來進行排序
            print("遞減排序")
            print(new_df)
            df_sort.to_csv('ro.csv', header=None, index=None, encoding='utf-8', columns = ['編號', '讚數'])
            
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == '__main__':
    check_vote()