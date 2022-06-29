from random import randint
import igraph as ig
import numpy as np
import pandas as pd



def export(glist, glabel_list, output_dir):
    from utility import dirMaker
    dirMaker(output_dir)
    for index, g in enumerate(glist):
        # node_size = (g.degree()/np.max(g.degree())*10)+8
        # g.vs['width'] = node_size
        # g.es['width'] = 0.9
        ig.plot(g, output_dir+'/'+glabel_list[index]+'.png')



def id_extractor(graph, src,trg, attribute):
    src_geo = graph.vs['id'][src]
    trg_geo = graph.vs['id'][trg]
    _max, _min = max(src_geo, trg_geo), min(src_geo, trg_geo)
    return str(int(_max))+str(int(_min))


def identifier(glist, attribute="geocode"):
    for graph in glist:
        for index,  (src, trg) in enumerate(graph.get_edgelist()):
            id = id_extractor(graph, src, trg,attribute)
            graph.es[index]['id'] = id


def edge_extractor(glist, attribute, all_unique_verttex_id):
    all_edges ={}
    for g in glist:
        for index, (src, trg) in enumerate(g.get_edgelist()):
            src_geo = g.vs['id'][src]
            trg_geo = g.vs['id'][trg]
            
            vertex_src, vertex_trg = all_unique_verttex_id.index(src_geo), all_unique_verttex_id.index(trg_geo) 
            id = id_extractor(g,src, trg, attribute)
            if id not in list(all_edges.keys()):
                all_edges[id] = [vertex_src, vertex_trg, g.es[index][attribute]]
            else:
                current_data = all_edges[id]
                current_weigth = current_data[2]
                current_weigth += g.es[index][attribute]
                current_data[2] = current_weigth
                all_edges.update({id : current_data})
    return all_edges



def merge_networks(glist, attribute):
    all_unique_verttex_id = []
    x_coords = []
    y_coords = []
    

    for graph in glist:
        ig.summary(graph)
        for index, id in enumerate(graph.vs['id']):
            if id not in all_unique_verttex_id:
                all_unique_verttex_id.append(id)
                x_coords.append(graph.vs[index]['x'])
                y_coords.append(graph.vs[index]['y'])
    N = len(all_unique_verttex_id)
    G = ig.Graph(N)

    G.vs['x'] = x_coords
    G.vs['y'] = y_coords
    G.vs['id'] = all_unique_verttex_id

    all_unique_edge = edge_extractor(glist, attribute, all_unique_verttex_id)

    for index, (key, val) in enumerate(all_unique_edge.items()):
        [src, trg, weight] = val
        G.add_edge(src, trg, weight=weight)
    
    return G


def coord_setter(g):
    dataFrame = pd.pandas.read_csv('in/cities_coord.csv')
    for index,node in enumerate(g.vs['id']):
        i = -1
        try:
            i = list(dataFrame['geocode']).index(node)
            g.vs[index]['x'] = list(dataFrame['x'])[i]
            g.vs[index]['y'] = -1 * list(dataFrame['y'])[i]
        except:
            print(node, end=" ")
            print("nao tem")
            pass




def calculator(glist, g_result):
    all_edges  = []
    identifier(glist, 'id')
    identifier([g_result], 'id')
    for g in glist:
        all_edges += [x for x in g.es['id'] if x not in all_edges]

    print(f'size of all_net {len(all_edges)}')
    print(f'size of merged {g_result.ecount()}')




def main(g_list, attribute):
    G = merge_networks(g_list, attribute)
    g_lst = g_list+[G]
    export(g_lst,['g1', 'g2', 'final'], 'teste_de_merge')
    
    calculator(g_list, G)


if __name__ == '__main__':

    rede_1 = ig.Graph.Read_GraphML("in/fluvial.GraphML")
    rede_2 = ig.Graph.Read_GraphML("in/aerialUTP.GraphML")
    
    rede_1.vs['id'] = rede_1.vs['geocode']
    rede_2.vs['id'] = rede_2.vs['geocode']

    # rede_2 = rede_1.copy()

    # rede_2.delete_edges(rede_2.get_eid(5,3))
    # rede_2.delete_edges(rede_2.get_eid(1,2))

    # rede_2.delete_vertices(6)
    # rede_2.delete_vertices(6)


    # rede_1.delete_edges(rede_1.get_eid(5,4))
    # rede_1.delete_edges(rede_1.get_eid(1,0))

    main([rede_2, rede_1], 'weight')



