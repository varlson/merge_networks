import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import string
import random
from matplotlib import rc

import sys

from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)


# Latex font --------------------
rc('text', usetex=True)
font = {'family' : 'normal',
         'weight' : 'bold',
         'size'   : 12}

rc('font', **font)
params = {'legend.fontsize': 14}
plt.rcParams.update(params)
# -------------------------------



# The network name comes from command line. 
net_name = sys.argv[1]
cases_or_deaths = sys.argv[2]

relative_path = 'results/'


print('PLOTTING PREDICITON OVER TIME')

'''
stats = ['degree', 'betweenness', 'closeness', 'vulnerability']
stats_w = [ 'strength', 'betweenness_weight', 'closeness_weight', 'vulnerability_weight']

lbls = [r'$k$', r'$b$', r'$c$', r'$v$'] #, r'$eig$', r'$pr$']
lbls_w = [r'$s$', r'$b_w$', r'$c_w$', r'$v_w$'] #, r'$eig_w$', r'$pr_w$']

colors   = ['black', 'palevioletred','brown','darkgreen',     'darkorange','indigo']
colors_w = ['gray',  'pink',         'red',    'mediumseagreen','orange',    'blueviolet']

'''
lbls = [r'$k$', r'$b$', r'$c$', r'$v$', r'$s$', r'$b_w$', r'$c_w$', r'$v_w$'] 
colors   = ['black', 'palevioletred','brown','darkgreen', 'gray',  'pink', 'red', 'mediumseagreen']
metrics = ['degree', 'betweenness', 'closeness', 'vulnerability', 'strength', 'betweenness_weight', 'closeness_weight', 'vulnerability_weight']




fig, ax = plt.subplots(1, 1)
fig.set_size_inches(6, 3) 



series_size = 0


relative_path_in = 'results/' + net_name + '/intersection/'


for i in range(len(metrics)):
	cl = colors[i]
	lbl = lbls[i]

	file_name = relative_path_in + 'intersec_' + cases_or_deaths + '_' + metrics[i] + '.csv'
	array_metrics = pd.read_csv(file_name, delimiter=';', header=None)


	#print('array_metrics:', array_metrics)
	#print('second column: ', array_metrics.iloc[:,2])

	#file_name = relative_path_in + 'intersec_integral_' + cases_or_deaths + '_' + metrics[i] + '.csv'
	#integral = np.genfromtxt(file_name)
	#integral = f'{integral:.2f}'
	
	#average_rate = np.mean(array_metrics.iloc[:,1])
	average_rate = np.mean([float(rate) for rate in array_metrics.iloc[:,1]])

	label = lbl + ' (' + '%.2f' % average_rate + ')' #r'({average_rate:.2f})'

	#print('size = ', len(array_metrics))

	
	if i < len(metrics)/2:
		ax.plot(array_metrics.iloc[:,0], array_metrics.iloc[:,1], lw=2, color=cl, label=label, linestyle='--', zorder=2)
	else:
		ax.plot(array_metrics.iloc[:,0], array_metrics.iloc[:,1], lw=2, color=cl, label=label, zorder=2)
	

#print(array_metrics.iloc[:,0])

# null_model = pd.read_csv('null_model.csv', delimiter=';', header=None)
# X = np.linspace(0,len(array_metrics),len(array_metrics)+1)

# #print('x = ', X)
# '''null_model_points = []
# for i in range(len(null_model.iloc[0,:])):
# 	null_model_points.append(np.mean(null_model.iloc[:,i]))


# ax.plot(X,null_model_points, lw=1, color='cornflowerblue', zorder=1)'''

# #for i in range(len(null_model)):
# #	ax.plot(X,null_model.iloc[i,:], lw=1, color='cornflowerblue', zorder=1)


# data = []
# for i in range(len(null_model.iloc[0,:])):
# 	data.append(null_model.iloc[:,i])

# print(f'lenght of data {len(data)}')
# print(f'lenght of data {len(X)}')
# ax.boxplot(data, positions=X, zorder=1)

# print('average by chance = ', np.mean(data))


#print(null_model.iloc[0])

#print('size null model = ', len(null_model.iloc[0,1:]))


#ax.set_xlim([1,len(array_metrics)])
ax.legend(ncol=2, fontsize=9, loc='lower right')

#ax.set_xlabel(r'$n$', fontsize=14)
ax.set_ylabel(r'Intersection rate', fontsize=14)

ax.set_ylim([-0.05, 1.05])
ax.set_xlim([0.0, len(array_metrics)-1])

ax.locator_params(axis='y', nbins=4)
#ax.locator_params(axis='x', nbins=10)


ax.set_xticks(np.linspace(0,len(array_metrics)-1,len(array_metrics)))
ax.set_xticklabels(array_metrics.iloc[:,2], 
	{'fontsize': 12,
     'rotation': 60})



plt.tight_layout()

fig.savefig(relative_path + net_name + '/intersec_' + cases_or_deaths + '.png', dpi=350)
fig.savefig(relative_path + net_name + '/intersec_' + cases_or_deaths + '.pdf', dpi=350)
fig.savefig(relative_path + net_name + '/intersec_' + cases_or_deaths + '.png', dpi=350)
fig.savefig(relative_path + net_name + '/intersec_' + cases_or_deaths + '.svg', dpi=350)
