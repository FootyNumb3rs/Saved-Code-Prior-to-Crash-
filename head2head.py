import opendata as OD
import numpy as np
import pprint as pp
import cv2
from pylab import *

class Rivals(object):
	def __init__(self,league, yearOne, yearTwo, teamOne, teamTwo):
		self.master = OD.openData()
		self.teamMatrix = { teamOne: np.zeros((8,8)), teamTwo: np.zeros((8,8)) }
		comp = self.master.H2H(league, yearOne, yearTwo, teamOne, teamTwo)

		for fixture in comp:
			result = fixture['match_result']
			slug = fixture['match_slug'].split('-')
			result = result.split('-')
			result = [int(i) for i in result]

			if result[0] != result[1]:
				wIndex = np.argmax(result) 
				wMatrix = self.teamMatrix[slug[wIndex]]
				wMatrix[result[0],result[1]] += 1

		print self.teamMatrix

	def getMatrix(self, team):
		return self.teamMatrix[team]

class Seasons(object):
	def __init__(self, league, yearOne, yearTwo, team):
		self.master = OD.openData()
		self.winMatrix = np.zeros((8,8))
		self.lossMatrix = np.zeros((8,8))
		self.drawMatrix = np.zeros((8,8))
		self.games = self.master.getRounds(league, yearOne, yearTwo, team)['data']['rounds']

		#************************************ POPULATE MATRIX ***********************************
		for game in self.games:
			if game['match_result'] != '':
				score = game['match_result'].split('-')
				score = [int(i) for i in score]
				if score[0] == score[1]:
					self.drawMatrix[ score[0], score[1]] += 1
				else:
					winIndex = np.argmax(score)
					if game['match_slug'].split('-')[winIndex] == team:
						self.winMatrix[score[0], score[1]] += 1
					else:
						self.lossMatrix[score[0], score[1]] += 1
		#****************************************************************************************

		#**************************************** GRAPHING **************************************
		ax = subplot(111)
		nonZero = np.where(self.winMatrix > 0)
		for i in range( len(nonZero[0]) ):
			row = nonZero[0][i]
			col = nonZero[1][i]
			print type(int(row))
			ax.text(col, row , int(self.winMatrix[row,col]) , fontsize = 15, color = 
			'r', fontweight = 'bold',  verticalalignment='center', horizontalalignment='center')
		ax.xaxis.tick_top()
		xlabel('Away Goals')    
		ylabel('Home Goals')
		ax.xaxis.set_label_position('top')
		#title(team)
		#****************************************************************************************


	def showGraph(self):
		imshow(mat.getWin(), interpolation='nearest', cmap = 'gray')
		pause(0)
		return
		
	def getWin(self):
		return self.winMatrix

	def getLoss(self):
		return self.lossMatrix

	def getDraw(self):
		return self.drawMatrix


mat = Seasons('Serie A', 2015, 2016, 'juventus')
mat.showGraph()










