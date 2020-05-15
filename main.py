'''
Graphs definition and main algorithms implementation
Expansion Tree
Expansion Tree at minimium cost
'''


if __name__ == '__main__':
    '''
    Create graph gith Graph([vertex], [edges])
    '''
    from methods.graphs import Graph

    vertex = ['a', 'b', 'c', 'd', 'e', 'f']

    edges = ['f-e', 'f-a', 'b-d', 'f-d', 'e-a', 'd-a', 'a-c', 'c-b']
    pesos = [1, 0, 2, 1, 2, 3, 3, 2]

    g1 = Graph(vertex, edges)
    g1.maximum_ramification(pesos)
