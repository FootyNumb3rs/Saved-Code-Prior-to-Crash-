import pandas as pd
import requests as req2
from bs4 import BeautifulSoup as bs 
import time
import math

last_num = 5
player_dict = []
col_labels = []
req = req2.Session()
for list_num in range(1,last_num):
	url_base = "http://www.espn.com/espn/feature/story/_/page/worldfame100/espn-world-fame-100-top-ranking-athletes#R"+str(list_num)+"__"
	req.get('http://www.espn.com/espn/feature/story/_/page/worldfame100/espn-world-fame-100-top-ranking-athletes')
	page_source = bs(req.get(url_base).text, 'html.parser')
	athlete_name = page_source.find('div', class_ = 'player-name').get_text()
	print(athlete_name)
	athlete_type = page_source.find('div', class_ = 'athlete-meta').get_text()
	athlete_rank = page_source.find('div',class_= 'number').get_text()
	social_chart = page_source.find('ul',class_ = 'chart')
	data_numbers = social_chart.find_all('div') # Endorsements, Instagram Followers, Facebook Followers, Twitter Followers
	print(data_numbers)
	data_labels = social_chart.find_all('span')
	for i,data in enumerate(data_numbers): 
		print(data_numbers[i].contents[0])
		if data == 'NA': 
			data_numbers[i] = 666
			continue
		multiple = data_numbers[i].contents[0][-1]
		number = float(data_numbers[i].contents[0].replace('M','').replace('K','').replace('$',''))
		if multiple == 'M':
			data_numbers[i] = number*(math.pow(10,6))
		elif multiple == 'K':
			data_numbers[i] = number*(math.pow(10,6))
	#label format ['Name','Rank','Type','Endorsements','Facebook_Followers','Instagram Followers','Twitter Followers']
	
	data_dict = {}

	for i, attr in enumerate(data_labels):
		data_dict[attr.get_text().replace(' ','_')] = data_numbers[i]
	data_dict['Name'] = athlete_name
	player_dict.append(data_dict)
	print(player_dict)
	col_labels = data_dict.keys()

print(player_dict)
print(pd.DataFrame(player_dict))





	





