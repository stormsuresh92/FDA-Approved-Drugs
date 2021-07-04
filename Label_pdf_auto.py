from os import write
from requests_html import HTMLSession
import os

session = HTMLSession()


def get_urls(url):
    baseurl = 'https://www.accessdata.fda.gov'
    r = session.get(url)
    datas = r.html.find('ul.collapse li')
    linkdata = []
    for item in datas:
        links = baseurl + item.find('a', first=True).attrs['href']
        linkdata.append(links)   
    return linkdata

def get_label_data(response):

    r = session.get(response)
    label_infos = r.html.find('div.panel-group')
    
    for item in label_infos:
        
        DrugName = item.find('#collapseProduct', first=True).text.split('\n')[-8]
       
        try:   
            labelDate = item.find('#exampleLabels > tbody > tr:nth-child(1)', first=True).text.split('\n')[-5].replace('/', '-')
        except:
            labelDate = '-'
        try:   
            labelurl = item.find('#exampleLabels > tbody > tr:nth-child(1) > td:nth-child(4) > a', first=True).attrs['href']
        except:
            labelurl = 'No label'
        try:
            with open(DrugName.replace(' ', '_') + '_' + labelDate + '.pdf', 'wb') as f:
                pdfs = session.get(labelurl)
                f.write(pdfs.content)
                print(f'{DrugName}', 'downloaded')
        except:
            pass
    return 


file = open('urls.txt', 'r')
urls = file.readlines()
for url in urls:
    lists = get_urls(url)
    for res in lists:
        get_label_data(res)
    
    