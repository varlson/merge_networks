from os import system
import igraph as ig
import numpy as np
def subnet_extractor(network, attribute, reference, ref_label):
    state_flag = [ref_label if str(geo)[:2] == reference else None for geo in network.vs[attribute]]
    gcopied = network.copy()
    gcopied.vs['state'] = state_flag
    subnet = gcopied.vs.select(state=ref_label)
    subnet = gcopied.subgraph(subnet)
    deg = [x+1 if x != 0 else 1 for x in subnet.degree()]
    node_size = (deg/np.max(deg)*10)+8
    subnet.vs['width'] = 10
    subnet.es['width'] = 1
    return subnet




def for_vibsualization_purpose(g, G, color):
    for lab in g.vs['label']:
        index = G.vs['label'].index(lab)
        G.vs[index]['color']  = color
    return G


def main():
    name = 'aerialUTP'
    folder = 'sao_paulo'
    prefixo = 'SP'
    code = '35'
    full_name = f'{prefixo}_{name}'

    fluvial = ig.Graph.Read_GraphML(f'in/{name}.GraphML')
    subnet = subnet_extractor(fluvial, 'geocode', code, prefixo)

    ig.Graph.write(subnet, f'out/{folder}/networks/{full_name}.GraphML')
    ig.plot(subnet, f'out/{folder}/plots/net/{full_name}.png')

if __name__ == '__main__':
    main()