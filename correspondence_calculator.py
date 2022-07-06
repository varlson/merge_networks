from datetime import datetime
from utility import *
import multiprocessing

return_values = multiprocessing.Manager()
dataframe = {}
_tuple = return_values.list()


# lgraph = ['fluvial_&_aerial.GraphML', 'fluvial_&_terrestrial.GraphML', 'terrestrial_&_aerial.GraphML']

name = 'fluvial_&_terrestrial'
in_net_base_path = 'out/amazonas/networks'
in_csv_base_path = 'out/amazonas/csv'
out_full_path = 'out/amazonas/plots/correspondence'
# name = sys.argv[2]
graph = Graph.Read_GraphML(f'{in_net_base_path}/{name}.GraphML')
graph.vs['geocode'] = graph.vs['id']  
graph.es['weight'] = [x if x > 0 else 0.00001 for x in graph.es['weight']] 

x_axis = [x for x in range(graph.vcount())]
covid_cases_geocodes = list(pd.read_csv(f'{in_csv_base_path}/fluvial_&_terrestrial.csv')['geocode'])
dataframe['covid_cases_geocode'] = covid_cases_geocodes


def degree():
    print('job-1')
    deg_metric = sort_by_metric(graph, 'degree')
    print(f'sorted: {deg_metric}')
    graph_geocodes = [x[0] for x in deg_metric]
    sorted_by_degree = [x[1] for x in deg_metric]
    correspondence = correspondence_processor(graph_geocodes, covid_cases_geocodes)
    dataframe['geocode_by_degree'] = graph_geocodes
    dataframe['correspondence_by_degree'] = correspondence
    cor,pvalue = spearman(graph_geocodes, covid_cases_geocodes)

    _tuple.append((x_axis, correspondence,( cor,pvalue)))

def strength():
    print('job-3')
    srte_metric = sort_by_metric(graph, 'strength')
    graph_geocodes = [x[0] for x in srte_metric]
    geocode_by_bet = [x[1] for x in srte_metric]
    correspondence = correspondence_processor(graph_geocodes, covid_cases_geocodes)
    dataframe['geocode_by_strength'] = graph_geocodes
    dataframe['correspondence_by_strength'] = correspondence
    cor,pvalue = spearman(graph_geocodes, covid_cases_geocodes)

    _tuple.append((x_axis, correspondence,( cor,pvalue)))
    # print(f'locally {for_strength}')

def betweenness():
    
    print('job-2')
    bet_metric = sort_by_metric(graph, 'betweenness')
    graph_geocodes = [x[0] for x in bet_metric]
    geocode_by_bet = [x[1] for x in bet_metric]
    correspondence = correspondence_processor(graph_geocodes, covid_cases_geocodes)
    dataframe['geocode_by_betweenness'] = graph_geocodes
    dataframe['correspondence_by_betweenness'] = correspondence
    cor,pvalue = spearman(graph_geocodes, covid_cases_geocodes)

    _tuple.append((x_axis, correspondence,( cor,pvalue)))
    # print(f'locally {for_betweenness}')


def betweenness_w():
    
    print('job-4')
    bet_w_metric = sort_by_metric(graph, 'betweenness_w')
    graph_geocodes = [x[0] for x in bet_w_metric]
    geocode_by_bet = [x[1] for x in bet_w_metric]
    correspondence = correspondence_processor(graph_geocodes, covid_cases_geocodes)
    dataframe['geocode_by_betweenness_w'] = graph_geocodes
    dataframe['correspondence_by_betweenness_w'] = correspondence
    cor,pvalue = spearman(graph_geocodes, covid_cases_geocodes)

    _tuple.append((x_axis, correspondence,( cor,pvalue)))
    # print(f'locally {for_betweenness_w}')

def main(graph, graph_name, full_path):

    
    all_process =[]
    
    start = datetime.now()

    task_lst = [degree, betweenness, strength, betweenness_w]
    for task in task_lst:
        all_process.append(multiprocessing.Process(target=task))
    
    for process in all_process:
        process.start()
   
    for process in all_process:
        process.join()

    end = datetime.now()


    print(f'total time {end-start}')
    print(f'size of {len(_tuple)}')
    graphPloter(_tuple, ["$k$", "$b$", "$s$", "$b_{w}$"], full_path, graph_name)

    df = pd.DataFrame(dataframe)
    dirMaker('out/csv/processed')
    df.to_csv('out/csv/processed/'+graph_name+'.csv')




# lgraph = ['fluvial_&_aerial.GraphML', 'fluvial_&_terrestrial.GraphML', 'terrestrial_&_aerial.GraphML']


    
main(graph, name, out_full_path)