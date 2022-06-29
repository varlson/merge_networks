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