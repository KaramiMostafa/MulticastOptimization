import numpy as np
import json
import networkx as nx
import random
import matplotlib.pyplot as plt

fp = open("./etc/config.json", 'r')

sim_setting = json.load(fp)
# print(sim_setting)


class Graph_Generation(object):
    def __init__(self, g):
        self.g = g

        pass

    def Node_Generator(self):
        # self.g = nx.Graph()
        for i in (range(sim_setting["total_node"])):
            nodes = self.g.add_node(i)

        # nodes positioned in a random spring layout and
        # the corresponding positiones are extracted
        self.node_pos = nx.spring_layout(self.g)
        for i in range(self.g.order()):
            x, y = self.node_pos[i]
            self.g.nodes[i]['pos'] = (x, y)
        # print(self.node_pos)

    # random edge generation
    def Edge_Generator(self):
        for j in (range(sim_setting["total_node"])):
            # while (len(self.g.in_edges(j)) and len(self.g.out_edges(j))) <= 1:
            while (self.g.degree(j) <= 1):
                c1 = np.random.choice(self.g.nodes())
                c2 = np.random.choice(self.g.nodes())
                if c1 != c2 and self.g.has_edge(c1, c2) == 0:
                    self.g.add_edge(c1, c2)

    # graph matrix generation

    def Real_Matrix(self):
        # np.random.seed(0)
        self.costs = []
        for i in range(self.g.size()):
            self.costs.append(random.randint(
                sim_setting['min_cost'],
                sim_setting['max_cost'],))
        nodes_matrix_size = (self.g.order(), self.g.order())
        self.nodes_matrix = np.zeros(nodes_matrix_size)
        for i in range(self.g.order()):
            for j in range(self.g.order()):
                if self.g.has_edge(i, j):
                    self.nodes_matrix[i][j] = 1
        self.nodes_matrix_triu = np.triu(self.nodes_matrix, k=0)
        # return self.nodes_matrix
        # print(nodes_matrix_triu)

    # random cost assignment to the edges
    def Cost_Assignment(self):
        t = 0
        for i in range(self.g.order()):
            for j in range(self.g.order()):
                if self.nodes_matrix_triu[i][j] == 1:
                    self.g.edges[i, j]['weight'] = self.costs[t]
                    self.nodes_matrix[i][j] = self.costs[t]
                    t += 1
        for i in range(self.g.order()):
            for j in range(self.g.order()):
                self.nodes_matrix[j][i] = self.nodes_matrix[i][j]
        return self.nodes_matrix

    # raw graph plot
    def plot(self):
        arc_weight = nx.get_edge_attributes(self.g, 'weight')
        nx.draw_networkx_nodes(self.g, pos=self.node_pos,
                               node_color='yellow')  # draw nodes
        nx.draw_networkx_labels(self.g, pos=self.node_pos)  # label nodes
        nx.draw_networkx_edges(self.g, pos=self.node_pos,
                               edge_color='red', style='dotted')  # draw edges
        nx.draw_networkx_edge_labels(
            self.g, pos=self.node_pos, edge_labels=arc_weight)  # label edges
        plt.show()

        # if nx.is_connected(self.g):
        #     print("connected")
        # else:
        #     print("not connected")
