import requests as req
from bs4 import BeautifulSoup as bs 
import pandas as pd 
import numpy as np 
import pprint as pp
from matplotlib import pyplot as plt
from pandtest import simpleGraph
import  os

if not os.path.exists('keepers.csv'):
	from goat import get_fox_table
	keepers_df = get_fox_table('2017','PL','GOALKEEPING')
	keepers_df.to_csv('keepers.csv',index = False,encoding = 'utf-8')
else:
	keepers_df = pd.read_csv('keepers.csv',header = 0, encoding = 'utf-8')

keepers_df['Save%'] = keepers_df['Saves'].astype(int)/keepers_df['Shots on Goal Against'].astype(int)
keepers_df['SavetoGA'] = keepers_df['Saves'].astype(int)/keepers_df['Goals Allowed'].astype(int)
keepers_df['SavesP90'] = keepers_df['Saves'].astype(int)*90/keepers_df['Minutes Played'].astype(int)

keepers_df['MinutesPStart'] = keepers_df['Minutes Played'].astype(int)/keepers_df['Games Started'].astype(int)

keepers_df.sort_values(['Save%'],inplace=True)
print(keepers_df[['Name','Save%']])


fig, ax = plt.subplots(1,1 ,figsize=(16,12))
plt.subplots_adjust(left = .2, right = .8)


p1 = keepers_df[['Name','Save%','SavetoGA','Saves','SavesP90','MinutesPStart','Team','Minutes Played']]
p1 = p1[p1['Minutes Played'] > 1700]

p1.sort_values(['Save%'],inplace=True)

x_data =  p1['Save%'].as_matrix()

p1.plot.barh(y='Save%',use_index = True, ax = ax,legend=False)
x_ticks = range(len(x_data))

#print(p1)
p1.Name = p1.Name + ' (' + p1.Team + ')' 
title = '   Save Percentage (Saves / Shots on Goal Against)                           '
simpleGraph(ax, 
			title ='\n      '+ title,
			subtitle = '2016-2017 Premier League | GKs with at least 1700 minutes                    ',
			kind = 'barh',
			x_data = x_data,
			y_data = x_ticks,
			tick_str= p1.Name,
			xlims=[0.4,1],
			ylabel = '',
			xlabel = '(Data from Fox Soccer Sports)       ',)
plt.text(.93, max(x_ticks)*1.045, 'u/TM_Data_ ', fontsize = 17,color = '#708090')
'''
p1.sort_values(['Saves'],inplace=True)
x_data =  keepers_df.iloc[1:10,:]['Save%'].as_matrix()
p1.plot.scatter(x='Save%',y='SavetoGA', ax = axs[1])

title = 'Saves Percentage'
simpleGraph(axs[1], 
			kind = 'scatter',
			subtitle= '{} \n {}'.format(title,'Premier League | 2016/2017'),
			x_data = x_data,
			y_data = p1.SavetoGA[1:10],
			tick_str= p1.Name,
			xlabel = 'Saves',
			)



#keepers_df.sort('Save%',inplace=True)
'''
fig.savefig('keepers.png', format = 'png', dpi= 300)
plt.show()