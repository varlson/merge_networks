from utility import *
def main(graph, graph_name):

    dataframe = {}
    _tuple = []

    x_axis = [x for x in range(graph.vcount())]
    covid_cases_geocodes = list(pd.read_csv('out/csv/'+graph_name+'.csv')['geocode'])
    dataframe['covid_cases_geocode'] = covid_cases_geocodes
    
    
    deg_metric = sort_by_metric(graph, 'degree')
    graph_geocodes = [x[0] for x in deg_metric]
    sorted_by_degree = [x[1] for x in deg_metric]
    correspondence = correspondence_processor(graph_geocodes, covid_cases_geocodes)
    dataframe['geocode_by_degree'] = graph_geocodes
    dataframe['correspondence_by_degree'] = correspondence
    cor,pvalue = spearman(graph_geocodes, covid_cases_geocodes)

    _tuple.append((x_axis, correspondence, (cor, pvalue)))

    bet_metric = sort_by_metric(graph, 'betweenness')
    graph_geocodes = [x[0] for x in bet_metric]
    geocode_by_bet = [x[1] for x in bet_metric]
    correspondence = correspondence_processor(graph_geocodes, covid_cases_geocodes)
    dataframe['geocode_by_betweenness'] = graph_geocodes
    dataframe['correspondence_by_betweenness'] = correspondence
    cor,pvalue = spearman(graph_geocodes, covid_cases_geocodes)
    _tuple.append((x_axis, correspondence, (cor, pvalue)))


    srte_metric = sort_by_metric(graph, 'strength')
    graph_geocodes = [x[0] for x in srte_metric]
    geocode_by_bet = [x[1] for x in srte_metric]
    correspondence = correspondence_processor(graph_geocodes, covid_cases_geocodes)
    dataframe['geocode_by_strength'] = graph_geocodes
    dataframe['correspondence_by_strength'] = correspondence
    cor,pvalue = spearman(graph_geocodes, covid_cases_geocodes)
    _tuple.append((x_axis, correspondence, (cor, pvalue)))



    bet_w_metric = sort_by_metric(graph, 'betweenness_w')
    graph_geocodes = [x[0] for x in bet_w_metric]
    geocode_by_bet = [x[1] for x in bet_w_metric]
    correspondence = correspondence_processor(graph_geocodes, covid_cases_geocodes)
    dataframe['geocode_by_betweenness_w'] = graph_geocodes
    dataframe['correspondence_by_betweenness_w'] = correspondence
    cor,pvalue = spearman(graph_geocodes, covid_cases_geocodes)
    _tuple.append((x_axis, correspondence, (cor, pvalue)))

    # graphPloter(_tuple, ["$k$", "$b$"], graph_name)
    graphPloter(_tuple, ["$k$", "$b$", "$s$", "$b_{w}$"], graph_name)


    df = pd.DataFrame(dataframe)
    dirMaker('out/csv/processed')
    df.to_csv('out/csv/processed/'+graph_name+'.csv')


name = 'aerial_&_terrestrial'
graph = Graph.Read_GraphML('in/'+name+'.GraphML')
graph.vs['geocode'] = graph.vs['id']  
graph.es['weight'] = [x if x > 0 else 0.00001 for x in graph.es['weight']] 

main(graph, name)