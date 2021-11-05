import time
import yaml
import datetime

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

credentials = yaml.load(open('lay.yml'))


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

    url = credentials['url']
    lay_url = url
    driver.get(lay_url)

    return driver

def vote():
    driver = get_driver()
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__title--1v3XO')))
    vote = driver.find_element(By.XPATH, '//*[@id="promoEntry"]/div[5]/div[2]/div[2]/div[2]/div/div[2]').click()
    username = credentials['login']['username']
    driver.find_element(By.ID, 'email').send_keys(username)

    password = credentials['login']['password']
    driver.find_element(By.ID, 'pass').send_keys(password)
    time.sleep(3)
    driver.find_element(By.ID, 'u_0_0_ta').click()
    print('%s登入成功'%username)
    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="promoEntry"]/div[5]/div[2]/div[2]/div[2]/div/div[2]').click()
    time.sleep(3)
    vote.click()
    driver.save_screenshot('lay.png')
    js = 'window.open(https://www.instagram.com/");'
    driver.execute_script(js)



if __name__ == '__main__':
    vote()