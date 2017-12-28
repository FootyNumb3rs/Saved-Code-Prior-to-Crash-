# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

from bs4 import BeautifulSoup
import requests as req
import pandas as pd
import numpy as np
import  pprint as pp
import matplotlib
matplotlib.matplotlib_fname()
import matplotlib.pyplot as plt

from pandtest import simpleGraph




def verticalAdd(frame,name,seasons, competition, avg = False, boolz = None):
	if boolz == None:
		name_df = frame[frame.Name == name]
	else:
		name_df=frame[boolz]
	if boolz:
		name_df=name_df[name_df.Competition==competition]
	lists = []
	for season in seasons: 
		indexes = frame.columns.values[1:10] # numerical indexes
		#print(name_df.loc[name_df.Season == season,][0:1])
		numerical_stats = name_df.loc[name_df.Season == season,indexes][0:5].as_matrix()
		if avg:
			newRow = np.mean(numerical_stats, axis=0).tolist()
		else:
			newRow = np.sum(numerical_stats,axis=0).tolist()
		newRow.insert(0,name)
		newRow.append(season)
		newRow.append(competition)
		lists.append(newRow)
	return(pd.DataFrame(lists, columns = frame.columns.values))

def extractName(name):
	if len(name.split(',')) > 1:
		name = name.split(',')[1].replace('\n',' ')
	else:
		split_name = name.split('\n')
		if split_name[0] not in split_name[1]:
			name = name.replace('\n','')
		else:
			name = split_name[1]

	return(name)

def strip(string):
	if string[0] == ' ':
		return(string[1:])
	else:
		return(string)

'''
# Getting Data

dfs = []
competitions = ['Liga','CL']
for comp in competitions:
	for year in range(2013,2017):
		table_for_year = get_fox_table(str(year), comp)
		dfs.append(table_for_year)

final = pd.concat(dfs)
final.to_csv('goat.csv', index=False, encoding = 'utf-8-sig')
'''
''
# Reading and analyzing data
goat = pd.read_csv('goat.csv', encoding = 'utf-8-sig', header=0)
goat['Name']= goat['Name'].apply(strip) # Removing spaces from beginning of Name



# Combining to produce combined results across competitions
seasons = range(2013,2017)
cr7=verticalAdd(goat,'Cristiano Ronaldo', seasons, 'All Comps') 
messi=verticalAdd(goat,'Lionel Messi',seasons,'All Comps') 
other_players = (goat['Name'] != "Cristiano Ronaldo") & (goat['Name'] != 'Lionel Messi')

other_top_performers=verticalAdd(goat,'Other Players',seasons,'Liga',True,other_players.tolist())
goat = pd.concat([goat,pd.concat([cr7,messi,other_top_performers])])
goat.reset_index(inplace=True) # Concatenation screws with index






#Creating Stats
goat['S%'] = goat['Shots On Goal']/goat['Shots']

#Plotting
cr7_bool = goat['Name'] == "Cristiano Ronaldo"
messi_bool = goat['Name'] == 'Lionel Messi'
other_top_performers = goat['Name'] == 'Other Players'
bools = (cr7_bool | messi_bool | other_top_performers) & (goat.Competition=='Liga')
frame = goat.loc[bools]

#print(frame) 
fig, ax = plt.subplots()
name_groups = frame.groupby('Name')
for group in name_groups:
	#print(group)
	x_data = group[1].Season.as_matrix()
	y_data = group[1].Goals.as_matrix()
	ax.plot(x_data,y_data)
print(group[0] for group in name_groups)
ax.legend([group[0] for group in name_groups])

plt.show()








'''
fig, ax = plt.subplots(nrows=2,ncols=2)

ylim=frame.Goals.max()*(1.5)
print(ylim)
seasons = frame.Season.unique()
seas_iter = 0

data = frame[['Name','Goals','Season']]
data.Season=data.Season#.astype(str)

for name in data.Name.unique():
	temp_data = data.groupby('Name').get_group(name)
	simpleGraph(temp_data.set_index('Season'), kind = 'line',use_index=True, labels = data.Goals.astype(str))


#graph1 = simpleGraph(data.set_index('Season'), kind = 'line',use_index=True, labels = data.Goals.astype(str))
plt.show()
'''
'''
for i in range(len(ax)):
	for j in range(len(ax)):
		data_=frame.loc[frame.Season==seasons[seas_iter],['Name','Goals','Assists','Season']].set_index('Season').sort_index()
		simpleGraph(data_,seasons[seas_iter],  ax=ax[i,j], kind = 'line',ylim = [0,ylim], use_index= True)
		seas_iter+=1
plt.show()
'''

'''
seasons = frame.Season.unique()
graph=None
for i in range(len(seasons)):
	season = seasons[i]
	data = frame
	#fig, axarr = plt.subplots(4, 4)
	#plt.sca(axarr[0, i])
	simpleGraph(data.loc[:,['S%','Goals','Assists']].set_index(data['Name']), 'Comparisons', graph)
	#simpleGraph(pd.Series((data['S%']*100).apply(round).tolist(), index = data['Name']).sort_index(ascending=False) ,season)

plt.show()

'''






















