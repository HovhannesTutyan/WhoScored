from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the WebDriver
driver = webdriver.Chrome()  # Ensure you have the Chrome WebDriver installed

# Navigate to Twitter search page
driver.get('https://twitter.com/search?q=Bitcoin&src=typed_query')

# Scroll the page to load more tweets
body = driver.find_element(By.TAG_NAME, 'body')
for _ in range(5):  # Adjust range for more scrolling
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

# Collect tweets
tweets = driver.find_elements(By.XPATH, "//div[@data-testid='tweet']")

for tweet in tweets:
    print(tweet.text)

driver.quit()
