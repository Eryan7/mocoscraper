from selenium import webdriver
import os

CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

url='https://countystat.shinyapps.io/rps_app/'

op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument("--disable-dev-shm-usage")
op.add_argument("--no-sandbox")
op.add_argument("--window-size=1920,1080")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
op.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)

driver.get(url)
download1 = driver.find_element_by_id('downloadData')
download1.click()

tab2 = driver.find_element_by_xpath("//*[text()='Maryland Police Accountability Act']");
tab2.click()
download2 = driver.find_element_by_id('downloadData2')
download2.click()

tab3 = driver.find_element_by_xpath("//*[text()='MCPD Audit']");
tab3.click()
download3 = driver.find_element_by_id('downloadData3')
download3.click()