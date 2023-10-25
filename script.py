import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import datetime
import re
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

today = datetime.date.today()
last_week = today - datetime.timedelta(days=1)

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

url = f"https://cryptopotato.com/category/crypto-news/page/"


num_pages = 1
page_links = []
import random
data_links = []

for page in range(num_pages + 1):
    page_url = f"{url}{page}"
    time.sleep(random.uniform(1, 15))
    driver.get(page_url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('h3.media-heading a')

    date_elements = soup.find_all("time", class_="date")
    date_list = []

    for date_element in date_elements:
        date_string = date_element.a.text.strip()
        date_list.append(date_string)

    count = 0
    for date_str in date_list:
        date_obj = datetime.datetime.strptime(date_str, "%b %d, %Y").date()
        if last_week < date_obj <= today:
            count += 1
            print(date_obj)

    if count > 0:
     
        new_list = [link['href'] for link in links[:count]]
        data_links.extend(new_list)
    else:
        break

driver.quit()

final_links = []
for link in data_links:
    try:
        final_links.append(link)
    except:
        pass

print(len(final_links))

titles = []
bodies = []
dates = []
count = 1

for link in final_links[:-17]:
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find("div", class_="page-title").find("h1").text
        body = soup.find("div", class_="entry-content col-sm-11").text
        date = soup.find("span", class_="last-modified-timestamp").text
        titles.append(title)
        bodies.append(body)
        dates.append(date)
        time.sleep(random.uniform(1, 15))
        count += 1
    except:
        print("An error occurred")

import pandas as pd
df = pd.DataFrame({'Title': titles, 'Content': bodies, 'Date': dates})

# Save the CSV file with the current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
#csv_file_name = f"crypto_{current_date}.csv"
csv_file_name = "crypto.csv"
df.to_csv(csv_file_name, index=False)
