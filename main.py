from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
import time
import uuid

from pymongo import MongoClient
from datetime import datetime
from selenium.webdriver.common.proxy import Proxy, ProxyType

service = Service(executable_path="chromedriver.exe")

driver = webdriver.Chrome(service=service)

proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = "PROXYMESH_URL" 
proxy.ssl_proxy = "PROXYMESH_URL"


options = webdriver.ChromeOptions()
proxy.add_to_capabilities(webdriver.DesiredCapabilities.CHROME)
driver = webdriver.Chrome(service=service, options=options, desired_capabilities=proxy.to_capabilities())

try:
    driver.get("https://twitter.com/login")
    time.sleep(2)

    username = driver.find_element(By.NAME, "session[username_or_email]")
    password = driver.find_element(By.NAME, "session[password]")
    username.send_keys("USERNAME")  
    password.send_keys("PASSWORD")
    password.send_keys(Keys.RETURN)
    time.sleep(5)

    trends = driver.find_elements(By.XPATH, "//span[contains(text(), 'Trending')]")[:5]

    trend_names = [trend.text for trend in trends]
    unique_id = str(uuid.uuid4())
    ip_address = proxy.http_proxy.split("@")[-1].split(":")[0]
    timestamp = datetime.now()

    record = {
        "unique_id": unique_id,
        "trend1": trend_names[0] if len(trend_names) > 0 else None,
        "trend2": trend_names[1] if len(trend_names) > 1 else None,
        "trend3": trend_names[2] if len(trend_names) > 2 else None,
        "trend4": trend_names[3] if len(trend_names) > 3 else None,
        "trend5": trend_names[4] if len(trend_names) > 4 else None,
        "date_time": timestamp,
        "ip_address": ip_address,
    }
    collection.insert_one(record)

finally:
    driver.quit()