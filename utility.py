from operator import ge
from igraph import *
import numpy as np
import pandas as pd
from scipy.stats import spearmanr as spearman
import matplotlib.pyplot as plt 
from os import mkdir,path


def sort_by_metric(graph, metric):
    
    switcher = {

        "degree": [(graph.vs[index]['geocode'], x) for index, x in enumerate(graph.degree())],
        "betweenness":[(graph.vs[index]['geocode'], x) for index, x in enumerate(graph.betweenness())],
        "strength": [(graph.vs[index]['geocode'], x) for index, x in enumerate(graph.strength(weights = graph.es['weight']))],
        "betweenness_w": [(graph.vs[index]['geocode'], x) for index, x in enumerate(graph.betweenness(weights = graph.es['weight']))] 
    }
    

    done = switcher.get(metric)
    done = sorted(done, key=lambda data: data[1], reverse=True )
    return done


def counter(graph_geocode, covid_cases_geocode, index):
    count=0

    for geo in graph_geocode[:index]:
        if geo in covid_cases_geocode[:index]:
            count+=1
    return (count/(index))

def correspondence_processor(graph_geocode, covid_cases_geocode):
    correspondence = []
    for index, geo in enumerate(graph_geocode):
        correspondence.append(counter(graph_geocode, covid_cases_geocode, index+1))

    return correspondence


def graphPloter(list_of_coord, labels, full_path, name="teste"): 
    plt.clf()
    # print(f'dados {list_of_coord}')
    for index, coord in enumerate(list_of_coord):
        x = coord[0]
        y = coord[1]
        sper = coord[2]
        corr = "{:.8f}".format(sper[0])
        pval = "{:.8f}".format(sper[1])
        plt.plot(x, y, label=labels[index]+' sp: '+corr+' pv: '+pval, marker="1")
    
    plt.legend()
    plt.title(name)
    dirMaker(full_path)
    plt.savefig(f'{full_path}/{name}.png')


def dirMaker(dir):
    if not len(dir):
        print('invalid path')
        return 0
    
    subdirs = dir.split('/')
    fullPath =[]
    
    for index, dir in enumerate(subdirs):
        if not index:
            fullPath.append(dir)
        else:
            fullPath.append(fullPath[index-1]+'/'+dir)
    # print(fullPath)
    
    try:
        for p in fullPath:
            if not path.isdir(p):
                mkdir(p)
    except:
        print('Houve umerro, verifique o path inserito se esta no formato uma_pasta/outra_pasta/...')
        return 0



def export_csv(g, dataframe, name, dir):
    df = {}
    lst_geo = []
    lst_cit = []
    lst_geocode = list(dataframe['ibgeID'])
    lst_cities = list(dataframe['city'])

    for index, geo in enumerate(lst_geocode):
        if geo in g.vs['id']:
            if geo not in lst_geo:
                lst_geo.append(geo)
                print(len(lst_cit))
                lst_cit.append(lst_cities[index])
    
    print(f'{len(lst_geo)} {len(lst_cities)}')

    df['cities'] = lst_cit
    df['geocode'] = lst_geo
    df = pd.DataFrame(df)
    df.to_csv(f'{dir}/{name}.csv')


def export(glist, glabel_list, output_dir):
    dirMaker(output_dir)
    for index, g in enumerate(glist):
        try:
            node_size = (g.degree()/np.max(g.degree())*10)+8
        except:
            pass
        g.vs['width'] = node_size
        g.es['width'] = 1
        plot(g, output_dir+'/'+glabel_list[index]+'.png')
    Graph.write(glist[-1], output_dir+'/'+glabel_list[-1]+'.GraphML')


if __name__ == '__main__':

    te_ae = Graph.Read_GraphML('out/amazonas/networks/terrestrial_&_aerial.GraphML')
    fl_ae = Graph.Read_GraphML('out/amazonas/networks/fluvial_&_aerial.GraphML')
    fl_te = Graph.Read_GraphML('out/amazonas/networks/fluvial_&_terrestrial.GraphML')
    
    fl_ae.vs['geocode'] = fl_ae.vs['id']
    fl_te.vs['geocode'] = fl_te.vs['id']
    te_ae.vs['geocode'] = te_ae.vs['id']


    # summary(fl_ae)
    # # summary(fl_te)
    # summary(te_ae)

    df = pd.read_csv('in/cases-brazil-cities-time.csv')

    export_csv(fl_ae, df, 'fluvial_&_aerial', 'out/amazonas/csv')
    export_csv(fl_te, df, 'fluvial_&_terrestrial', 'out/amazonas/csv')
    export_csv(te_ae, df, 'terrestrial_&_aerial', 'out/amazonas/csv')
