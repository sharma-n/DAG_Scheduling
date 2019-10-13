import pydot
import numpy as np
from random import randint, gauss

def read_dag(filename, p=3, b=0.5, ccr=0.5):
    graph = pydot.graph_from_dot_file(filename)[0]
    n_nodes = len(graph.get_nodes())

    # get adjacency matrix for DAG
    adj_matrix = np.full((n_nodes, n_nodes), -1)
    n_edges = 0
    for e in graph.get_edge_list():
        adj_matrix[int(e.get_source())-1][int(e.get_destination())-1] = 0
        n_edges += 1

    # if DAG has multiple entry/exit nodes, create dummy nodes in its place
    ends = np.nonzero(np.all(adj_matrix==-1, axis=1))[0]    # exit nodes
    starts = np.nonzero(np.all(adj_matrix==-1, axis=0))[0]  # entry nodes
    start_node = pydot.Node("0", alpha="\"0\"", size="\"0\"")
    end_node = pydot.Node(str(n_nodes+1), alpha="\"0\"", size="\"0\"")
    graph.add_node(start_node)
    graph.add_node(end_node)

    for start in starts:
        s_edge = pydot.Edge("0", str(start+1), size="\"0\"")
        graph.add_edge(s_edge)
        
    for end in ends:
        e_edge = pydot.Edge(str(end+1), str(n_nodes+1), size="\"0\"")
        graph.add_edge(e_edge)

    n_nodes = len(graph.get_nodes())

    # construct computation matrix
    comp_matrix = np.empty((n_nodes, p))
    comp_total = 0
    for n in graph.get_node_list():
        size_str = n.obj_dict['attributes']['alpha']
        size = float(size_str.split('\"')[1])
        if size==0:
            comp_matrix[int(n.get_name())][:] = 0
        else:
            comp_temp = np.random.randint(size*(1-b/2), high=size*(1+b/2), size=p)
            comp_temp[comp_temp==0] = 1
            comp_matrix[int(n.get_name())][:] = comp_temp
            comp_total += np.average(comp_temp)

    #get modified adjency matrix
    adj_matrix = np.full((n_nodes, n_nodes), -1)
    mu = ccr*comp_total/n_edges
    for e in graph.get_edge_list():
        source, dest = int(e.get_source()), int(e.get_destination())
        if source == 0 or dest == n_nodes -1:
            adj_matrix[source][dest] = 0
        else:
            adj_matrix[int(e.get_source())][int(e.get_destination())] = abs(gauss(mu, mu/4))
    
    return [n_nodes, p, comp_matrix, adj_matrix]


if __name__ == "__main__":
    n_nodes, p, comp_matrix, adj_matrix = read_dag('dag/10_0.1_0.2_0.2_1.dot')
    print('No. of nodes: {}\nNo. pf processors: {}\nComputation Matrix:\n{}\nAdjacency Matrix:\n{}\n'.format(
        n_nodes, p, comp_matrix, adj_matrix))