import numpy as np
from graphviz import Digraph
import pydotplus
import re
import copy
import networkx as nx

def remove_end(matr):
    start = []
    finish = []
    for elem in matr:
        if elem[0] == 'start':
            start.append(str(elem[1]))
        if elem[1] == 'finish':
            finish.append(str(elem[0]))

    matr = list(filter(lambda x: x[0] != 'start' and x[1] != 'finish', matr))
    return matr, start, finish

def draw_and_transform(clean_matr):
    g = Digraph(comment='FromMatrix')
    for elem in clean_matr:
        g.node(str(elem[0]))
        g.edge(str(elem[0]), str(elem[1]), label=elem[2])
    g.graph_attr['rankdir'] = 'LR'  
    #display(g)
    return g

def graph_to_network(g):
    dotplus = pydotplus.graph_from_dot_data(g.source)
    return nx.nx_pydot.from_pydot(dotplus)

def get_paths(graph, start, end, path, visits):
    if start == end:
        if start in visits.keys():
            visits[start] += 1
            if visits[start] > 1:
                path.append(start)
                return [path]
        else:
            visits[start] = 1
        path.append(start)
        if list(nx.neighbors(graph, start)) == []:
            return [path]
        else:
            neighbors = list(nx.neighbors(graph, start))
            paths = [path]
            for neighbor in neighbors:
                paths += get_paths(graph, neighbor, end, copy.copy(path), copy.copy(visits))
            return paths
    if start in visits.keys():
        visits[start] += 1
        if visits[start] > 2:
            path.append(start)
            return []
    else:
        visits[start] = 1
    path.append(start)
    neighbors = list(nx.neighbors(graph, start))
    paths = []
    for neighbor in neighbors:
        paths += get_paths(graph, neighbor, end, copy.copy(path), copy.copy(visits))
    return paths

def find_kernels(matr1, start1, finish1):
    graph1 = draw_and_transform(matr1)
    graph = graph1
    start = start1
    end = finish1
    nx_graph = graph_to_network(graph)
    paths = []
    for s in start:
        for e in end:
            paths +=  get_paths(nx_graph, s, e, [], {})
    labels = nx.get_edge_attributes(nx_graph, "label")
    kernels = []
    for path in paths:
        kernel = []
        for i in range(len(path)-1):
            kernel.append(labels[(path[i], path[i+1], 0)])
        kernels.append(kernel)
    return list(map(lambda x: list(map(lambda y: re.sub(r'\"',"",y), x)), kernels))

def check_correct_path(kernel):
    for path in kernel:
        word = ""
        for elem in path:
            word += elem
            word = re.sub(r'[^()\d]+', '', word)
        if check_brackets(split_word(word)):
            return True
    return False
    
def split_word(word):
    if word == "":
        return []
    res = []
    tmp = word[0]
    for letter in word[1:]:
        if letter == '(' or letter == ')':
            res.append(tmp)
            tmp = letter
        else:
            tmp += letter
    res.append(tmp)
    return res

def check_brackets(brackets):
    if brackets == []:
        return True
    tmp = len(brackets)
    for index, bracket in enumerate(brackets[1:]):
        if brackets[0] == '(' and ')'+brackets[0][1:] == bracket:
            brackets.pop(index)
            break
    if len(brackets) == tmp:
        return False
    brackets.pop(0)
    return check_brackets(brackets)

def find_correct_path(res):
    matr1, start1, finish1 = remove_end(res)
    kernels1 = find_kernels(matr1, start1, finish1)
    correct_paths = []
    for kernel in kernels1:
        if check_correct_path([kernel]):
            correct_paths.append(kernel)
    return correct_paths


def check_path_in_graph(matr, start, end, path, kernels):
    path.append(start)
    if kernels == []:
        if start == end:
            return True
        else:
            return False
    res = []
    for elem in matr:
        if elem[2].find(kernels[0].split()[0]) >= 0 and start == elem[0]:
            res.append(check_path_in_graph(matr, elem[1], end, copy.copy(path), kernels[1:]))
    if True in res:
        return True
    return False

def check_all_paths_in_graph(matr, start, end, kernels):
    res = []
    if kernels == []:
        k = 0
        for s in start:
            for e in end:
                if check_path_in_graph(matr, s, e, [], kernels):
                    res.append(True)
                    k = 1
        if k == 0:
            res.append(False)
    else:
        for kernel in kernels:
            k = 0
            for s in start:
                for e in end:
                    if check_path_in_graph(matr, s, e, [], kernel):
                        res.append(True)
                        k = 1
            if k == 0:
                res.append(False)
    if False in res:
        return False
    return True

def check_eq(res1, res2):
    matr1, start1, finish1 = remove_end(res1)
    kernel1 = find_correct_path(res1) 
    matr2, start2, finish2 = remove_end(res2)
    kernel2 = find_correct_path(res2) 
    if not check_all_paths_in_graph(matr1, start1, finish1, kernel2):
        return False
    if not check_all_paths_in_graph(matr2, start2, finish2, kernel1):
        return False
    return True
