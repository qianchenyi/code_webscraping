import requests
import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
import json
import os
import wget

json_file = "/Users/jessica/Desktop/hello/app_urls.json"
url='https://en.softonic.com/download/turbo-vpn/windows/post-download'
#url = "https://en.softonic.com/download-launch?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb3dubG9hZFR5cGUiOiJpbnRlcm5hbERvd25sb2FkIiwiZG93bmxvYWRVcmwiOiJodHRwczovL2dzZi1mbC5zb2Z0b25pYy5jb20vYjk0LzBhMC8wM2YzYzZmNzJkYWVjY2M2MmExMjg0Y2RmZTc5ZDVmZDg2L3N1bmRheS1tb2QtZm5mX3YwNzE0NC56aXA_RXhwaXJlcz0xNjI5NjAwNTc3JlNpZ25hdHVyZT1mOTc2YjA5MDYzNzZiYTA3MmQ3ODY1NDI4M2JiYTBlNjQxZmNkNmJlJnVybD1odHRwczovL3N1bmRheS1tb2QtZm5mLmVuLnNvZnRvbmljLmNvbSZGaWxlbmFtZT1zdW5kYXktbW9kLWZuZl92MDcxNDQuemlwIiwiYXBwSWQiOiJmNzM3YzQ5Yy05NzM3LTRjNmQtOTY3Yy05MDk3ZGY1MTQ5ZDAiLCJwbGF0Zm9ybUlkIjoid2luZG93cyIsImlhdCI6MTYyOTU2MTY4MSwiZXhwIjoxNjI5NTY1MjgxfQ.IpZCmYCxRh2HE2tipci17oejHuH-jFb0_o9qlIl5sBc"

def url_process(url):
    r=requests.get(url)
    try:
        file_size_str=r.headers['Content-Length'] #提取出来的是个数字str
    except:
        respone=urllib2.urlopen(url)
        html=respone.read()
        soup = BeautifulSoup(html, 'html.parser')
        app_div = soup.find(name="div",attrs={"class":"message-download mb-s"})
        data_download = app_div.span["data-download"]
        url = json.loads(data_download)['downloadUrl']
        
        download_link = requests.get(url)
        file_size_str=download_link.headers['Content-Length'] #提取出来的是个数字str
        
    file_size=int(file_size_str)/1024/1024    #把提取出数字str转为int或者float进行运算 
    return url,file_size

with open(json_file) as f:
    data = json.load(f,strict = False)


#todo,bigger than 1 m return
for i in data:
    na = i['name']
    name = re.sub(r"[^a-zA-Z0-9]","",na)
    a = i['url']
    try:
        url,file_size = url_process(a)
        if file_size>100:
            continue
    except:
        continue
    filepath ='/Users/jessica/Documents/masterproject/softonic/'+name+'.exe'
    try :
        if not os.path.exists(filepath):
            continue
        #urllib2.urlretrieve(url,filepath)
        wget.download(url)
        print('successful '+name)
        
    except:
        print('can not get '+name)
        continue


# url_data = json.load(json_file)
