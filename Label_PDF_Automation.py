from requests_html import HTMLSession
import os
from tqdm import tqdm
import logging

session = HTMLSession()

logging.basicConfig(filename='Logfile.log', level=logging.DEBUG, 
                    format='%(asctime)s-%(message)s', datefmt='%d-%b-%y %H-%M-%S')

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
    datas = r.html.find('ul.collapse li')
    linkdata = []
    for item in datas:
        links = baseurl + item.find('a', first=True).attrs['href']
        linkdata.append(links)
    return linkdata

def get_label_data(response):
    cur_dir = os.getcwd()
    pdf = os.path.join(cur_dir, 'Downloaded Labels')
    if not os.path.exists(pdf):
        os.mkdir(pdf)

    r = session.get(response)
    label_infos = r.html.find('div.panel-group')

    for item in label_infos:
        try:
            DrugName = item.find('#collapseProduct', first=True).text.split('\n')[-8]
            labelDate = item.find('#exampleLabels > tbody > tr:nth-child(1)', first=True).text.split('\n')[-5].replace('/', '-')
            labelurl = item.find('#exampleLabels > tbody > tr:nth-child(1) > td:nth-child(4) > a', first=True).attrs['href']

            with open(os.path.join(pdf, f'{DrugName.replace(" ", "_")}_{labelDate}.pdf'), 'wb') as f:
                pdfs = session.get(labelurl)
                f.write(pdfs.content)
        except Exception as e:
            logging.error(f"Error processing label data: {e}")
            continue

    return

def process_urls(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()

        for url in tqdm(urls):
            lists = get_urls(url.strip())
            for res in tqdm(lists):
                get_label_data(res)
    except Exception as e:
        logging.error(f"Error processing URLs: {e}")

process_urls('urls.txt')
