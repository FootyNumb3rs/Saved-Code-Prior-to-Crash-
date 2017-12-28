import json 
import pprint as pp
import numpy as np
import requests
import collections, soccer 
from tabulate import tabulate

#
# Champions League ScoreBoard
# Champions League is tourament consisting of the best teams(clubs) from various countries around the world.
# This is the single biggest intercountry club tourament in the world. 
# This tool groups CL teams by country (league essentially), and monitors performances of each country(league) in the tournament.
# Only teams in the country's best league are sent. i.e Premiere League from England, La Liga from Spain
# Henceforth, a country in the program really represents the best league from that country.
# Countries can send more than one team. The number of teams they send varys according to offical FIFA coefficent.

# Enjoy

base = 'http://api.football-data.org'
add = '/v1/competitions/440/fixtures'
url = base + add
item = requests.get(url,  headers = { 'X-Auth-Token': '732c6cba888e45809a463888b61f0bb3', 'X-Response-Control': 'minified'})
item = item.json()
tableIndex = []
table = np.array([[99,99, 99, 99 ,99]], float)
print table.shape

scores = {} # items are country records in the form .... 'country' : [Wins, Loses, Draws] 
tableData = [['Country (League)', 'Wins', 'Losses', 'Draws', 'Points Per Game']] # header for table
tableData2 = tableData
checkedTeams = soccer.giveList() #the soccer module contains a list of teams with their corresponding 
use = 0

for match in item['fixtures']:
	if match['status'] != 'TIMED':
		winner = None
		loser = None
		homeTeamGoals = match['result']['goalsHomeTeam']
		awayTeamGoals = match['result']['goalsAwayTeam']
		tie = None
		tempList = []

		if homeTeamGoals > awayTeamGoals:
			winner = 'home'
			loser = 'away'

		elif awayTeamGoals > homeTeamGoals:
			winner = 'away'
			loser = 'home'

		else: # TIE CASE
			winner = 'home'
			loser = 'away'
			tie = True

		try: # Place-holder for now. I will find a more efficient way to do this
	
			for team in [winner, loser]: # ['home','away']...
				teamName = match[team + 'TeamName']

				if  teamName in checkedTeams:  # We already have the team's country 
					teamCountry = checkedTeams[teamName] 

				else:
					teamId = match[team + 'TeamId']
					teamCountry = soccer.clubCountry(teamId) # Else, retrieve the team country
					use  +=  1
					checkedTeams[teamName] = teamCountry #Add team, country to checked teams
				
				if teamCountry not in tableIndex:
					tableIndex.append(teamCountry)
					tableId = tableIndex.index(teamCountry)
					table = np.append(table, [[tableId, 0 , 0 , 0, 0]] ,0)

				tempList.append(teamCountry)


			if tie:
				for count in tempList:
					iD = tableIndex.index(count) # Column 0 are IDs 
					table[iD + 1, 3] += 1 

			else:
				for i in range(len(tempList)):
					country = tempList[i]
					iD = tableIndex.index(country)
					teamIndex = np.where(table[:,0] == iD)
					table[teamIndex, i + 1] += 1 

		
			scores = soccer.score(tempList[0], tempList[1], scores, tie)
			
			#print 'Use = ' + str(use)

		except:
			print 'Error - ' + str(winner) # Just a checking mechanism if TeamName doesn't execute correctly
		#print (checkedTeams) # checking.
		#print 'USE: ' + str(use)
	else:
		break	
table = np.delete(table,0,0)


print table
v = np.array(np.sum(table[:,1:4], axis = 1), float)
print v

table[:,4] = ((table[:,1]*3) + (table[:,3])) /  v
print table

q = np.argsort(table[:,4])
q = q[::-1]
table = table[q]

for i in table:
	tableData2.append( [ tableIndex[int(i[0])]  , int(i[1]), int(i[2]), int(i[3]), np.around(i[4], decimals = 2) ])

print '          Champions League 2016/2017 Group Stage'
print tabulate(tableData2)
#print table, tableIndex

