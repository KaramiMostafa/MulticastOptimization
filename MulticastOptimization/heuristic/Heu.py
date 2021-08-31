#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import networkx as nx
import time
import numpy as np
from itertools import permutations

fp = open("./etc/config.json", 'r')
sim_setting = json.load(fp)
fp.close()

def heu(heu_group, G, matrix):
    ############ Start Permutation ############
    perm = permutations(heu_group) 
    permutation_creation = []
    permutation_result = []
    for i in list(perm): 
        permutation_creation.append(i)
    for permutation_itteration in range(0, len(permutation_creation)):
        computation_time = 0
        start = time.time()
        dict_path_cost = {}
        source_itteration = 0
        final_cost = []
        final_path = []
        value_matrix_constraint = int(sim_setting['total_node'])
        matrix_constraint = np.zeros([value_matrix_constraint, value_matrix_constraint], dtype = int)
        path_constraint = []
        matrix_constraint_copy = matrix_constraint.copy()
        
        ############ Start Group Routing ############
        while source_itteration < int(sim_setting['n_multicast_group']):
            group_path = []
            group = permutation_creation[permutation_itteration][source_itteration]
            heu_source = group.get("source")
            selected_source = heu_source
            group_cost = []
            heu_destinations = group.get("destinations")
            
            ############ Start Source to one destination routing ############
            destinations_itteration = 0
            while destinations_itteration < int(sim_setting['num_destination']):          
                source_constraint = []
                matrix_copy = matrix.copy()
                constraint_destinations = []
                destinations_copy = heu_destinations.copy()
                destinations_copy.remove(heu_destinations[destinations_itteration])
                constraint_destinations.append(destinations_copy)
                
                ############ constraint ############
                for x in range(0, len(constraint_destinations[0])):
                    for y in range(0, int(sim_setting['total_node'])):
                        n = constraint_destinations[0][x]
                        matrix_copy[n][y] = 0
                        matrix_copy[y][n] = 0
                
                ############ constraint ############
                for s in range(0, int(sim_setting['total_node'])):
                    source_constraint.append(matrix_copy[selected_source][s])
                count = 0
                for index, item in enumerate(source_constraint):
                    if item > 0:
                        count = count + 1
                        if count > int(sim_setting['num_destination']):
                            source_constraint[index] = 0
                matrix_copy[selected_source] = source_constraint
                
                ############ constraint ############
                '''
                for i in range (0 , len(path_constraint)):
                    for j in range (0, len(path_constraint[i])-1):
                        n= path_constraint[i][j] 
                        m= path_constraint[i][j+1]
                        matrix_constraint_copy[n][m] = matrix_constraint_copy[n][m] + 1
                        matrix_constraint_copy[m][n] = matrix_constraint_copy[m][n] + 1  
                for i in range(0,value_matrix_constraint):
                    for j in range (0,value_matrix_constraint):
                        if matrix_constraint_copy[i][j] >= int(sim_setting['h']-1):
                            matrix_copy[i][j] = matrix_copy[j][i] = 0
                '''
                
                ############ Start Dijkstra Section ############
                G = nx.from_numpy_matrix(matrix_copy)
                try:
                    cost = nx.dijkstra_path_length(G,selected_source,heu_destinations[destinations_itteration])
                    path = nx.dijkstra_path(G,selected_source,heu_destinations[destinations_itteration])
                    path_constraint.append(path)
                    
                    if len(path_constraint) >= 2:
                        path_constraint.remove(path_constraint[0])
                    
                    group_cost.append(cost)
                    final_cost.append(cost)
                    final_path.append(path)
                    group_path.append(path)

                except nx.NetworkXNoPath:
                    pass

                destinations_itteration = destinations_itteration + 1
            group_cost = sum(group_cost)
            source_itteration = source_itteration + 1
        
        dict_path_cost["Final path"] = final_path
        dict_path_cost["Final cost"] = sum(final_cost)

        end = time.time()
        computation_time = end - start
        permutation_result.append(dict_path_cost)

    ############ Select Best Rout From Permutation results ############  
    z = 0
    while z < len(permutation_result):
        if len(permutation_result[z]['Final path']) != int(sim_setting['num_destination']) * int(sim_setting['n_multicast_group']):
            permutation_result[z]['Final cost'] = 'infinite'
        z = z + 1
        
    min_result = min(permutation_result, key=lambda x:x['Final cost'])
    
    ############ Print Result ############
    # z = print("\nHeuristic Path:\n",min_result)
    fin_cost = min_result['Final cost']
    fin_path = min_result['Final path']
    if min_result['Final cost'] == 'infinite':
        x = print("No feasbile solution found! Try again")
        optimal = False
    else:
        print("Heuristic Minimum Cost: ", fin_cost)
        print("Heuristic Computation Time: ", round(computation_time,4),'seconds')
        optimal = True
    return fin_cost,fin_path,optimal



