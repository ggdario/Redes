'''
Author: Darío Garcia
Graphs definition and main algorithms implementation
Expansion Tree
Expansion Tree at minimium cost
Maximum ramification
'''


if __name__ == '__main__':

    #Create graph with Graph([vertex], [edges])
    from methods.graphs import Graph

    vertex = ['a', 'b', 'c', 'd', 'e', 'f']

    #Edges are considered directed (just for methods which require it
    edges = ['f-e', 'f-a', 'b-d', 'f-d', 'e-a', 'd-a', 'a-c', 'c-b']
    pesos = [1, 0, 2, 1, 2, 3, 3, 2]

    #Graph definition and analysis
    g1 = Graph(vertex, edges)
    g1.maximum_ramification(pesos)
