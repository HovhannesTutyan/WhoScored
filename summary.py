import json
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
try:
    elements = driver.find_elements(By.CLASS_NAME, 'grid-ghost-cell')
    elemenets_count = int(len(elements)) 
    for i in range(1, elemenets_count):
        data.append({
            'name': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[1]'%i).text.strip(),
            'age':driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[1]/span/span[1]'%i).text.strip(),
            'positon': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[1]/span/span[2]'%i).text.strip(),
            'height': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[3]'%i).text.strip(),
            'weight': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[4]'%i).text.strip(),
            'appearance': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[5]'%i).text.strip(),
            'minPlayed': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[6]'%i).text.strip(),
            'goal': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[7]'%i).text.strip(),
            'assistsTotal': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[8]'%i).text.strip(),
            'yellowCard': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[9]'%i).text.strip(),
            'redCard': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[10]'%i).text.strip(),
            'shotsPerGame': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[11]'%i).text.strip(),
            'passSuccess': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[12]'%i).text.strip(),
            'aerialWonPerGame': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[13]'%i).text.strip(),
            'manOfTheMatch': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[14]'%i).text.strip(),
            'rating': driver.find_element(By.XPATH, '//*[@id="player-table-statistics-body"]/tr[%s]/td[15]'%i).text.strip()
        })
    print(data)
    df = pd.json_normalize(data)
    df.to_csv('summary.csv', index=False)
except Exception as X:
    print(X)
    