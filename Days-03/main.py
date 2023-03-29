from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from bs4 import BeautifulSoup as soup
import pandas as pd
from pymongo import MongoClient


client = MongoClient("mongodb+srv://radionmatt:oSXHymXK3AwO1iDZ@cluster0.gd8xi8b.mongodb.net/?retryWrites=true&w=majority")
db = client.test
collection = db.vin_data

df_vin = pd.read_csv('vin_11.csv')
vin = []

def policy_kill(driver):
      time.sleep(5)
      try:
        close_btn=driver.find_element(By.CLASS_NAME,'privacy_policy-close')
        close_btn.click()
        print('...(Privacy policy div intercepted and closed)')
      finally:
        print('...(Privacy policy div checked)')
      return True
    
def web_scrap():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--disable-extensions")

  for i in df_vin['vin_11'][10:30]:
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.autodna.com/")

    ## Finding Elements
    search = driver.find_element(By.CLASS_NAME, 'vin-input')
    search.send_keys(i + '123456')
    policy_kill(driver)
    driver.find_element(By.CLASS_NAME, 'vin-btn').click()
    time.sleep(10)
    Marque = driver.find_element(By.XPATH,'//*[@id="vehicle-general"]/div/div/div[2]/div/strong').text
    tab={'vin_11':i,'Make':Marque}
    print(tab)
    collection.insert_one(tab)
    vin.append(tab)
    driver.quit()

  collection.insert_many(tab)


  with open('data-vin.json', 'w') as outfile:
    json.dump(vin, outfile)
  df = pd.read_json('data-vin.json')
  df.to_csv('data-vin.csv',index=False)

if __name__ == "__main__":
  web_scrap()