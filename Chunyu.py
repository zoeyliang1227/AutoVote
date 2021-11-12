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

credentials = yaml.load(open('change.yml'))
timeout = 3

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

    driver = webdriver.Chrome(options = chrome_options, executable_path = 'chromedriver')

    url = credentials['Chunyu_url']
    rice_url = url
    driver.get(rice_url)

    return driver


def rice():    
    try:
        for i in range(1, 6):
            driver = get_driver()
            driver.switch_to.frame('worksFrame')
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'text-info')))
            vote(driver)
            print(i)
            time.sleep(3)
            login(i, driver) 
            time.sleep(10)
            driver.switch_to.frame('worksFrame')
            done_vote = driver.find_element(By.XPATH, '//*[@id="promoEntry"]/div[5]/div[2]/div[2]/div[2]/div/div[2]')
            time.sleep(3)
            done_title = done_vote.text
            if done_title == '已投票':
                print(done_title)
                now = datetime.datetime.now()     #截圖的名稱拼接上日期
                date_time = now.strftime('%Y%m%d')
                fime_time = date_time+str(i)+'.png'
                print(fime_time)
                driver.get_screenshot_as_file('./Chunyu/' + fime_time +'')
                driver.quit()
            else:
                done_vote.click()
                time.sleep(20)
                print(done_title)  
                now = datetime.datetime.now()     #截圖的名稱拼接上日期
                date_time = now.strftime('%Y%m%d')
                fime_time = date_time+str(i)+'.png'
                print(fime_time)
                driver.get_screenshot_as_file('./Chunyu/' + fime_time +'')
                driver.quit()
                r = random.randrange(1,180)
                time.sleep(r)
    finally:
        time.sleep(3)
        driver.quit()

def vote(driver):   
    rice = driver.find_element(By.XPATH, '//*[@id="promoEntry"]/div[5]/div[1]/div/div/div[2]')
    rice_name = rice.text
    rice.click()
    try:
        if rice_name == '無米樂穰滿之禮':
            print(rice_name)
    except NoSuchElementException as NE:
        raise TypeError(rice_name) from NE
    
def login(i, driver):
    driver.find_element(By.XPATH, '//*[@id="promoEntry"]/div[5]/div[2]/div[2]/div[2]/div/div[2]').click()  #click FB 
    time.sleep(3)
    main_page = driver.current_window_handle        # storing the current window handle to get back to dashboard
    for handle in driver.window_handles:            # changing the handles to access login page
        if handle != main_page:
            login_page = handle

    driver.switch_to.window(login_page)             # change the control to signin page
    username = credentials['login' + str(i) +'']['username']
    driver.find_element(By.ID, 'email').send_keys(username) #FB username

    password = credentials['login' + str(i) +'']['password']
    driver.find_element(By.ID, 'pass').send_keys(password) #FB pwd
    time.sleep(3)
    login = driver.find_element(By.NAME, 'login').click()
    print('%s登入成功'%username)
    time.sleep(3)

    driver.switch_to.window(main_page)      # change control to main page

    return i



if __name__ == '__main__':
    rice()