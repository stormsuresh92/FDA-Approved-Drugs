from requests_html import HTMLSession
import pandas as pd
from time import sleep

s = HTMLSession()

def input_url(url):
	r = s.get(url)
	cont = r.html.find('td > div > div.col-md-12 > ul > li')
	data = []
	for drugs in cont:
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
		sleep(0.1)
	return data

def save_data(data):
	df = pd.DataFrame(data, columns=['DrugName', 'Drug Id', 'Application', 'Route', 'Dosage Form', 'Manufacturer'])
	df.to_csv('drug dataset.csv', index=False)

def main():
	url = 'https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=browseByLetter.page&productLetter=Z&ai=0'
	save_data(input_url(url))

if __name__ == '__main__':
	main()
