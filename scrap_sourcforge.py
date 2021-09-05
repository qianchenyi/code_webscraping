from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import urllib.request as urllib2

import csv
import time
import re
import requests

chromeOptions = webdriver.ChromeOptions()
prefs = {'safebrowsing.enabled': 'false', "download.default_directory" : r"/Users/jessica/Documents/masterproject/dataset_Sourceforge/"}
chromeOptions.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chrome_options=chromeOptions)

driver.maximize_window()


def downloadSW():
    page ="https://sourceforge.net/directory/os:windows/?page=1"

    for i in range(2,100):
        print(page)
        driver.get(page)
        time.sleep(2)
        blocks = driver.find_elements_by_css_selector('li[itemprop="itemListElement"]')[2:]
        print(len(blocks))
        hrefs = []
        for block in blocks:
            app_site = block.find_element_by_css_selector('a[class="button green hollow see-project"]')
            hrefs.append(app_site.get_attribute("href"))
        for href in hrefs:
            try:
                driver.get(href+'files/')  
            
                time.sleep(2)
    
                download_bt=driver.find_element_by_css_selector('a[class="button green big-text download with-sub-label extra-wide"]')
                size_str = download_bt.find_element_by_class_name("sub-label").text
                str_list = re.split("[()\s]", size_str)           
                if str_list[-2] == "GB":
                    print("bigger then 100MB")
                    continue
                elif str_list[-2] == "MB":
                    if float(str_list[-3])>100:
                        print("bigger then 100MB")
                        continue
                # app_name = driver.find_element_by_css_selector('h1[class="has-masthead-badges long-title"]').find_element_by_tag_name('a').text
                download_bt.click()
                # #get the real_download link for VirusTotal
                # indirect_link = download_bt.get_attribute("href")
                # driver.get(indirect_link)
                # html = driver.execute_script("return document.documentElement.outerHTML")
                # soup = BeautifulSoup(html , 'html.parser')
                # r_url=soup.find('noscript')
                # real_url = r_url.meta['content'][7:]
                # real_url_str = soup.find(name="noscript",attrs={"meta":"js-launch-download"})["data-download"]
                # #download the app
                # driver.get(real_url)
                app_name = ' '
                print(f'Downloading... {app_name} of size {str_list[-3]} {str_list[-2]}')
                time.sleep(10)
            except:
                continue
        page = 'https://sourceforge.net/directory/os:windows/?page='+str(i)
    
    time.sleep(1)

downloadSW()
driver.close()
