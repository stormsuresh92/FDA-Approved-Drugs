from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm
import logging
from time import sleep

# Set up logging
logging.basicConfig(filename='Logfile.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H-%M-%S')

session = HTMLSession()

headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding':'gzip, deflate, br, zstd',
    'accept-language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'connection':'keep-alive'
}

def get_urls(url):
    baseurl = 'https://www.accessdata.fda.gov'
    r = session.get(url, headers=headers, timeout=10)
    sleep(1)
    datas = r.html.find('ul.collapse li')
    linkdata = []
    for item in datas:
        links = baseurl + item.find('a', first=True).attrs['href']
        linkdata.append(links)   
    return linkdata

def get_label_data(response):
    r = session.get(response, headers=headers, timeout=10)
    sleep(1)
    label_infos = r.html.find('div.panel-group')

    for item in label_infos:
        try:
            ID = item.find('span.appl-details-top', first=True).text
        except:
            ID = ''
        try:
            Company = item.find('#accordion > span > span:nth-child(5)', first=True).text
        except:
            Company = ''
        try:
            DrugName = item.find('#collapseProduct', first=True).text.split('\n')[-8]
        except:
            DrugName = ''
        try:   
            ActiveIngredient = item.find('#collapseProduct', first=True).text.split('\n')[-7]
        except:
            ActiveIngredient = ''
        try:   
            Marketing_Status = item.find('#collapseProduct', first=True).text.split('\n')[-4]
        except:
            Marketing_Status = ''
        try:   
            labelDate = item.find('#exampleLabels > tbody > tr:nth-child(1)', first=True).text.split('\n')[-5]
        except:
            labelDate = ''
        try:   
            labelurl = item.find('#exampleLabels > tbody > tr:nth-child(1) > td:nth-child(4) > a', first=True).attrs['href']
        except:
            labelurl = ''
            
        dic = {
            'ID' : ID,
            'Company': Company,
            'Drug_Name' : DrugName,
            'Active_Ingredient' : ActiveIngredient,
            'Marketing_Status' : Marketing_Status,
            'Label_Date' : labelDate,
            'Label_Urls' : labelurl
        }

        return dic

mainlist = []
try:
    with open('urls.txt', 'r') as file:
        urls = file.readlines()
        for url in tqdm(urls):
            lists = get_urls(url.strip())
            for res in tqdm(lists):
                mainlist.append(get_label_data(res))
except Exception as e:
    logging.error(f"Error processing URLs: {e}")

df = pd.DataFrame(mainlist)
df.to_csv('lableData.csv', index=False)
print('Downloaded')
