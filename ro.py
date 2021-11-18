# import schedule
import time
import yaml
import datetime
import random
# import getpass

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
    # ro_url = 'https://rox.gnjoy.com.tw/roxfanart?work_id=19&fbclid=IwAR1qefjezAqYl8yjg1AXYgLaz6peT3tuzCuoxaLX9a6P2OIDJrUoA4dlzMY'
    # driver.implicitly_wait(20) # 隱式等待，最長等20秒

    url = credentials['ro_url']
    ro_url = url
    driver.get(ro_url)


    return driver


def ro():    
    try:
        for i in range(1, 25):
            if i == 6 or i == 15 or i == 14:
                pass
            else:
                driver = get_driver()
                # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__title--1GEE0')))
                vote(driver)
                print(i)
                time.sleep(3)
                login(i, driver)            
                driver.refresh()
                time.sleep(3)
                vote(driver)
                time.sleep(3)
                done_vote = driver.find_element(By.XPATH, '//*[@id="useModal__3"]/div/div/div[1]/div[1]')
                time.sleep(3)
                done_title = done_vote.text
                if done_title == '作品當天已投過票':
                    print(done_title)
                    # driver.refresh()
                    # time.sleep(3)
                    # logout = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/span')
                    # logout_name = logout.text
                    # logout.click()
                    # print(logout_name)
                    driver.quit()
                else:
                    print(done_title)  
                    print('太感謝你了٩(●˙▿˙●)۶…⋆ฺ')
                    get_vote = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div[4]/div[1]/div[4]/div/div[1]/div/div[6]/div[1]/span')
                    votes = get_vote.text
                    print('目前票數%s'%votes)

                    driver.quit()
                    r = random.randrange(1,180)
                    time.sleep(r)
    finally:
        time.sleep(3)
        driver.quit()

def vote(driver):     
    choose = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[2]/div[2]')
    choose.click()
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__active--1YiWY')))
    choose_title = choose.text
    print('click %s'%choose_title)

    time.sleep(5)
    vote = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div[1]/div/div[5]')
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__title--2JLqT')))
    devil = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[4]/div[1]/div[4]/div/div[1]/div/div[2]')
    name = devil.text
    print(name)
    try:
        if name == '惡魔波利👿':
            vote.click()
    except NoSuchElementException as NE:
        raise TypeError(name) from NE
    
def login(i, driver):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'style-module__title--1v3XO')))
    driver.find_element(By.XPATH, '//*[@id="useModal__1"]/div/div/div[1]/div[2]').click()  #click FB 
    username = credentials['ro_login' + str(i) +'']['username']
    driver.find_element(By.ID, 'email').send_keys(username) #FB username

    password = credentials['ro_login' + str(i) +'']['password']
    driver.find_element(By.ID, 'pass').send_keys(password) #FB pwd
    time.sleep(3)
    login = driver.find_element(By.ID, 'loginbutton').click()
    print('%s登入成功'%username)
    time.sleep(3)

    return i



if __name__ == '__main__':
    # input_id = input('Your FB ID:')
    # input_password = getpass.getpass('Your FB password') 
    ro()
    # main()