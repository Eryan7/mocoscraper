from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.by import By
import os
from datetime import datetime
import pandas as pd

CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

url = 'https://countystat.shinyapps.io/rps_app/'
file_directory = os.path.abspath('files')

op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument("--disable-dev-shm-usage")
op.add_argument("--no-sandbox")
op.add_argument("--window-size=1920,1080")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
op.add_argument(f'user-agent={user_agent}')
op.add_experimental_option("prefs", {
    "download.default_directory": file_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
    }
)
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=op)

driver.get(url)
WebDriverWait(driver, 60).until(visibility_of_element_located((By.ID, 'downloadData')))
download1 = driver.find_element(By.ID, 'downloadData')
download1.click()

tab2 = WebDriverWait(driver, 60).until(lambda x: x.find_element(By.XPATH, "//*[text()=''Maryland Police Accountability Act'']"))
tab2.click()
WebDriverWait(driver, 60).until(visibility_of_element_located((By.ID, 'downloadData2')))
download2 = driver.find_element(By.ID, 'downloadData2')
download2.click()

tab3 = WebDriverWait(driver, 60).until(lambda x: x.find_element(By.XPATH, "//*[text()='MCPD Audit']"))
tab3.click()
WebDriverWait(driver, 60).until(visibility_of_element_located((By.ID, 'downloadData3')))
download3 = driver.find_element(By.ID, 'downloadData3')
download3.click()

filedate = datetime.utcnow().strftime("%Y-%m-%d")
file1 = "data-"+filedate+".csv"
file2 = "data2-"+filedate+".csv"
file3 = "data3-"+filedate+".csv"

rpsTable = pd.read_csv(os.path.join(file_directory, file1))
mpaaTable = pd.read_csv(os.path.join(file_directory, file2))
auditTable = pd.read_csv(os.path.join(file_directory, file3))

print(rpsTable)
print(mpaaTable)
print(auditTable)