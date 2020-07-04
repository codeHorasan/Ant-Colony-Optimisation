#@author: UgurHorasan

import random as rn

class Edge():
    def __init__(self,s,t,weight):
        self.s = s
        self.t = t
        self.weight = weight
        self.phe = 1

    def return_weight(self):
        return self.weight

    def __str__(self):
        return "{} - {} = {}, phe = {}".format(self.s, self.t,self.weight,self.phe)

class Node():
    def __init__(self,name):
        self.name = name
        self.neighbors = []

class Graph():
    def __init__(self,edge_list):
        self.edge_list = edge_list
        self.list_of_edges = []
        self.create_nodes()
        self.create_graph()
    def create_nodes(self):
        self.node_names = list(set([s for s,t,d in self.edge_list] + [t for s,t,d in self.edge_list]))
        self.nodes = {n : Node(n) for n in self.node_names}
    def create_graph(self):
        for s,t,d in self.edge_list:
            e = Edge(s,t,d)
            self.list_of_edges.append(e)
            self.add_edges(e)
    def add_edges(self,edge):
        self.nodes[edge.s].neighbors.append(edge)
    def show_info(self):
        for edge in self.list_of_edges:
            print(edge)

#edge_list = (['A','B',5],['A','C',9],['B','D',1],['C','D',13])
edge_list = (['A','B',14],['A','C',5],['A','D',7],['B','F',4],['B','C',3],['C','B',3],['D','E',6],['C','D',4],['D','C',4],['E','C',5],['C','E',5],['C','F',10],['E','F',7])
graph = Graph(edge_list)
graph.show_info()
print("*********************************************************")

class Ant():
    def __init__(self,graph,alpha,beta,delta = 1,start = 'A',end = 'D'):
        self.graph = graph
        self.alpha = alpha
        self.beta = beta
        self.delta = delta
        self.route = []
        self.current_node = graph.nodes[start]
        self.final_node = graph.nodes[end]
        self.total_distance = 0
        self.edge_list = self.graph.list_of_edges
        self.route.append(self.current_node.name)

    def move(self):
        self.possible_path = {edge.t : (edge.weight,edge.phe)  for edge in self.edge_list if edge.s is self.current_node.name if edge.t not in self.route}
        self.sum_of_possibilities = 0
        self.list_for_sum = [t for n,t in self.possible_path.items()]
        for weight,phe in self.list_for_sum:
            self.sum_of_possibilities += (phe**self.alpha) / (weight**self.beta)
        self.possibilities = {x : (z**self.alpha / y**self.beta) / self.sum_of_possibilities for x,(y,z) in self.possible_path.items()}
        self.selected_path = rn.choices(list(self.possibilities.keys()),self.possibilities.values(), k=1)[0]
        self.route.append(self.selected_path)
        self.current_node = self.graph.nodes[self.selected_path]

    def go_to_target(self):
        while self.current_node != self.final_node:
            self.move()
            n1,n2 = self.route[-1],self.route[-2]
            dis = [edge.return_weight() for edge in self.graph.list_of_edges if edge.s == n2 and edge.t == n1]
            self.total_distance += dis[0]

    def deposit(self):
        edges_of_route = []
        for i in range(len(self.route)-1):
            edge = ((self.route[i],self.route[i+1]))
            edges_of_route.append(edge)
        my_list = [edge for edge in edges_of_route]
        for e in self.graph.list_of_edges:
            for i in range(len(my_list)):
                if e.s == my_list[i][0] and e.t == my_list[i][1]:
                    e.phe += self.delta/self.total_distance


class AntColony():
    def __init__(self,graph,alpha,beta,nest_size,iteration,delta=1,start = 'A',end = 'D'):
        self.graph = graph
        self.alpha = alpha
        self.beta = beta
        self.delta = delta
        self.start = start
        self.end = end
        self.nest_size = nest_size
        self.iteration = iteration
        self.apply_ACO()

    def evaporate(self,decay = 0.05):
        for edge in self.graph.list_of_edges:
            edge.phe *= (1-decay)

    def apply_ACO(self):
        list_of_ants = [Ant(self.graph,self.alpha,self.beta,delta = self.delta,start = self.start, end = self.end) for i in range(self.nest_size)]
        self.last_routes = []
        self.best_route = []
        for ite in range(self.iteration):
            for ant in list_of_ants:
                ant.go_to_target()
                if ite == self.iteration-1:
                    self.last_routes.append(ant.route)
            for ants in list_of_ants:
                ants.deposit()
            self.evaporate()
            list_of_ants = [Ant(self.graph, self.alpha, self.beta, delta=self.delta, start=self.start, end=self.end) for i in range(self.nest_size)]

        for elm in self.last_routes:
            print(elm)


#colony = AntColony(graph,1,1,30,200,delta=1,start='A',end='D')
colony = AntColony(graph,1,1,30,100,delta=1,start='A',end='F')
graph.show_info()

