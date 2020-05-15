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

    vertex = ['a', 'b', 'c', 'd', 'e']

    edges = ['a-b','a-c', 'a-d', 'a-e', 'b-c', 'b-d', 'b-e', 'c-d', 'c-e', 'd-e']
    pesos = [5, 50, 80, 90, 70, 60, 50, 8, 20, 10]

    g1 = Graph(vertex, edges)
    g1.expansion_tree(pesos)
