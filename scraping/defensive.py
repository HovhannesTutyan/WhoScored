import json
import time
import sqlite3
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service



chrome_service  = Service(r'C:\Users\User\Desktop\WEB_SCRAPING\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=chrome_service, options=options)
website = "https://www.whoscored.com/Teams/36/Show/Germany-Bayer-Leverkusen"
driver.get(website)
data = []
driver.find_element(By.XPATH, '//*[@id="team-squad-stats-options"]/li[2]/a').click()
time.sleep(2)
try:
    elements = driver.find_elements(By.CLASS_NAME, 'grid-ghost-cell')
    elemenets_count = int(len(elements)) 
    for i in range(1, elemenets_count-25):
        data.append({
            'name' :driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[1]'%i).get_attribute('innerText').strip(),
            'age':driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[1]/span/span[1]'%i).get_attribute('innerText').strip(),
            'positon': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[1]/span/span[2]'%i).get_attribute('innerText').strip(),
            'height': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[3]'%i).get_attribute('innerText').strip(),
            'weight': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[4]'%i).get_attribute('innerText').strip(),
            'appearance': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[5]'%i).get_attribute('innerText').strip(),
            'minPlayed': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[6]'%i).get_attribute('innerText').strip(),
            'tackles': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[7]'%i).get_attribute('innerText').strip(),
            'inter': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[8]'%i).get_attribute('innerText').strip(),
            'fouls': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[9]'%i).get_attribute('innerText').strip(),
            'offsides': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[10]'%i).get_attribute('innerText').strip(),
            'clear': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[11]'%i).get_attribute('innerText').strip(),
            'drb': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[12]'%i).get_attribute('innerText').strip(),
            'blocks': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[13]'%i).get_attribute('innerText').strip(),
            'ownG': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[14]'%i).get_attribute('innerText').strip(),
            'rating': driver.find_element(By.XPATH, '//*[@id="team-squad-stats-defensive"]//*[@id="player-table-statistics-body"]/tr[%s]/td[15]'%i).get_attribute('innerText').strip()
        })
    df = pd.json_normalize(data)
    print(df)
    df.to_csv('summary1.csv', index=False)
except Exception as X:
    print(X)
    