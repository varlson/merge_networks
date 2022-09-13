# -*- coding: utf-8 -*-

import igraph as ig
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib

import scipy.stats as st

import time
import multiprocessing as mp

import sys

# to create directories
from pathlib import Path





# Here we consider only the intersection between the ordered metric and the ordered cities
# Sometimes the array with the ordered cities present cities that are not in the network and vice-versa
# Besides, some nodes represent more than one city
def pre_processing_data(ord_metric, data_covid):
	ord_metric_comp = []
	data_covid_comp = []

	# Removing the 'unknown' lines
	#ord_metric = ord_metric[ord_metric['city_code'] != 'UNKNOWN']


	for i in range(len(ord_metric)):
		code = ord_metric.iloc[i,1]
		# print(code)
		if code != 'UNKNOWN':
			included = False
			for j in range(len(data_covid)):
				if(str(data_covid.iloc[j,2]) in str(code) or (str(code) in str(data_covid.iloc[j,2]))):
					# Codes are added only once. 
					# It means that those nodes who represent more than one city will consider
					# only the first city that notifies a case or death by COVID-19
					if(data_covid.iloc[j,2] not in ord_metric_comp):
						ord_metric_comp.append(data_covid.iloc[j,2])
						#data_covid_comp.append(data_covid.iloc[j,2])
						included = True
						break
			if included == False:
				ord_metric_comp.append(code)
		#else:
		#	ord_metric_comp.append(code)


	# Now that we have the intersection of cities, we get the clean ordered cities from
	# the covid data
	for i in range(len(data_covid)):
		for j in range(len(ord_metric_comp)):
			if( data_covid.iloc[i,2] == ord_metric_comp[j] ):
				data_covid_comp.append((data_covid.iloc[i,1],data_covid.iloc[i,2]))

	'''
	x1 = np.arange(1,len(data_covid_comp)+1,1)
	x2 = []
	for i in range(len(data_covid_comp)):
		ind = data_covid_comp.index( int(ord_metric_comp[i]) )
		x2.append(ind)
	x2 = np.array(x2)
	print(len(ord_metric_comp), '  ', len(data_covid_comp))'''

	return ord_metric_comp, data_covid_comp#, x1, x2
	


# Compute Kendall's tau and spearman correlations
def correlations(file_out_corr, x1, x2):
	# kendall, p-value-kendall, spearman, p-value-spearman
	corr, p_value = st.kendalltau(x1, x2)
	file_out_corr.write(metric + ';' + str(len(ord_metric)) + ';' + str(corr) + ';' + str(p_value))

	corr, p_value = st.spearmanr(x1, x2)
	file_out_corr.write(';' + str(corr) + ';' + str(p_value) + '\n')



# Compute the intersections between the network ordered nodes (by metrics) and COVID-19 data by date
def intersections(metric, ord_metric, ord_covid):

	#print(ord_covid)
	ord_covid = np.array(ord_covid)
	print(f'orde covid {ord_covid}')

	file_out = open(relative_path + 'intersec_' + cases_or_deaths + '_' + metric + '.csv', 'w')
	file_out_int = open(relative_path + 'intersec_integral_' + cases_or_deaths + '_'+ metric + '.csv', 'w')

	N_cases = len(ord_covid)
	# for each metric: vary the series size until N_cases.
	# Check: cont/n

	integral = 0.0

	# the set size
	nc = 1
	# the first date
	current_date = ord_covid[nc-1,0]

	cont_plot = 0
	while(nc <= N_cases): 

		# find all cases at the same date
		while(nc <= N_cases and current_date == ord_covid[nc-1,0]):
			nc += 1

		nc_aux = nc-1

		cont = 0.0
		for i in range(nc_aux):
			#print(ord_metric[i])
			if(str(ord_metric[i]) in ord_covid[:nc_aux,1]):
				cont += 1.0

		#print(str(nc) + ';' + str(cont) + ';' + str(nc_aux))
		file_out.write(str(cont_plot) + ';' + str(cont / float(nc_aux)) + ';' + current_date + '\n')
		cont_plot += 1

		integral += cont / float(nc_aux)
		
		if(nc <= N_cases):
			# update with the new date (for the next iteration)
			current_date = ord_covid[nc-1,0]

	file_out_int.write(str(integral))

	file_out_int.close()
	file_out.close()



# MAIN CODE

# The network name and whether we are dealing with "cases or deaths" come from command line. 
net_name = sys.argv[1]
cases_or_deaths = net_name
group = sys.argv[2]
prefix = None

temp = net_name.split('_')
if len(temp) > 1:
	net_name = f'{temp[1]}_&_{temp[2]}'
	cases_or_deaths = net_name
	prefix = temp[0]


relative_path_in = 'results/' + net_name + '/metrics/'
relative_path = 'results/' + prefix+'_'+net_name + '/intersection/'

# create directory if it does not exist
Path(relative_path).mkdir(parents=True, exist_ok=True)

print('CORRELATIONS')


# Metrics we use
metrics = ['degree', 'betweenness', 'strength', 'betweenness_w', 'closeness', 'closeness_w']

# metrics = ['degree', 'betweenness', 'closeness', 'vulnerability', 'strength', 'betweenness_weight', 'closeness_weight', 'vulnerability_weight']


# COVID-19 data
file_name = f'out/{group}/cities/' + cases_or_deaths+'.csv'
# print(f'full path {}')
data_covid = pd.read_csv(file_name, delimiter=',')



file_out_corr = open(relative_path + 'correlations_' + cases_or_deaths + '.csv', 'w')
file_out_corr.write('METRIC;KENDALL;KEDALL_P_VALUE;SPEARMAN;SPEARMAN_P_VALUE\n')


for metric in metrics:
	print('metric: ', metric)
	metric_data = pd.read_csv(f'out/{group}/metric/{net_name}_{metric}.csv', delimiter=',')

	# Renaming columns to make it easier to manipulate de dataframes
	# metric_data.columns = ['city_number', 'city_code', 'metric']

	ord_metric, ord_covid = pre_processing_data(metric_data, data_covid)
		
	# Compute Kendall's tau and spearman correlations
	#correlations(file_out_corr, x1, x2)

	# Compute the intersections between the network ordered nodes (by metrics) and the COVID-19 data by date
	intersections(metric, ord_metric, ord_covid)


file_out_corr.close()