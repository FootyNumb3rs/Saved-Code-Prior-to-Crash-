from __future__ import unicode_literals
import pprint as pp
import requests 
import soccer
import statistics
from babel import numbers
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import ticker as tick
import matplotlib.ticker as plticker
from matplotlib.ticker import FormatStrFormatter
from StringIO import StringIO
import urllib, cStringIO
import cv2
from PIL import Image 
from io import BytesIO
matplotlib.style.use('ggplot')


# The point of this program is to assess the price trends of teams in a particular league.
# Provided the leauge(leaugeId), the tool calculates mean player price for each team. This is the green bar
# It also calculates, how much, on average, players less expensive than the mean cost, and those more expensive
# than the mean. These are what the thin blue lines indicate. 

# Still making tweaks


leagueId = 440

def leaguePrice(leagueId):
	teamDict = soccer.idList(leagueId) #  retrieves TeamName:TeamId list given leagueCode  
	teamNames = [] # team names will be appended to this 
	meanList = [] # upper and lower means will be appended as 2-D lists corresponding to team names 
	teamMeanPrices = [] #means for each team name is added here 
	teamVals = []
	higherTier = []

	for teamName, teamInfo in teamDict.iteritems(): #Team names are the key
		#teamId =  teamDict[teamName] #get id given teamName - I could do this better.
		squad = soccer.getPlayers(teamInfo[0]) #teamInfo[0] == teamId
		prices = np.array([])


		for player in squad: 
			try:
				price = player['marketValue'].split(' ')[0].split(',') #remove unicode dollar symbol
				price = int(''.join(price)) # recombines array to form original number
				prices = np.append(prices, price) # appends team price to list o fprices

			except:
				pp.pprint (player['name'] + ': No price') # if marketValue is None, it doesn't have .split method

		if prices !=  []: # entire team with no marketvalue throws error, otherwise
			teamVal = sum(prices)
			mean = statistics.mean(prices)	# calculate mean of all players prices

			lowerThanAverage = np.where(prices < mean)
			higherThanAverage = np.where(prices > mean)

			#higherTier.append(len(higherThanAverage[0]))

			lowerMean = statistics.mean(-1*(prices[lowerThanAverage])) #mean of price differences above mean player price
			higherMean = statistics.mean(prices[higherThanAverage] )  # the same of price differences above the mean
			# How expensive, on average, are players that cost above and below the mean. 

			footballClub = ['AFC','FC', 'CF'] # so 'Real Madrid CF' becomes 'Real Madrid', 
											  # 'FC Barcelona' becomes 'Barcelona' etc.
			for i in footballClub:
				try:
					teamName = teamName.split(i)
					teamName = ''.join(teamName)
				except: # Works for now. I  know to avoid in the future.
					pass
			#teamName = teamName[0:len(teamName) -1 :1]

			teamNames.append(teamName)
			meanList.append([lowerMean,higherMean])
			teamMeanPrices.append(mean)
			teamVals.append(teamVal)
		else:
			print 'Problem' #  just a checking mechanism. Doesn't indicate actual problem.

	teamNames = np.array(teamNames)
	meanList = np.array(meanList)
	teamMeanPrices = np.array(teamMeanPrices)
	teamVals = np.array(teamVals)
	#higherTier = np.array(higherTier)


	sortIndex = np.argsort(teamMeanPrices) 
	sortIndex = sortIndex[::-1]
	#print sortIndex

	#DATA POINTS
	lowerMeans = meanList[:,0]
	upperMeans = meanList[:,1]
	asymmetryBars = [(lowerMeans/1e6)[sortIndex], (upperMeans/1e6)[sortIndex]] # 1e6 to so I can express in millions.

	x = range(len(teamMeanPrices)) # placeholder for team names
	print x 

	#asymmetryBars = asymmetryBars[sortIndex]
	teamMeanPrices = teamMeanPrices[sortIndex]
	teamNames = teamNames[sortIndex]
	teamVals = teamVals[sortIndex]
	#higherTier = higherTier[sortIndex]

	for i in range(0, teamMeanPrices.size):
		print teamNames[i] + ': ' + str(upperMeans[sortIndex][i]/teamMeanPrices[i] )
	print upperMeans[sortIndex]/teamMeanPrices

	#PLOT
	fig = plt.figure()
	ax = plt.subplot(111)
	tick = plt.xticks(x, teamNames, rotation='vertical')
	plt.gca().yaxis.set_major_formatter(FormatStrFormatter('\u20ac %dM'))


	ax2 = ax.twinx()
	tVals = ax.bar(x, teamVals/1e7, color = 'y', align = 'center')
	ax.set_ylabel('Average Player Value', color = 'g')
	for tick1 in ax.get_yticklabels():
		tick1.set_color('g')
	plt.gca().yaxis.set_major_formatter(FormatStrFormatter('\u20ac %dM'))

	avgVals = ax2.bar(x, teamMeanPrices/1e5, color='g', tick_label = teamNames, align = 'center')
	#ax2.errorbar(x, teamMeanPrices/1e5, yerr=asymmetryBars, fmt='o')
	ax2.set_ylabel('AvgVals', color = 'y')
	for tick2 in ax2.get_yticklabels():
		tick2.set_color('y')


	plt.yticks(np.arange(0, 900, 100))
	#print teamVals/1e7
	#print teamMeanPrices/1e6
	plt.title('Champions League')
	

	ax.grid(True)
	ax2.grid(False)


	## ANNOTATIONS

	for i in range(len(teamNames)):	
		text = '\u20ac ' + '%.0f'%(teamVals[i]/1e6) + 'M' 
		text2 = '\u20ac ' + '%.0f'%(teamMeanPrices[i]/1e6) + 'M' 


		ax2.annotate( text , xy = (float(i), teamVals[i]/1e6), horizontalalignment = 'center'   )
		ax.annotate( text2 , xy = (float(i), teamMeanPrices[i]/1e6), horizontalalignment = 'center'   )

	print plt.gca()


	#loc = plticker.MultipleLocator(base=5.0)
	#ax.yaxis.set_major_locator(loc)


	#plt.yticks(np.arange(0, 120, 10))




	#handle = line2, line2
	#label = 'Average Price', # I'm not sure why but I need a comma here.
	#pos = 'upper right'
	#plt.figlegend(handle, label,pos)

	#X-Label
	plt.ylabel('Total Team Value', rotation = 'vertical')
	plt.show()


leaguePrice(leagueId)
