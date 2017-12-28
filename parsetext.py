import requests as req
from bs4 import BeautifulSoup as bs 

def parsetext(headline, league, teams, players): # Just one headline
	if len(headline) == 0:
		return([players,teams])

 	threeWordName = headline[0:3]
 	sep = ' '
 	twoWord = sep.join(headline[0:2])
 	if twoWord not in league: # Not two-word team
 		oneWord = twoWord.split(' ')[0]
 		if oneWord not in league: # Not one-word team
 			base = "https://en.wikipedia.org/wiki/"
 			html = bs(req.get(base + twoWord).text,"html.parser")
 			bad = html.find_all('div', class_ =  'noarticletext')
			if bad:
				return (parsetext(headline[1:], league, teams, players))
			else: #Two-Word Player or Two-Word International
				players.append(twoWord)
				try:
					return (parsetext(headline[2:], league, teams, players))
				except:
					return([players,teams])

		else: # One-Word Team
			teams.append(oneWord)
			return(parsetext(headline[1:], league, teams, players))
	else: # Two Word Team
		teams.append(twoWord)
		return(parsetext(headline[2:], league, teams, players))


def getLeague():
	leagueList = []
	leagues = ['Premier League', 'La Liga', 'Serie A', 'Bundesliga']
	url = "https://en.wikipedia.org/wiki/2016%E2%80%9317_Premier_League"
	leagueWiki = req.get(url).text
	leagueSoup = bs(leagueWiki, "html.parser") 
	teamTable  = leagueSoup.find('table',class_= 'wikitable')
	rows = teamTable.find_all('tr')[1:] # finds [16] in zero for some reason
	for tr in rows:
		leagueList.append(tr.find('a').get_text())
	leagueList += ['West Ham', 'Man City', 'Bournemouth']
	return leagueList

headline = ['Real','Madrid','Manchester', 'United', 'Diego','Costa','Dimitri','Payet','Chelsea','Cristiano','Ronaldo']
league = getLeague()

teamz = []

play = []
done = parsetext(headline, league,play, teamz )


print(done)

