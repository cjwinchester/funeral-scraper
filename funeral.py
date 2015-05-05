from bs4 import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time

driver = webdriver.Chrome()
driver.get("http://www.nebraska.gov/LISSearch/search.cgi")
assert "Nebraska DHHS" in driver.title

def scrapeFunerals():
    business = driver.find_element_by_xpath("//input[@value='E']")
    business.click()
    select = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "profession")
                )
            )
    all_options = select.find_elements_by_tag_name("option")
    for option in all_options:
        if option.get_attribute("value") == "1":
            option.click()
    name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ent_name")
                )
            )
    name.send_keys("%")
    submit = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "gobut")
                )
            )
    submit.click()
    page = driver.page_source
    soup = BeautifulSoup(page)
    links = soup.find_all(href=re.compile('search.cgi\?mode=details'))
    f = open("funeral.txt", "wb")
    f.write("|".join(['name', 'manager', 'address', 'phone', 'profession', 'lic_type', 'lic_no', 'issued', 'expires', 'lic_status', 'reason', 'viols']) + "\n")
    for dude in links:
        driver.get("http://www.nebraska.gov/LISSearch/" + dude['href'])
        page = driver.page_source
        soup = BeautifulSoup(page)
        for e in soup.find_all('br'):
            e.replace_with(" ")
        error = re.compile(r'None on record at this time')
        if error.search(str(soup)):
            viols = ""
        else:
            viols = "x"
        attrs = soup.find_all('div', {'class': 'fieldValue'})
        data = []
        print attrs[0].text
        for thing in attrs:
            data.append(thing.text)
        data.append(viols)
        f.write("|".join(data) + "\n")
        time.sleep(2)
    f.flush()
    f.close()
    driver.close()
    
scrapeFunerals()