#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from time import sleep
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException

from typing import List, Tuple
import tkinter as tk

def endYear():
    time = datetime.now()
    return time.year - 1911 - 1 + (time.month+4) //6 //2

def getLoginInfomation():
    data = open('account', 'r', encoding='utf-8').readlines()
    return data[0].strip(), data[1].strip()

def getScores(messageLabel: tk.Label = None):
    def find_element(by: str = By.ID, value: Tuple[str, None] = None, timeout: float = 10) -> WebElement:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def find_elements(by: str = By.ID, value: Tuple[str, None] = None, timeout: float = 10) -> List[WebElement]:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((by, value))
        )

    def log(text: str):
        if messageLabel is not None:
            messageLabel.config(text = messageLabel.cget('text') + text)

    account, password = getLoginInfomation()
    if account is None or password is None:
        log(f'請先填寫.env\n')
        return None
    elif(not account.isdecimal()):
        log(f'學號 {account} 並非正確的陽明交通大學學號\n')
        return None
    elif len(account) == 7:
        startyear = int(f'1{account[0:2]}')
    elif len(account) == 9:
        startyear = int(f'1{account[1:3]}')
    else:
        log(f'學號 {account} 並非正確的陽明交通大學學號\n')
        return None

    log('安裝最新版的chrome driver... ')
    try:
        chromedriver_autoinstaller.install()
    except:
        log('網路錯誤，請檢查網路連線\n')
        return None

    log('完成\n')
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument('log-level=2')

    log('建立selenium瀏覽器... ')
    driver = webdriver.Chrome(options=chrome_options)
    log('成功\n')
    driver.maximize_window()

    driver.get('https://portal.nycu.edu.tw/#/login?redirect=%2F')
    log('進入portal\n')
    sleep(0.2)
    log('登入中... ')
    find_element(By.ID, 'account').send_keys(account)
    find_element(By.ID, 'password').send_keys(password)
    find_element(By.CLASS_NAME, 'login').click()
    
    try:
        find_element(By.XPATH, '//a[text()="校園單一入口"]', 5)
    except TimeoutException:
        log('學號或密碼錯誤\n')
        open('account', 'w').write('')
        return None
    
    log('完成\n')
    sleep(0.2)

    log('進入學籍成績系統... \n')
    driver.get(f'https://portal.nycu.edu.tw/#/redirect/regist')
    try:
        find_element(By.ID, 'objTopMenu_lbnToGrd', 5)
    except TimeoutException:
        log(f'無成績資料。請確認是否開啟VPN\n')
        return None

    driver.get(f'https://regist.nycu.edu.tw/p_student/grd_stdscoreedit.aspx')

    tbodys = find_elements(By.XPATH, '//table[@class="table" and @border="1"]', timeout=5)

    titles = []
    ret = []
    for tbody in tbodys:
        title = tbody.find_element(By.XPATH, './/../../../../tr/td/span').text
        titles.append(title)
        log(f'正在取得{title}... ')

        ths = tbody.find_elements(By.XPATH, './/tr/th')
        tds = tbody.find_elements(By.XPATH, './/tr[@class="table_text" or @class="table_alt"]/td')
    
        cur = {}
        cur_semester = []
        for i in range(len(tds)):
            cur[ths[i%len(ths)].text] = tds[i].text

            if (i+1)%len(ths) == 0:
                cur_semester.append(cur)
                cur = {}
        ret.append(cur_semester)

        log(f'完成\n')
    log(f'關閉連線，即將顯示成績...\n')
    driver.close()

    return titles, ret

# data = getScores()
# open('ret.json', 'w', encoding='utf-8').write(str(data))