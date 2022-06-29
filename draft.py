# def merge_networks_v1(glist, attribute):
#     identifier(glist, "id")
#     lst = []
#     G = ig.Graph()
#     for g in glist:
#         for index, geo in enumerate(g.vs['id']):
#             if geo not in lst:
#                 lst.append(geo)
#                 G.add_vertices(1)
#                 G.vs[G.vcount()-1]['id'] = g.vs[index]['id']
#                 G.vs[G.vcount()-1]['x'] = g.vs[index]['x']
#                 G.vs[G.vcount()-1]['y'] = g.vs[index]['y']
#     G.es['id'] = [-1]*G.vcount()    
#     G.es[attribute] = [-1]*G.vcount()    
#     for g in glist:
#         for index, (src, trg) in enumerate(g.get_edgelist()):
#             id = id_extractor(g, src, trg, 'id')
#             if id in G.es['id']:
#                 i = G.es['id'].index(id)
#                 G.es[i][attribute] += g.es[attribute][index]
#             else:
#                 G.add_edgess([(src, trg)])
#                 G.es[G.ecount()-1]['id'] = id
#                 G.es[G.ecount()-1][attribute] = g.es[attribute][index]
#     return G



# def merge_networks_v2(glist, attribute):
    
#     glist = sorted(glist, key=lambda g: g.ecount())
#     G =  glist.pop()

#     identifier(glist, 'geocode')
#     identifier([G], 'geocode')

#     for graph in glist:
#         for index, (src, trg) in enumerate(graph.get_edgelist()):
#             id = graph.es['id'][index]
            
#             if id in G.es['id']:
#                 _index = G.es['id'].index(id)
#                 G.es[_index][attribute] += graph.es[attribute][index]
#             else:
#                 src_geocode = graph.vs['geocode'][src]
#                 trg_geocode = graph.vs['geocode'][trg]
                
#                 if src_geocode not in G.vs['geocode'] and trg_geocode not in G.vs['geocode']:
#                     G.add_vertices(2)
#                     G.add_edges([(G.vcount()-2, G.vcount()-1)])

#                     G.vs[G.vcount()-2]['geocode'] = graph.vs['geocode'][src]
#                     G.vs[G.vcount()-2]['x'] = graph.vs['x'][src]
#                     G.vs[G.vcount()-2]['y'] = graph.vs['y'][src]

#                     G.vs[G.vcount()-1]['geocode'] = graph.vs['geocode'][trg]
#                     G.vs[G.vcount()-1]['x'] = graph.vs['x'][trg]
#                     G.vs[G.vcount()-1]['y'] = graph.vs['y'][trg]

#                     G.es[G.ecount()-1]['id'] = id_extractor(graph, src, trg, 'geocode')

#                 elif src_geocode not in G.vs['geocode'] and trg_geocode in G.vs['geocode']:
                    
#                     G.add_vertices(1)
#                     G.add_edges([(G.vcount()-1, trg)])

#                     G.vs[G.vcount()-1]['geocode'] = graph.vs['geocode'][src]
#                     G.vs[G.vcount()-1]['x'] = graph.vs['x'][src]
#                     G.vs[G.vcount()-1]['y'] = graph.vs['y'][src]

#                 else:
#                     G.add_vertices(1)
#                     G.add_edges([(src, G.vcount()-1)])

#                     G.vs[G.vcount()-1]['geocode'] = graph.vs['geocode'][trg]
#                     G.vs[G.vcount()-1]['x'] = graph.vs['x'][trg]
#                     G.vs[G.vcount()-1]['y'] = graph.vs['y'][trg]


#     return G












from datetime import datetime
from utility import *
def main(graph, graph_name):

    dataframe = {}
    _tuple = []

    x_axis = [x for x in range(graph.vcount())]
    covid_cases_geocodes = list(pd.read_csv('out/csv/'+graph_name+'.csv')['geocode'])
    dataframe['covid_cases_geocode'] = covid_cases_geocodes
    
    start = datetime.now()

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


    end = datetime.now()

    print(f' the cost time is {end-start}')
    # graphPloter(_tuple, ["$k$", "$b$"], graph_name)
    graphPloter(_tuple, ["$k$", "$b$", "$s$", "$b_{w}$"], graph_name)


    df = pd.DataFrame(dataframe)
    dirMaker('out/csv/processed')
    df.to_csv('out/csv/processed/'+graph_name+'.csv')


name = 'fluvial_&_terrestrial'
graph = Graph.Read_GraphML('in/'+name+'.GraphML')
graph.vs['geocode'] = graph.vs['id']  
graph.es['weight'] = [x if x > 0 else 0.00001 for x in graph.es['weight']] 

main(graph, name)