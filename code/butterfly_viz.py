import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from pyvis import network as net
import json
from os import listdir

import datashader as ds
import datashader.transfer_functions as tf
from datashader.bundling import hammer_bundle


# Load the ASCT+B tables (JSON files)
def load_data(directory):
    # Load json files 
    json_data_asctb = {}
    for filename in listdir(directory):
        if '.json' in filename:
            # print(filename)
            with open(f'{directory}{filename}', encoding='utf8') as json_file:
                data = json.load(json_file)

            json_data_asctb[filename[:-5]] = data
    return json_data_asctb


json_data_asctb = load_data('./asct+b/v14/')


organ_order = ['trachea', 'main_bronchus', 'lung', 'heart', 'spinal_cord', 'brain', 'eye', 'skin',
               'thymus', 'lymph_nodes', 'spleen', 'liver', 'pancreas', 
               'small_intestine', 'large_intestine', 'kidney', 'urinary_bladder', 'ureter', 'prostate', 
               'ovary', 'fallopian_tube', 'uterus', 'placenta_full_term', 'knee', 'bone_marrow']



json_data_asctb = {organ: json_data_asctb[organ] for organ in organ_order}



# Merge the ASCT+B tables and create the network

def combine_data(json_dat, remove_ctct=True, combine=True, blood=False, verbose=False):
    """
    combine_data takes the json data of the organs and returns the node and edge lists in pandas dataframes

    :param json_dat: data of all the organs in a json format that was loaded by the load_data function
    :param remove_ctct: There should not be edges between CT and CT, however sometimes there can be mistakes in the data files. 
    :param combine: if true then the organs are combined into one network, and the function outputs 2 dataframes: nodes and edges. 
                    if false, then the organs are not combined, the function returns a node and an edge table for each organ.
    :param blood: By default it is false, and in this case, the function ignores the following tables: 'blood_pelvis', 'blood_vasculature', 
                 'lymph_vasculature', and 'peripheral_nervous_system'. If true, then 'blood_vasculature' is not excluded.

    """ 
    nodes_data = []
    edges_data = []
    organ_names = ['body']
    
    # The numbering of the nodes starts from 1 in each organ
    # If we combine the organs, we need a new id
    node_id_start_point = 1 
    
    #Add the 'body' node to the nodes data:
    body_df = pd.DataFrame(json_dat['brain']['nodes']).head(1)
    body_df.index = body_df['id']
    body_df['id_old'] = 0
    body_df['organ'] = 'body'
    body_df['ontology_id'] = 'UBERON:0013702'
    
    nodes_data += [body_df[['id', 'id_old', 'name', 'type', 'organ', 'ontology_id']]]
    
    if not combine:
        body_data = body_df[['id', 'id_old', 'name', 'type', 'organ', 'ontology_id']].copy()
    
    if blood:
        exclude = ['blood_pelvis', 'lymph_vasculature', 'peripheral_nervous_system']
    else:
        exclude = ['blood_pelvis', 'blood_vasculature', 'lymph_vasculature', 'peripheral_nervous_system']
    
    for name in json_dat.keys():
        if name in exclude:
            continue
        else:
            # print(name)
            organ_names += [name]
            # Combine nodes:
            organ_nodes = pd.DataFrame(json_dat[name]['nodes']).iloc[1:,:]
            not_as_ct_nodes = organ_nodes[~organ_nodes['type'].isin(['AS', 'CT'])]['id'] #filter for AS and CT
            organ_nodes['id_old'] = organ_nodes['id'].copy()
            if combine:
                organ_nodes['id'] = organ_nodes['id'].add(node_id_start_point-1)
            organ_nodes.index = organ_nodes['id']
            # organ_nodes = organ_nodes.drop(columns=['id'])
            organ_nodes = organ_nodes[organ_nodes['type'].isin(['AS', 'CT'])]
            organ_nodes['organ'] = name
            organ_nodes['ontology_id'] = organ_nodes['metadata'].apply(lambda x: x['ontologyId'])
            organ_nodes = organ_nodes[['id', 'id_old', 'name', 'type', 'organ', 'ontology_id']]
            

            # Combine edges:
            organ_edges = pd.DataFrame(json_dat[name]['edges'])
            ## Remove CT-CT edges:
            if remove_ctct:
                organ_nodes_original = pd.DataFrame(json_dat[name]['nodes'])
                organ_nodes_original.index = organ_nodes_original['id']
                organ_edges['source_type'] = organ_edges['source'].apply(lambda x: organ_nodes_original.loc[x]['type'])
                organ_edges['target_type'] = organ_edges['target'].apply(lambda x: organ_nodes_original.loc[x]['type'])
                organ_edges = organ_edges[(organ_edges['source_type']=='AS')|(organ_edges['target_type']=='AS')]
            ##rename edges due to colliding ids
            organ_network = nx.from_pandas_edgelist(organ_edges)
            #remove unnecessary edges:
            organ_network.remove_nodes_from(not_as_ct_nodes.to_list())
            # Remove body-organ edge (we will add it later)
            organ_network.remove_edge(0, 1)
            organ_network.remove_node(0)
            #rename nodes
            # organ_network = nx.relabel_nodes(organ_network, organ_nodes['name'].to_dict())
            if combine:
                organ_network = nx.convert_node_labels_to_integers(organ_network, first_label=node_id_start_point)
            #add body-organ edge
            # organ_network.add_node(0) 
            # nx.set_node_attributes(organ_network, {0: {"type": 'AS', "name": "Body", 'organ': 'body', 'ontology_id': 'UBERON:0013702'}})
            if combine:
                organ_network.add_edge(0, node_id_start_point) #add body-organ edge
                #v1.4 correction:
                if name=='lung':
                    organ_network.add_edge(node_id_start_point, 63+node_id_start_point-1)  #connect lung to pulmonary vascular system
                    organ_network.add_edge(node_id_start_point, 69+node_id_start_point-1)  #connect lung to systemic artery
                    organ_network.add_edge(node_id_start_point, 73+node_id_start_point-1)  #connect lung to venous blood vessel

                elif name=='trachea':
                    organ_network.add_edge(node_id_start_point, 15+node_id_start_point-1)  #connect trachea to bronchial vein
                    organ_network.add_edge(node_id_start_point, 18+node_id_start_point-1)  #connect trachea to bronchial artery
                    
                elif name=='main_bronchus':
                    organ_network.add_edge(node_id_start_point, 10+node_id_start_point-1) #connect trachea to bronchial artery
                    organ_network.add_edge(node_id_start_point, 13+node_id_start_point-1) #connect trachea to bronchial vein
                    
            else:
                organ_network.add_edge(0, 1) #add body-organ edge
                
                #v1.4 corrections:
                if name=="lung":
                    organ_network.add_edge(0, 63) #connect lung to pulmonary vascular system
                    organ_network.add_edge(0, 69) #connect lung to systemic artery
                    organ_network.add_edge(0, 73) #connect lung to venous blood vessel

                elif name=="trachea":
                    organ_network.add_edge(0, 15) #connect trachea to bronchial vein
                    organ_network.add_edge(0, 18) #connect trachea to bronchial artery

                elif name=='main_bronchus':
                    organ_network.add_edge(0, 10) #connect trachea to bronchial artery
                    organ_network.add_edge(0, 13) #connect trachea to bronchial vein


                

            # Create CT duplicates
            organ_CT_nodes = organ_nodes[organ_nodes['type']=='CT'].copy()
            organ_CT_nodes['degree'] = dict(organ_network.degree(organ_CT_nodes['id'])).values()
            
            ct_nodes_to_copy = organ_CT_nodes[organ_CT_nodes['degree']>1]['id'].values
            edges_to_remove = []
            edges_to_add = []
            
            for ct_node in ct_nodes_to_copy:
                as_neighbors_of_ct = list(nx.neighbors(organ_network, ct_node))
                for ind, as_neighbor in enumerate(as_neighbors_of_ct):
                    if ind==0:
                        continue
                    else:
                        ct_node_details = organ_nodes.loc[ct_node].to_dict()
                        new_node_id = organ_nodes['id'].max()+1
                        ct_node_details['id'] = new_node_id
                        # organ_nodes = organ_nodes.append(ct_node_details, ignore_index=False)
                        organ_nodes.loc[new_node_id] = ct_node_details
                        
                        edges_to_remove += [(as_neighbor, ct_node)]
                        edges_to_add += [(as_neighbor, new_node_id)]

            if verbose:
                print(name)
                print(f'Number of deleted edges: {len(edges_to_remove)}')
                print(f'Number of added edges: {len(edges_to_add)}')
                
            organ_network.remove_edges_from(edges_to_remove)
            organ_network.add_edges_from(edges_to_add)
                
            
            
            nodes_data += [organ_nodes]
            if not combine:
                nodes_data[-1] = pd.concat([body_data, nodes_data[-1]])
            
            node_id_start_point = max(organ_network.nodes)+1
            
            organ_edges = nx.to_pandas_edgelist(organ_network)[['source', 'target']]
            print(f"{name} is tree: {nx.is_tree(organ_network)}", end='\n_____________\n')
            edges_data += [organ_edges]

    if combine:
        return pd.concat(nodes_data, ignore_index=True), pd.concat(edges_data, ignore_index=True)
    else:
        return dict(zip(organ_names, nodes_data)), dict(zip(organ_names[1:], edges_data))
    
    
    
# All nodes and edges in a graph
nodes, edges = combine_data(json_data_asctb, remove_ctct=True, combine=True)



# Construction of the network using networkx

whole_graph = nx.from_pandas_edgelist(edges)

# For visualizing it in Vega, we need the parent node
def get_parent(node, graph):
    neighbors = nx.neighbors(graph, node)
    
    return min(neighbors)



nodes['parent'] = nodes['id'].apply(get_parent, graph=whole_graph)


# Set the colors of the nodes (AS: purple, CT: orange, FTUs: green)

## The 22 FTUs
FTUs = ['UBERON:0001229', 'UBERON:0001285', 'UBERON:0004134', 'UBERON:0001292', 'UBERON:0001232', 'UBERON:0004193', 
        'UBERON:0001289','UBERON:0001291','UBERON:0013485','UBERON:0004647','UBERON:0008870', 'UBERON:8410043',
        'UBERON:0000006','UBERON:0001263','UBERON:0007329','UBERON:0004179','UBERON:0001003','UBERON:0002067',
        'UBERON:0001213','UBERON:0001959','UBERON:0001250','UBERON:0002125']

nodes['color'] = nodes.apply(lambda row: '#56a04e' if row['ontology_id'] in FTUs else ('#984ea0' if row['type']=='AS' else '#ff7f00'), axis=1)

# Convert the data frame to json
nodes_json = nodes[['id', 'name', 'parent', 'type', 'ontology_id', 'color']].to_dict(orient='index')

# the first node shouldn't have a parent
del(nodes_json[0]['parent'])


nodes_json = [nodes_json[i] for i in nodes_json.keys()]

with open('human_atlas_v1.4', 'w', encoding='utf8') as f:
    f.write('[\n')
    for item in nodes_json:
        f.write(f"{json.dumps(item)},\n".replace("'", ''))
    f.write(']')
    
    

# Construct female and male networks and Vega viz

fem_json_data = {organ: json_data_asctb[organ] for organ in organ_order}
del(fem_json_data['prostate']) #delete prostate from female network

male_json_data = json_data_asctb.copy()
del(male_json_data['fallopian_tube'])
del(male_json_data['ovary'])
del(male_json_data['uterus'])
del(male_json_data['placenta_full_term'])


def construct_network_create_vega_viz(jason_data, filename):
    nodes_df, edges_df = combine_data(jason_data, remove_ctct=True, combine=True)
    graph = nx.from_pandas_edgelist(edges_df)
    nodes_df['parent']= nodes_df['id'].apply(get_parent, graph=graph)
    nodes_df['color'] = nodes_df.apply(lambda row: '#56a04e' if row['ontology_id'] in FTUs else ('#984ea0' if row['type']=='AS' else '#ff7f00'), axis=1)
    
    nodes_df['organ_label'] = nodes_df.apply(lambda row: row['name'] if row['id_old']==1 else '', axis=1)
    nodes_json = nodes_df[['id', 'name', 'parent', 'type', 'ontology_id', 'color', 'organ', 'organ_label']].to_dict(orient='index')
    del(nodes_json[0]['parent'])
    nodes_json = [nodes_json[i] for i in nodes_json.keys()]
    

    with open('./viz_v14/vega_config.json', encoding='utf8') as json_file:
        config = json.load(json_file)

    config['data'][0]['values'] = nodes_json
    
    
    # Writing to sample.json
    with open(f"./viz_v14/vega_viz_{filename}.json", "w") as outfile:
        outfile.write(json.dumps(config, indent=4))
    
    return nodes_df, edges_df


_, _ = construct_network_create_vega_viz(fem_json_data, 'female')
_, _ = construct_network_create_vega_viz(male_json_data, 'male')



#####################################################################################################################

# Vasculature network
vasc_data = pd.read_csv('./Vessel.csv', encoding="ISO-8859-1")[['BranchesFrom', 'Vessel', 'ASID', 'VesselType', 'BodyPart', 'BodyPartID', 'PathFromHeart', 'PathFromHeartWithIDs']]


def transform_id(input_id):
    return str(input_id).lower().replace(':', '')


ids_in_organtables = set([transform_id(node) for node in set(nodes.ontology_id)])


# Get matching and non matching vessels
vasc_data['is_in_organ_table'] = vasc_data['ASID'].apply(lambda x: 1 if transform_id(x) in ids_in_organtables else 0)
vasc_data['not_in_organ_table'] = vasc_data['ASID'].apply(lambda x: 0 if transform_id(x) in ids_in_organtables else 1)
vasc_data['#vessels'] = 1

matching_nodes = vasc_data[(vasc_data['is_in_organ_table']==1)&(vasc_data.BodyPart!='testis')]

vasc_edges = vasc_data[['BranchesFrom', 'Vessel', 'VesselType']].copy()

vasc_edges = vasc_edges.rename(columns={'BranchesFrom':'source', 'Vessel': 'target'})
# vasc_edges.to_excel('vasc_edgelist.xlsx')


#Removal of the self-loops
vasc_edges = vasc_edges[vasc_edges.source!=vasc_edges.target]


vasc_graph = nx.from_pandas_edgelist(vasc_edges)

layout_pos_full = nx.drawing.nx_agraph.graphviz_layout(vasc_graph)


plt.figure(figsize=(10,10))
nx.draw(vasc_graph, pos=layout_pos_full, node_size=10)
nx.draw_networkx_nodes(vasc_graph, layout_pos_full, nodelist=['right ventricle'], node_size=10, node_color='tab:orange')
plt.show()



## Construction of the pruned graph

### The graph has to be pruned at the matching nodes
### We start with the layer of matching nodes, and then in each iteration, we get the parent nodes (vessels), i.e. we are moving towards the core of the network in layers.


layer = vasc_edges[vasc_edges.target.isin(matching_nodes.Vessel)]
layers = [layer]
indices = list(layer.index)
while len(layer):
    layer = vasc_edges[(vasc_edges.target.isin(layer.source)) & (~vasc_edges.index.isin(indices))]
    layers += [layer]
    indices += list(layer.index)
    
    
    
pruned_vasc_edges = vasc_edges[vasc_edges.index.isin(indices)]

pruned_vasc_graph = nx.from_pandas_edgelist(pruned_vasc_edges)

pruned_vasc_graph = nx.induced_subgraph(vasc_graph, set(pruned_vasc_graph.nodes).union(set(matching_nodes.Vessel.values)))


layout_pos = nx.drawing.nx_agraph.graphviz_layout(pruned_vasc_graph)
nx.draw(pruned_vasc_graph, pos=layout_pos, node_size=10)



organ_mapping = {'eye': 'eye', 'heart': 'heart', 
                 'heart chamber': 'heart', # heart chamber -> heart
                 'kidney': 'kidney',  'liver': 'liver', 'lung': 'lung', 'ovary': 'ovary', 
                 'pelvis': 'placenta_full_term', #pelvis -> placenta
                 'spleen': 'spleen', 'thymus': 'thymus', 
                 'thyroid gland': 'lung', #thyroid gland -> lung
                 'uterus': 'uterus'}


def get_coordinates_4_vessels(visualization, graph=pruned_vasc_graph):
    name = []
    name_in_vasc = []
    coords=[]
    organs = []
    for node in visualization:
        if transform_id(node['ontology_id']) in matching_nodes['ASID'].apply(transform_id).values: #if the node is in the vascular data 
            if node['organ']==matching_nodes[matching_nodes['ASID'].apply(transform_id)==transform_id(node['ontology_id'])]['organ'].values[0]: # and if the organs match
                name += [node['name']]
                name_in_vasc += [matching_nodes[matching_nodes['ASID'].apply(transform_id)==transform_id(node['ontology_id'])]['Vessel'].values[0]]
                coords += [np.array([node['x'], -node['y']])]
                organs += [node['organ']]

    for node in graph:
        if node not in name_in_vasc:
            name += [node]
            name_in_vasc += [node]
            coords += [np.nan]
            organs += [np.nan]

    art_data = pd.DataFrame.from_dict({'name': name, 'name_in_vasc': name_in_vasc,
                                       'organ': organs, 'coords': coords})
    
    art_data = art_data.drop_duplicates(subset=['name_in_vasc', 'organ']).reset_index(drop=True) 
    
    art_data = art_data[art_data.name_in_vasc.isin(graph.nodes())]
    
    return art_data







def plot_fixed_graph2(graph, viz, bundle_edges=False, draw_labels=False, filename='vasculature'):
    graphs = {'veins': nx.induced_subgraph(graph, veins), 'arteries': nx.induced_subgraph(graph, arteries)}
    coords = {'veins': get_coordinates_4_vessels(viz, graphs['veins']), 'arteries': get_coordinates_4_vessels(viz, graphs['arteries'])}
    relabel_mapping_inv = {'veins': coords['veins']['name_in_vasc'].to_dict(), 'arteries': coords['arteries']['name_in_vasc'].to_dict()}
    relabel_mapping =  {'veins': {v: k for k, v in relabel_mapping_inv['veins'].items()}, 'arteries':{v: k for k, v in relabel_mapping_inv['arteries'].items()}}
    # {'veins': , 'arteries': }
    renamed_comp = {'veins': nx.relabel_nodes(graphs['veins'], relabel_mapping['veins']), 'arteries': nx.relabel_nodes(graphs['arteries'], relabel_mapping['arteries']) } 
    
    pos = {'veins': coords['veins']['coords'].dropna().to_dict(), 'arteries': coords['arteries']['coords'].dropna().to_dict()}
    pos['veins'][relabel_mapping['veins']['blood vasculature']] = np.array([body_x-10, -body_y])
    pos['arteries'][relabel_mapping['arteries']['blood vasculature']] = np.array([body_x-10, -body_y])
    pos2 = {'veins': nx.spring_layout(renamed_comp['veins'], pos=pos['veins'], fixed=list(pos['veins'].keys()), seed=10, iterations=1000, dim=2, k=0.01/np.sqrt(len(graphs['veins']))), 
            'arteries': nx.spring_layout(renamed_comp['arteries'], pos=pos['arteries'], fixed=list(pos['arteries'].keys()), seed=10, iterations=1000, dim=2, k=0.01/np.sqrt(len(graphs['arteries'])))}
    
    if not bundle_edges:
        plt.figure(figsize=(23.8888888889,23.8888888889))
        plt.axes().set_aspect('equal')
        plt.margins(x=0, y=0)
        plt.xlim(0,1720)
        plt.ylim(-1720, 0)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0, hspace=0, wspace=0)
        plt.tight_layout(pad=0, h_pad=0, w_pad=0, rect=(0,0,1,1))
        plt.axis('off') 
        nx.draw(renamed_comp['veins'], pos2['veins'], node_size=10, edge_color='tab:blue', node_color='tab:blue')
        nx.draw(renamed_comp['arteries'], pos2['arteries'], node_size=10, edge_color='tab:red', node_color='tab:red')
        if draw_labels:
            nx.draw_networkx_labels(renamed_comp['veins'], pos2['veins'], labels=relabel_mapping_inv['veins'], font_size=3)
            nx.draw_networkx_labels(renamed_comp['arteries'], pos2['arteries'], labels=relabel_mapping_inv['arteries'], font_size=3)
        # nx.draw_networkx_nodes(renamed_comp, pos2, nodelist=list(pos.keys()), node_color='tab:orange', node_size=10)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.tight_layout(pad=0, h_pad=0, w_pad=0, rect=(0,0,1,1))
        plt.axis('off')
        plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        plt.margins(0,0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.savefig(f'./viz_v13/{filename}_v13.pdf',  transparent=True, pad_inches=0.0, bbox_inches=0)
        plt.show()
    else:
        nodes_only = {'veins': pd.DataFrame.from_dict(relabel_mapping_inv['veins'], orient='index').rename(columns={0:'name'}), 
                      'arteries': pd.DataFrame.from_dict(relabel_mapping_inv['arteries'], orient='index').rename(columns={0:'name'})}
        
        nodes = {'veins': pd.DataFrame.from_dict(pos2['veins']).T.rename(columns={0:'x', 1:'y'}).join(nodes_only['veins'])[['name', 'x', 'y']], 
                 'arteries': pd.DataFrame.from_dict(pos2['arteries']).T.rename(columns={0:'x', 1:'y'}).join(nodes_only['arteries'])[['name', 'x', 'y']]}
        
        edges = {'veins': nx.to_pandas_edgelist(renamed_comp['veins'])[['source', 'target']], 
                 'arteries': nx.to_pandas_edgelist(renamed_comp['arteries'])[['source', 'target']]}
        # hb = hammer_bundle(nodes, edges, initial_bandwidth=0.03,tension=0.9, accuracy=8000)
        hb = {'veins': hammer_bundle(nodes['veins'], edges['veins'], initial_bandwidth=.015, decay=0.8, tension=0.99, accuracy=1000), 
              'arteries': hammer_bundle(nodes['arteries'], edges['arteries'], initial_bandwidth=.015, decay=0.8, tension=0.99, accuracy=1000)}
        
        plt.figure(figsize=(23.8888888889,23.8888888889))
        plt.axes().set_aspect('equal', anchor="NW")
        plt.margins(x=0, y=0)
        plt.xlim(0,1720)
        plt.ylim(-1720, 0)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0, hspace=0, wspace=0)  
        plt.plot(hb['veins']['x'], hb['veins']['y'], color='tab:blue', alpha=0.8)
        plt.plot(hb['arteries']['x'], hb['arteries']['y'], color='tab:red', alpha=0.8)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.tight_layout(pad=0, h_pad=0, w_pad=0, rect=(0,0,1,1))
        plt.axis('off')
        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0,0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.savefig(f'./viz_v13/{filename}_bundled_v13.pdf', pad_inches=0.0, transparent=True, bbox_inches=0)
        plt.show()
        
        
        
with open('viz_v13/female_wing_viz_v14.json', encoding='utf8') as json_file:
    viz = json.load(json_file)
    
    
female_wing_viz = viz['data'][0]['values']


plot_fixed_graph2(pruned_vasc_graph_comp_female, female_wing_viz, draw_labels=True, filename='female_wing')
plot_fixed_graph2(pruned_vasc_graph_comp_female, female_wing_viz, bundle_edges=True, filename='female_wing')

with open('viz_v13/male_wing_viz_v13.json', encoding='utf8') as json_file:
    viz = json.load(json_file)
    
    
male_wing_viz = viz['data'][0]['values']
    
plot_fixed_graph2(pruned_vasc_graph_comp_male, male_wing_viz, draw_labels=True, filename='male_wing')
plot_fixed_graph2(pruned_vasc_graph_comp_male, male_wing_viz, bundle_edges=True, filename='male_wing')
