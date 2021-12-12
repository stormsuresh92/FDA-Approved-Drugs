from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm

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
file = open('urls.txt', 'r')
urls = file.readlines()
for url in tqdm(urls):
    lists = get_urls(url)
    for res in tqdm(lists):
        mainlist.append(get_label_data(res))
    
df = pd.DataFrame(mainlist)
df.to_csv('lableData.csv', index=False)
print('downloaded')





    
    
