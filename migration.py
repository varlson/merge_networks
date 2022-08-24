from utility import sort_by_metric, dirMaker, export_csv
import igraph as ig
import pandas as pd
import sys
path = 'vanderVersion'
out_path = f'{path}/'
net_group_name = sys.argv[1]
net_name = ''

print(f'size {sys.argv[1]} {sys.argv[2]}')

if len(sys.argv) >= 4:
    net_name = f'{sys.argv[2]}_&_{sys.argv[3]}'
else:
     net_name = sys.argv[2]

full_out = f'{path}/out/{net_group_name}'

print(f'path {full_out}')
dirMaker(f'{full_out}/metric')
dirMaker(f'{full_out}/cities')


def exporter(sorted_by_metric):
    nodes = [data[0] for data in sorted_by_metric]
    geocode = [int(data[1]) for data in sorted_by_metric]
    value = [data[2] for data in sorted_by_metric]
    dataframe = {}
    dataframe['city_number'] = nodes
    dataframe['city_code'] = geocode
    dataframe['metric'] = value

    # 'city_number', 'city_code', 'metric'

    df = pd.DataFrame(dataframe)
    print(df)
    df.to_csv(f'{full_out}/metric/{net_name}.csv', index=False)

def migrator():
    g = ig.Graph.Read_GraphML(f'out/{net_group_name}/networks/{net_name}.GraphML')
    g.es['weight'] = [x if x >0 else 0.00001 for x in g.es['weight']]
    try:
        g.vs['geocode'] = g.vs['id']
    except:
        pass
    sorted_by_metric = sort_by_metric(g, 'degree')
    exporter(sorted_by_metric)
    df = pd.read_csv('in/cases-brazil-cities-time.csv')
    g.vs['id'] = g.vs['geocode']
    export_csv(g, df, net_name, f'{full_out}/cities')


if __name__ == '__main__':
    print('migration...........')
    migrator()
