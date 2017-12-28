# encoding=utf8  
# -*- coding: utf-8 -*-
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from matplotlib import cm
import pandas as pd 
import numpy as np 
from bs4 import BeautifulSoup as bs
import requests as req 
import pprint as pp
import re
import pylab
import matplotlib
from pylab import plt
from matplotlib.font_manager import FontProperties
from babel.numbers import format_currency
from matplotlib.ticker import FuncFormatter
from adjustText import adjust_text
from scipy import interpolate
from text_plotter import text_plotter, get_text_positions


spec = cm.get_cmap('Greens')

matplotlib.style.use('ggplot')
newFrame = pd.read_csv('tester2_with_pos.csv', header = 0)

def set_tick_params(which, bottom, left,right, top):

	return None#dict{'which': which, 'bottom': bottom, 'left': left, 'right':right, 'top':top}  

def get_currency(curr_float):
	return u'\xA3'+ str(int(float(curr_float))/1000) + 'K' # Turn currency into British Pounds
	#return format_currency(curr_float, 'EUR', locale='de_DE',currency_digits = False)

def simpleGraph(data, 
				title = '', # Super Title
				subtitle = '',	# Axes title
				kind='bar', # Plot type
				tick_str=None, # Y-ticks replacement
				x_data=None,y_data= None, # Optional 
				name_labels = None,	# If you want names instead of numbers on plot
				xlabel='', # Self-explanatory
				ylabel='', #...
				ylabel_formatter = str, # String formatter for x/y labels
				xlabel_formatter = str,
				ylims = None, # Array containing upper and lower y-limits
				xlims=None,	#...
				annotate=False, # Annotating graph with string
				fontname = 'Poppins', # Universal Font
				col_mode = 'light' #Modify plot color
				): 
	dummySeries = pd.Series() # Not sure this is necessary
	dummyFrame = pd.DataFrame()
	graph = data # Somewhat redundant 

	color_modes = {'dark':  
						{'suptitle':'#FFFFFF', 
						 'title':'#FFFFF0',
						 'grid' :'gray',
						 'bg': '#000000',
						 'ticks':'#dadada',
						 },
				   'light':
				   		{'suptitle':'black',
				   		 'title':'grey',
				   		 'grid':'#D3D3D3',
				   		 'bg':'#FFFFFF',
				   		 'ticks':'black',
				   		}
				  }
	# Setting colors for various parts of the plot
	color_mode = color_modes[col_mode]
	suptitle_color = color_mode['suptitle']
	title_color = color_mode['title']
	grid_color = color_mode['grid']
	bg_color = color_mode['bg']
	tick_color = color_mode['ticks']


	# Setting the major and minor ticks 
	tick_params_dict = {'bar': set_tick_params('both','off','off','off','off'), 
						 'line': set_tick_params('both','on','on','on','off'),
						 'barh': set_tick_params('both','off','off','off','off') }

	# Various plot properties grouped according to plot type
	property_dict = {'bar': { 'y_axis_visible': True,
							  'x_axis_visible': True,
							  'x_axis_grid':False,
							  'y_axis_grid':True,
							  'spines':['bottom','left'],
							  
										}, 
					'barh':{ 'y_axis_visible': True,
							  'x_axis_visible': True,
							  'x_axis_grid':True,
							  'y_axis_grid':False,
							  'spines':['left','bottom']
							  
										},
					'line': 
						   { 'y_axis_visible': True,
							  'x_axis_visible': True,
							  'x_axis_grid':True,
							  'y_axis_grid':True,
							  'spines':['left','bottom','right','top']
							  
							  },

					'scatter':
							{ 'y_axis_visible': True,
							  'x_axis_visible': True,
							  'x_axis_grid':True,
							  'y_axis_grid':True,
							  'spines':['left','bottom','right','top']
										}
					}

 	# SETTING FONT PROPERTIES
	font_dict = { 'xlabel': {'fontname':fontname, 'fontsize':15},
				  'ylabel':	{'fontname':fontname, 'fontsize':15},
				  'yticks': {'fontname':fontname, 'fontsize':18},
				  'xticks': {'fontname':fontname, 'fontsize':18},
				  'subtitle': {'fontname':fontname, 'fontsize':11},
				  'suptitle': {'fontname':fontname, 'fontsize':25},
				}

	# Setting aformentioned plot properties
	params = property_dict[kind]


	# Setting X and Y axis grids 
	graph.axes.get_yaxis().grid(color = grid_color, ls = '-', linewidth=1 )
	graph.axes.get_yaxis().grid(params['y_axis_grid'])
	graph.axes.get_xaxis().grid(color = grid_color, ls = '-', linewidth=1 )
	graph.axes.get_xaxis().grid(params['x_axis_grid'] )

	# Setting x and y axes visible -- Not to be confused with GRIDS
	graph.axes.get_xaxis().set_visible(params['x_axis_visible'])
	graph.axes.get_yaxis().set_visible(params['y_axis_visible'])


	# Setting background color (within plot)
	graph.set_axis_bgcolor(bg_color)
	graph.tick_params(which = 'both',
					  bottom = 'off',
					  left = 'off',
					  right ='off',
					  top = 'off',
					  labelsize = 15,
					  )

	# This is why x and y data are necessary
	'''
	# Setting Axis limit
	if kind == 'barh':
		y_lim_0=np.mean(y_data) - (max(y_data)*1.2 - np.mean(y_data))
	if kind == 'line':
		y_lim_0 = 0
	'''

	# Is this necessary??
	if xlims!= None:
		graph.set_xlim([xlims[0],xlims[1]])
	if ylims != None:
		graph.set_ylim([ylims[0],ylims[1]])

	# Setting yticklabels
	if type(tick_str) == type(None): # If We don't have a tick_string
		xticks = [int(tick) for tick in graph.get_xticks()] # Turning ticks into proper numerical form
		yticks = [round(tick,3) for tick in graph.get_yticks()]

	else:
		yticks = tick_str
		xticks= graph.get_xticks()
	
	# Applying label formatter - labels turned to string here -- SHOULD THIS BE DONE WITHIN THE FORMATTER?
	graph.set_yticklabels([ylabel_formatter(str(tic)) for tic in yticks],
		color = 'black',**font_dict['yticks'])
	graph.set_xticklabels([xlabel_formatter(str(tic)) for tic in xticks],
		color = 'black',**font_dict['xticks'])
	
	# Setting Spines
	spines = property_dict[kind]['spines'] # Getting spines on/off from tick params
	for side in ['right','left','top','bottom']:
		if side in spines:
			graph.spines[side].set_color(grid_color) # Setting spine color
			graph.spines[side].set_visible(True) # True if side in spine dictionary
		else:
			graph.spines[side].set_visible(False) 


	
	# Setting super-title, otherwise known as 'Title'
	plt.suptitle(title+'', horizontalalignment = 'center',
						   color = suptitle_color,
						 **font_dict['suptitle']
						   )
	# Setting plot titles indiviudally 
	graph.set_title(subtitle+'\n',color = title_color,
					 horizontalalignment = 'center', linespacing = .1,
	 				**font_dict['subtitle']) # font_dict contains font information

	# Setting x and y labels
	graph.set_xlabel(xlabel,  labelpad = 15,**font_dict['xlabel'])
	graph.set_ylabel(ylabel, labelpad = 25,**font_dict['ylabel'])


	'''
	#Adjusting text
	texts = []
	names = name_labels
	txt_height = 0.04*(plt.ylim()[1] - plt.ylim()[0])
	txt_width = 0.02*(plt.xlim()[1] - plt.xlim()[0])
	text_positions = get_text_positions(x_data,y_data,txt_width,txt_height)
	text_positions = get_text_positions(x_data, y_data, txt_widths, txt_height)
	text_plotter(names,x_data, y_data, text_posit ions, txt_width, txt_height)
	plt.show()
	'''

	
	# Annotating bars with value
	if annotate:
		if (kind == 'barh'): # If horzontal barplot
			try:
				n_col = np.shape(x_data)[1] # Np.shape returns a tuple, if its ONE-D 
			except:
				n_col = 1
			for j in range(0,n_col): # For each set of bars or bar x locations
				if n_col== 1:
					bar_x_locations = x_data 
				else:
					arr = x_data[:,j]
				for i, label in enumerate(list(arr)):
					adj = .08
					graph.annotate(str(round(label,2)), xy = (label+.003,i-.1),fontsize = 13.5)


		elif kind == 'bar': #  If vertical bar plot
			for p in graph.patches: # For individual bars 
				graph.annotate(int(np.round(p.get_height(),2)), # The number we're annotating
					(p.get_x()+p.get_width()/2., p.get_height()), # x_value is the x-value of the bar, y is the height of the bar
					 ha='center', va='center', xytext=(0, 10), # xy text is the location of the text if an arrow is included, if nit 
					 textcoords='offset points')


	'''
	if (k
	ind == 'line') | (kind =='scatter'):
		graph.axis('on')
		li_x = list(x_data)
		li_y = list(y_data)
		for i, label in enumerate(y_data):
			name = name_labels[i]
			att = ' ('+get_currency(li_y[i])+')'
			#name = name + att
			#label = str()
			#print(name)
			pound=u'\xA3'
			graph.annotate(name, xy = (float(li_x[i])+.1, float(li_y[i])+.1), fontsize = 10)
	'''
	
	x_lim = graph.get_xlim()
	y_lim = graph.get_ylim()
	ylabel_loc = (x_lim[0],y_lim[1]*(1.005)) # Places Y-label at the top of y-axis
	xlabel_loc = [x_lim[1]*(1.005) ,y_lim[0]] # X-label  at the end of x-axis 
#
	
	texts = []

	'''
	for x, y, s in zip(x_data, y_data, name_labels):
	    texts.append(plt.text(x, y, s))

	f = interpolate.interp1d(x_data, y_data)
	x = np.arange(min(x_data), max(x_data), 0.0005)
	y = f(x)    
	adjust_text(texts,
	            only_move={'points':'y', 'text':'y'}, force_points=0.15,
	            arrowprops=dict(arrowstyle="->", color='grey', lw=0.5))
	'''

	# SETTING LABELS ABOVE AXES -- ALTERNATE LABELS
	#graph.annotate(xlabel, xy = xlabel_loc, fontsize = 18)
	#graph.text( -4.69,ylabel_loc[1], ylabel,color = 'black', fontsize = 18)
	#graph.text(xlabel_loc[0],xlabel_loc[1], xlabel,color = 'black', fontsize = 18)

	#graph.annotate(ylabel, xy = ylabel_loc, fontsize = 18)

	
	# Y-axis data formatter
	

	
'''
# Number of Links by team 
params = ('Name','Team')
for param in params:
	data = newFrame[param].value_counts(ascending = False)[:11].sort_values()
	graph = simpleGraph(data, param, use_index=True, ylim = data.max()*(1.9))
	plt.tight_layout(pad = 4)
	plt.savefig(param+'Chart.pdf')
'''


'''
def fix(Series):
	temp = ['Defender','Forward','Goalkeeper','Midfielder']
	col = ['r','b','g','y']
	for pos in ('Defender','Forward','Goalkeeper','Midfielder'):
		if pos not in Series.keys():
			col.remove(colors[temp.index(pos)])
			temp.remove(temp[temp.index(pos)])
	ax.pie(Series, labels=lab[:len(Series)], colors=col)
	ax.axis('equal')
pylab.show()


group = newFrame.groupby('Team')['Position'].value_counts(ascending = False).sort_index()
'''


'''
colors = {'Midfielder':"gold",'Forward':"yellowgreen",'Goalkeeper':"lightcoral",'Defender':"lightskyblue"}

img= plt.imread('prem_background.jpg')
plt.imshow(img, extent=[1,3,1,3])
plt.grid(False)
'''

'''
font0 = FontProperties()
fig = plt.figure()
unq_teams = newFrame.loc[:,'Team'].unique()
for i, team in enumerate(unq_teams):
	name_label = []
	bools = newFrame.loc[:,'Team'] == team
	pos_count = newFrame.loc[bools,'Position'].value_counts(ascending = True).sort_index()
	lab = ['Defender', 'Forward','Goalkeeper','Midfielder']
	colors = ['fuchsia','mediumspringgreen','indigo','yellow']

	for pos in ('Defender', 'Forward','Goalkeeper','Midfielder'):
		if pos not in pos_count.keys():
			colors.remove(colors[lab.index(pos)])
			lab.remove(lab[lab.index(pos)])
		else:
			boolz = newFrame['Position'] == pos
			players = newFrame.loc[bools & boolz,'Name'].unique()
			players='\n'.join(list(players))
			name_label.append(players)

	# Setting Fonts
	font_dict = {'family':'serif',
				 'color':'black',
				 'weight': 'light',
				 'size':16,}
	ax = fig.add_subplot(5,5,i+1)
	font = font0.copy()
	plt.title(team, fontdict = font_dict)
	#ttl.set_position([.5, 1.35])
	ax.pie(pos_count, labels=name_label, colors=colors)
	ax.axis('equal')
	fig.subplots_adjust(hspace=1.3,wspace=1.3)
pylab.show()
'''

'''
fig, ax = plt.subplots(1,4)

table_data = []
name_count= newFrame.Name.value_counts(ascending = False)
for group in name_count.groupby(name_count):
	print(group)
	formatted = [[name] for name in group[1].axes[0].tolist()]
	print(formatted)
	table_data.append(formatted)
pp.pprint(table_data)

fig, ax = plt.subplots(1,1)
ax.axis('off')
ax.table(cellText= table_data, cellLoc='center',loc='center' )
plt.show()
'''


'''
## Player count 
playerCount = newFrame['Name'].value_counts(ascending = False)[0:20]
boolean = playerCount.values >= 2
simpleGraph(playerCount[boolean].sort_values(ascending = True),'Number of Times Mentioned', use_index=True)
pylab.show()
'''

'''
for i in range(len(newFrame['Team'].unique())):
	team = newFrame['Team'].unique()[i]
	boolIndex = newFrame['Team'] == team
	teamPos = newFrame.loc[boolIndex,'Position'].value_counts(ascending = True)
	teamPos.plot.pie(subplots = True)
pylab.show()
'''

