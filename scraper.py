from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import os
from datetime import datetime
import pandas as pd
import numpy as np
import psycopg2
import psycopg2.extras as extras

CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
DATABASE_URL = os.environ['DATABASE_URL']

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
download1 = WebDriverWait(driver, 60).until(lambda x: x.find_element(By.ID, 'downloadData'))
download1.click()

# tab2 = driver.find_element(By.XPATH, "//h4[()='Maryland Police Accountability Act']")
# tab2 = driver.find_element(tab2.parent)
# tab2.click()
# download2 = WebDriverWait(driver, 60).until(lambda x: x.find_element(By.ID, 'downloadData2'))
# url2 = download2.get_attribute('href')
# print(url2)
# driver.get(str(url2))

# driver.get(url)
# tab3 = driver.find_element(By.XPATH, "//h4[text()='MCPD Audit']")
# tab3.click()
# download3 = WebDriverWait(driver, 60).until(lambda x: x.find_element(By.ID, 'downloadData3'))
# url3 = download3.get_attribute('href')
# print(url3)
# driver.get(str(url3))

filedate = datetime.utcnow().strftime("%Y-%m-%d")
file1 = "data-"+filedate+".csv"
file2 = "data2-"+filedate+".csv"
file3 = "data3-"+filedate+".csv"

rpsTable = pd.read_csv(os.path.join(file_directory, file1))
rpsTable.drop(rpsTable.columns[[0]], axis=1, inplace=True)
rpsTable['SSJC Comments'] = np.NaN

# mpaaTable = pd.read_csv(os.path.join(file_directory, file2))
# mpaaTable.drop(mpaaTable.columns[[0]], axis=1, inplace=True)
# mpaaTable['SSJC Comments'] = np.NaN

# auditTable = pd.read_csv(os.path.join(file_directory, file3))
# auditTable.drop(auditTable.columns[[0]], axis=1, inplace=True)
# auditTable['SSJC Comments'] = np.NaN

rpsTable.columns = ['action_id', 'focus_area', 'tf_rec', 'action', 'parties', 'progress', 'timeline', 'priority', 'ssjc_comments']
print(rpsTable)
# print(mpaaTable)
# print(auditTable)

def execute_values(conn, df, table):
  
    tuples = [tuple(x) for x in df.to_numpy()]
  
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS tf_recs (action_id serial PRIMARY KEY, focus_area text, tf_rec text, action text, parties text, progress text, timeline date, priority text, ssjc_comments text);")
cur.close()
# execute_values(conn, rpsTable, 'tf_recs')
conn.commit()
conn.close()