#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import numpy as np
import networkx as nx
from simulator.Matrix_Definition import Graph_Generation
from simulator.group_generator import GP_generator
from solver.Multicast import MultiCast
from heuristic.Heu import *

#np.random.seed(11)

if __name__ == '__main__':
    log_name = "./logs/main.log"
    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO, datefmt="%H:%M:%S",
        filemode='w'
    )

    fp = open("./etc/config.json", 'r')
    sim_setting = json.load(fp)
    fp.close()
    
    '''
    Graph G generation
    '''
    G = nx.Graph()
    # graph G configuration
    Graph_Generation_run = Graph_Generation(G)
    Graph_Generation_run.Node_Generator()
    Graph_Generation_run.Edge_Generator()
    Graph_Generation_run.Real_Matrix()
    matrix = Graph_Generation_run.Cost_Assignment()

    # to see raw graph uncomment below line
    Graph_Generation_run.plot()
    
#============== Print graph configuration ==============
    print('\n============ Graph configuration ============')  
    print(f"number of nodes: {G.order()}")
    print(f"number of edges: {G.size()}")
    
    '''
    Group generator
    takes configured graph G as input
    '''
    available_nodes = list(G.nodes)
    gp_counter = 1
    gp_container = []
    for i in range(1, sim_setting['n_multicast_group']+1):
        print('\n================= group', i, '=================')
        locals()["gp" + str(i)] = GP_generator(G, available_nodes, i)
        locals()["gp" + str(i)].source_selector()
        group = locals()["gp" + str(i)].destination_selector()
        # locals()["gp" + str(i)].plot()
        gp_container.append(group)
        


#============== Exact method ==============
    print('\nComputing the result please wait, it might take a while...')
    prb = MultiCast()
    status, of, sol_x, sol_f, comp_time = prb.solve(
        G,
        matrix,
        gp_container,
    )
    
    
    print("\n============ Exact method result ============")
    if status == 'Optimal':
        print('\nminimum cost :', of)
        print('computation time:', round(comp_time, 4),'seconds')
        optimal_E = True

    else:
        print('\nNo feasbile solution found! Try again')
        optimal_E = False

#============== Heuristic method ==============
    print("\n============ Heuristic method result ============\n")
    heuristic_result = heu(gp_container, G, matrix)
    optimal_H = heuristic_result [2]
    
    if type(heuristic_result) == int or type(heuristic_result) == float:
        if type(of) == int or type(of) == float:
            if heuristic_result < of:
                penalized = of -  heuristic_result
                result = heuristic_result + penalized
                print("\nHeuristic Minimum Cost (Penalized):",result)
                
#============== print path? ==============
while (optimal_E) or (optimal_H):
    answer = input('Do you want the paths to be printed as well?\npress "y" yes or "n" no:\n')
    if answer in ['y', 'Y'] and optimal_E:
        print("\n============ Exact method path ============")
        print('format : ((node i, node j, group number), flow_i,j on that group)')
        for g in range(len(gp_container)):
            print('\nchosen edges and corresponding flows in group {} are {}:'.format(g+1, sol_f[g]))
        if optimal_H:
            print("\n============ Heuristic method path ============")
            print (heuristic_result[1])
        break
    elif answer in ['n', 'N']:
        break
    else:
        print("Invalid input!")
print ('\nFinished!')