from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import urllib.request as urllib2

import json
import csv
import time
import re
import requests

chromeOptions = webdriver.ChromeOptions()
prefs = {'safebrowsing.enabled': 'false', "download.default_directory" : r"/Users/jessica/Documents/masterproject/dataset_softonic/"}
chromeOptions.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chrome_options=chromeOptions)

driver.maximize_window()


def downloadSW():
    page ="https://en.softonic.com/windows/"
    categorys = ["security-privacy","games","business-productivity","internet-network","education-reference","multimedia","development","lifestyle"]
    for category in categorys:
        for i in range(1,10):#from page 2 to page 10
            category_page = "{}{}:trending/{}".format(page,category,i)
            print(category_page)
            driver.get(category_page)
            time.sleep(2)
            #find_pos = driver.find_element_by_css_selector('article[class="app-list-item app-list-item--interactive"]')
            blocks = driver.find_elements_by_xpath("//div[@class = 'content content--category content--colored']/ul/li")
            hrefs = []
            for block in blocks:
                app_site = block.find_element_by_tag_name('a')
                href = app_site.get_attribute("href") + "download"
                hrefs.append(href)
            for href in hrefs:
                try:
                    driver.get(href)  
                    download_buttom=driver.find_element_by_css_selector('a[data-meta="button-download-direct"]')

                    app_url = download_buttom.get_attribute("href")
                    
                    app_name = driver.find_element_by_css_selector('h1[class="app-header__name"]').find_element_by_tag_name('a').get_attribute("title")
                    #driver.get(app_url )#open the download page
                    #real_url_str = driver.find_element_by_css_selector('span[class ="js-launch-download"]').get_attribute('data-download')
                
                    respone=urllib2.urlopen(app_url)  
                    html=respone.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    real_url_str = soup.find(name="span",attrs={"class":"js-launch-download"})["data-download"]
                    real_url = json.loads(real_url_str)['downloadUrl']#the download_link

                    #get and analyse the size of file
                    download_link = requests.get(real_url)
                    file_size_str=download_link.headers['Content-Length'] #the type is string
                    file_size=int(file_size_str)/1024/1024 
                
                    if(file_size >=100 ):
                        print("bigger then 100MB")
                        continue
                    else:
                        #TODO:use API to check
                        driver.get(real_url)#download
                except:

                    continue
                #download_buttom.click()
            #    size_str = download_bt.find_element_by_class_name("sub-label").text
            #     str_list = re.split("[()\s]", size_str)           
            #     if str_list[-2] == "GB":
            #         print("bigger then 100MB")
            #         continue
            #     elif str_list[-2] == "MB":
            #         if float(str_list[-3])>100:
            #             print("bigger then 100MB")
            #             continue
                
            #     # app_name = driver.find_element_by_css_selector('h1[class="has-masthead-badges long-title"]').find_element_by_tag_name('a').text
            #     download_bt.click()
                print('Downloading... {} of size {:.2f} M'.format(app_name,file_size))
                time.sleep(5)

            # page = 'https://en.softonic.com/windows/'+str(i)
            # print(page)
        time.sleep(1)

downloadSW()
driver.close()

