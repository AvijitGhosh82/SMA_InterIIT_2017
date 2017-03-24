from bs4 import BeautifulSoup
import lxml
import urllib2
import requests
from datetime import datetime,timedelta
from newspaper import Article
import pandas as pd

def fool(ticker):
	with open('links.txt', 'r', encoding='cp1252') as link_file:
		links = link_file.readlines()
		print links
		# links = [link[] for link in links]
	# ticker_symbols = [tickers according to the order in links.txt]
	url = ticker_url
	
	try:
		response = requests.get(url)
		html = response.content
		soup = BeautifulSoup(html, "lxml")

		timestamp = []
		title = [] 
		urls = []
		content = []

		articles = 	soup.findAll('article')
		error_file = open('error_daylink.txt', 'w+')
		error_file_1 = open('error_day-sublink.txt', 'w+')

		for article in articles:
			try:
				times = article[i].text[len(article[i].find('a').text):article[i].text.find('•')]
				dates = fool_date(timestamp)
				today = datetime.now().day
				print(date, today)
				if(abs(date - today) in [1,2]):''
					heading = article
					link = 'https:' + article[i].find('a')['href']
					try:
						subresponse = requests.get(link)
						subhtml = subresponse.content
						subsoup = BeautifulSoup(subhtml)
						division = subsoup.find('span', {'class': 'article-content'})
						content.append(division.text)
						timestamp.append(times)
						urls.append(link)
						title.append(heading)
					except Exception as e:
						print(e, subdict['link'])
                        print(subdict['link'], end = "\n", file = error_file_1)
                        continue
			except Exception as e:
                print(e, daylink)
                print(daylink, end = "\n", file = error_file)
				continue

error_file.close() 
error_file_1.close()
