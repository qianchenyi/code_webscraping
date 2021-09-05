import urllib.request as urllib2
from bs4 import BeautifulSoup
import json
import csv

# # url = "https://ruffle-for-firefox.en.softonic.com/download"
# url = "https://ccleaner-browser.en.softonic.com/download"
# # url = "https://royal-mail-people-application.en.softonic.com/android/download"

def get_software_download_addr(app_url):

    respone=urllib2.urlopen(app_url)
    html=respone.read()
    soup = BeautifulSoup(html, 'html.parser')
    section = soup.find(name ="section",attrs={"class":"download-module mb-s"})
    if section is None:
        return None
    return section.a["href"] 


def store_json(data):
    with open('app_urls.json', 'w') as fw:
        json.dump(data,fw,indent =0)

windows_url = "https://en.softonic.com/windows/"
categorys = ["security-privacy","games","business-productivity","internet-network","education-reference","multimedia","development","lifestyle"]

cnt = 0
app_urllist=[]

if __name__=='__main__':
    for category in categorys:
        for i in range(1,5):
            if i == 1:
                url = "{}{}:new-apps".format(windows_url,category)	
            else:
                url = "{}{}:new-apps/{}".format(windows_url,category,i)            
            respone=urllib2.urlopen(url)
            html=respone.read()
            soup = BeautifulSoup(html, 'html.parser')
            app_div = soup.find(name="div",attrs={"class":"content content--category content--colored"})
            app_list = app_div.contents[2]
            for app in app_list.contents:
                if app.li is None:
                    continue
                app_url = app.a["href"] + "/download"
                app_name = app.img['alt']
                try:
                    app_download_addr = get_software_download_addr(app_url)
                except:
                    continue
                data = {'name':app_name,'url':app_download_addr}
                app_urllist.append(data)
                if app_download_addr is not None:
                    cnt += 1	
                    if cnt%100 ==0:
                        store_json(app_urllist)		
                    #store_json(app_download_addr)
                    print(app_download_addr)
            print ("\ntotal app count:{}\n".format(cnt))
    