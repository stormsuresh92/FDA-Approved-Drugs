from requests_html import HTMLSession
import os
from tqdm import tqdm
import logging

session = HTMLSession()

logging.basicConfig(filename='Logfile.log', level=logging.DEBUG, 
                    format='%(asctime)s-%(message)s', datefmt='%d-%b-%y %H-%M-%S')




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
    cur_dir = os.getcwd()
    pdf = cur_dir + '/Downloaded Labels'
    if not os.path.exists(pdf):
        os.mkdir(pdf)

    r = session.get(response)
    label_infos = r.html.find('div.panel-group')
    
    for item in label_infos:
        
        DrugName = item.find('#collapseProduct', first=True).text.split('\n')[-8]
       
        try:   
            labelDate = item.find('#exampleLabels > tbody > tr:nth-child(1)', first=True).text.split('\n')[-5].replace('/', '-')
        except:
            pass
        try:   
            labelurl = item.find('#exampleLabels > tbody > tr:nth-child(1) > td:nth-child(4) > a', first=True).attrs['href']
        except:
            pass
        try:
            with open(pdf + '/' + DrugName.replace(' ', '_') + '_' + labelDate + '.pdf', 'wb') as f:
                pdfs = session.get(labelurl)
                f.write(pdfs.content)
        except:
            pass

    return 


file = open('urls.txt', 'r')
urls = file.readlines()
for url in tqdm(urls):
    lists = get_urls(url)
    for res in tqdm(lists):
        get_label_data(res)
    
input() 
