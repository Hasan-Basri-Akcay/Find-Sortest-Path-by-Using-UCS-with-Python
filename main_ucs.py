import csv
from queue import PriorityQueue

import pandas as pd
import numpy as np


class CityNotFoundError(Exception):
    def __init__(self, city):
        print("%s does not exist" % city)
        

class Graph:
    def __init__(self):
        self.edges = {}
        self.weights = {}

    def get_neighbors(self, node):
        return self.edges[node]

    def get_cost(self, from_node, to_node):
        return self.weights[(from_node + to_node)]
    
    def set_neighbors(self, node, neighbors):
        self.edges[node] = neighbors
        
    def set_cost(self, from_node, to_node, cost):
        self.weights[(from_node + to_node)] = cost


# Implement this function to read data into an appropriate data structure.
def build_graph(path):
    cities1 = path['city1'].unique()
    cities2 = path['city2'].unique()
    
    cities = list(list(set(cities1)-set(cities2)) + list(set(cities2)))
    print('cities: ', cities)
    
    city_graph = Graph()
    
    for city in cities:
        city1_pd = path[path['city1'] == city]
        city2_pd = path[path['city2'] == city]
        
        neighbors1 = city1_pd['city2'].values
        neighbors2 = city2_pd['city1'].values
        distances1 = city1_pd['distance'].values
        distances2 = city2_pd['distance'].values
        
        neighbors = np.concatenate((neighbors1, neighbors2), axis=0)
        distances = np.concatenate((distances1, distances2), axis=0)
        
        distances_sort_index = np.argsort(distances)
        
        distances = distances[distances_sort_index]
        neighbors = neighbors[distances_sort_index]
        
        neighbors_lower = [x.lower() for x in neighbors]
        
        city_graph.set_neighbors(city.lower(), neighbors_lower)
        
        for i in range(len(distances)):
            city_graph.set_cost(city.lower(), neighbors_lower[i], distances[i])
    
    return city_graph


# Implement this function to perform uniform cost search on the graph.
def uniform_cost_search(graph, start, end):
    visited = set()
    queue = PriorityQueue()
    queue.put((0, start))
    cost_dict = {}
    cost_dict[0] = [start]
    
    while not queue.empty():
        cost, node = queue.get()
        if node not in visited:
            visited.add(node)

            if node == end:
                return cost_dict[cost], cost
            
            for i in graph.get_neighbors(node):
                if i not in visited:
                    total_cost = cost + graph.get_cost(node, i)
                    
                    keys_list = cost_dict.keys()
                    
                    if total_cost in keys_list:
                        total_cost = total_cost + np.random.rand() / 100000
                        
                        queue.put((total_cost, i))
                    
                        temp = cost_dict.get(cost).copy()
                        temp.append(i)
                        
                        cost_dict[total_cost] = temp
                    else:
                        queue.put((total_cost, i))
                    
                        temp = cost_dict.get(cost).copy()
                        temp.append(i)
                        
                        cost_dict[total_cost] = temp
    
    print('Result cannot be found.')
    

def print_way_list(graph, way_list, cost, start, end):
    print('...')
    print('Start: ', start, ' - End:', end)
    for i in range(len(way_list) - 1):
        print(way_list[i] + ' --> ' + str(graph.get_cost(way_list[i], way_list[i+1])) + ' --> ' , end =" ")
    print(way_list[-1])
    print('total cost: ', round(cost, 2))
    print('...')


# Implement main to call functions with appropriate try-except blocks
if __name__ == "__main__":   
    print('---/---')
    print('Press q for exit.')
    while True:
        print('Write the file path', end=' ')
        csv_path = input()
        print('---')
        
        if csv_path == 'q':
            print('System Exit.')
            break
        
        try:
            road_pd = pd.read_csv(csv_path)
        except:
            print('FileNotFoundError')
            print('---')
            continue
        
        print('---')
        try:
            graph = build_graph(road_pd)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
                print('Please Check Your File.')
                print('---')
                continue
            else:
                print(e)
                print('Please Check Your File.')
                print('---')
                continue
        print('---')
        
        print('Start: ', end=' ')
        start = input()
        
        if start == 'q':
            print('System Exit.')
            break
        
        print('end: ', end=' ')
        end = input()
        
        if end == 'q':
            print('System Exit.')
            break
        
        try:
            way_list, cost = uniform_cost_search(graph, start.lower(), end.lower())

            print_way_list(graph, way_list, cost, start, end)
        except:
            print('CityNotFoundError')
            print('---')
            continue
        
    print('---/---')
        
