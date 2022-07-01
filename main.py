import os
lgraph = ['fluvial_&_aerial.GraphML', 'fluvial_&_terrestrial.GraphML', 'terrestrial_&_aerial.GraphML']

for graph in lgraph[:1]:
    # graph = graph.split('.')[0]
    os.system(f'python merge_net.py')