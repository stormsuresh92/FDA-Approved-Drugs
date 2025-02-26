from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm

s = HTMLSession()


headers = {
	'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	'accept-encoding':'gzip, deflate, br, zstd',
	'accept-language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
	'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
	'connection':'keep-alive'
}

def input_url(url):
	r = s.get(url, headers=headers, timeout=10)
	cont = r.html.find('td > div > div.col-md-12 > ul > li')
	data = []
	for drugs in tqdm(cont):
		drug = drugs.text.split('|')[-4].strip()
		ids = drugs.text.split('|')[-3].split('#')[-1].strip()
		app = drugs.text.split('|')[-3].split('#')[-2].strip()
		roa = drugs.text.split('|')[-2].split(';')[-1].replace(' ', '').strip()
		try:
			roaa = drugs.text.split('|')[-2].split(';')[-2].replace(' ', '').strip()
		except:
			roaa = 'None'
		manu = drugs.text.split('|')[-1].strip()
		data.append([drug, ids, app, roa, roaa, manu])

	return data

def save_data(data):
	df = pd.DataFrame(data, columns=['DrugName', 'Drug Id', 'Application', 'Route', 'Dosage Form', 'Manufacturer'])
	df.to_csv('drug dataset.csv', index=False)

def main():
	#Product Names Beginning with alphabet order
	url = 'https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=browseByLetter.page&productLetter=Z&ai=0'
	save_data(input_url(url))

if __name__ == '__main__':
	main()
