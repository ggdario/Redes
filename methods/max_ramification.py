import random
from collections import Counter
def max_ram(edges, vertex, weights):
    '''
    This function gets the maximum ramification from a given graph.
    First of all, all circuits must be reduced to weights and weights mus tbe recalculated.
    After calculating maximum graph without cycles, reduced circuits must be regenrated to ger the final
    solution.

    Parameters
    ----------
    edges: list(str)
        list containing all graph edgex (vertex1-vertex2)
    vertex: list(str)
        list containing all verex as string
    weights: list(float)
        list containing each edge weights/cost

    Returns
    -------

    '''
    reduced = True
    v = vertex
    e = edges
    w = weights
    v_f = []
    e_f = []
    w_f = []

    # Initial vertex, edges and weights are appended to the final solution so steps can be followed.
    v_f.append([item for item in vertex])
    e_f.append([item for item in edges])
    w_f.append([item for item in weights])
    i=0
    circ = []
    repl = []

    # If there are circuits, they are transformed to vertex, recalculating weights as it is explained in
    # the corresponding function documentation.
    while reduced == True:
        v,e, w, reduced, next, replaced = reduce_cicles(v,e, w, i)

        # It a circuit is reduced to a vertex, new graph is appended to the solution list.
        # The circuit that has been reduced is appended to 'circ', and vertex involved in the circuit are
        # appended to 'repl'
        if reduced == True:
            v_f.append([item for item in v])
            e_f.append([item for item in e])
            w_f.append([item for item in w])
            circ.append([item for item in next])
            repl.append([item for item in replaced])
            i=i+1

    # For the graph with no circuits, maximum cost incident edge is selected for each vertex in 'chose_edges' function
    v, e, w, i = choose_edges(v, e, w, i)

    # Graph containing maximum weight edges is appended to the final solution

    v_f.append([item for item in v])
    e_f.append([item for item in e])
    w_f.append([item for item in w])

    # Reduced circuits are extended again to obtain final solution
    ext_e, ext_w = extend_graph(e_f[-1], w_f[-1],repl,circ,e_f[0], w_f[0],i)

    print(f'Ramificación máxima: {ext_e}')
    print(f' Coste: {sum(ext_w)}')

def extend_graph(e_f,w_f,replaced,circ,e_o,w_o, i):
    '''
    This function gets a graph with some circuits reduced to vertex and it expands te graph considering maximum costs
    and avoiding new circuits genration.
    Parameters
    ----------
    e_f: list(str)
        list containing graph with no circuit edges
    w_f: list(str)
        weights of the reduced graph
    replaced: list(str)
        vertex that were part of the reduced circuits
    circ: list(str)
        reduced circuits
    e_o: list(str)
        original graph edges
    w_o: list(str)
        original graph weigths
    i: int
        number of circuits, circuits = i+1 since it is 0-ondexed

    Returns
    -------

    '''

    extended = []
    w_ext = []

    # For each circuit (i circuits), it is expanded
    for j in range(i+1):

        # If an edge is conected to a circuit, one of the vertex is 'v_i' named
        for e in e_f:

            # If there is not v_ in the edge vertex, it is the same as the original one so it is appended to final
            # solution and it is weight is looked to be appended in the final solution
            if f'v_' not in e:
                extended.append(e)
                w_ext.append(w_f[e_f.index(e)])

            # If v_i is the final vertex of an edge, its corresponding cicruit must be generated except final edge
            # to avoid getting a new circuit. If a-b, b-c, c-a was the initial circuit, only a-b and b-c will be
            # appende

            elif f'v_{j}' == e.split('-')[1]:
                added = []
                for r in replaced[j]:
                    if r in added: continue

                    # v_i is replaced by its original vertex and these new edge is appended to the solution
                    try:
                        extended.append(e_o[e_o.index(e.replace(f'v_{j}', r ))])
                        w_ext.append(w_o[e_o.index(e.replace(f'v_{j}', r ))])

                        # If and edge of the circuits ends in v_i, it is not appended to avoid new circuits
                        for item in circ[j]:
                            if item.split('-')[1] == r:
                                continue
                            else:
                                extended.append(item)
                                w_ext.append(w_o[e_o.index(item)])
                        added.append(r)
                    except:
                        continue

            # If the reduced vertex is a root, its circuit is generated except the vertex with minimum cost
            elif f'v_{j}' == e.split('-')[0]:
                w_c = []
                for item in circ[j]:
                    w_c.append(w_o[e_o.index(item)])
                w_m = min(w_c)
                w_c_2 = []
                for item in circ[j]:
                    if (w_o[e_o.index(item)]>=w_m) and (len(w_c_2)< len(circ[j])):
                        extended.append(item)
                        w_ext.append(w_o[e_o.index(item)])
    return extended, w_ext

def reduce_cicles(v, e, w, i=0):
    '''

    Parameters
    ----------
    v: list(str)
        list containing graph vertex
    e: list(str)
        list containing graph edges
    w: list(float)
        list containing edges weights
    i: int
        circuits reduces previously

    Returns
    -------

    '''
    reduced = False
    cir = []
    e_or = e.copy()
    v_or = v.copy()
    w_or = w.copy()
    replaced = []

    # For each edge, it is looked for an edge that starts where the first one ends
    for e_ in e:
        first = e_.split('-')[0]
        next = [e_]
        we = [w[e.index(e_)]]
        v_circuit = [e_.split('-')[0], e_.split('-')[1]]
        for ed in e:
            # if an edge does not start where the preivous ends, nothing happend
            if ed.split('-')[0]!= next[-1].split('-')[1]:
                continue
            else:
                next.append(ed)
                v_circuit.append(ed.split('-')[1])
                we.append(w[e.index(ed)])
                # If and edge ends where the first edge begins, a circuit has been found
                if next[-1].split('-')[1] == first:
                    v_circuit.pop(-1)
                    print(f'circuit found {next}')
                    cir = [item for item in next]
                    print(f'Circuit vertex {v_circuit}')
                    # Lower cost of the circuit is needed later
                    min_w = min(we)
                    for item in next:
                        #Each edge, vertex and weight of the circuit is removed from the graph
                        w.pop(e.index(item))
                        e.pop(e.index(item))

                    for ver in v_circuit:
                        v.pop(v.index(ver))
                    new_e = []
                    replaced = []

                    # All edges which only one vertex belonging to the circuit are renamed. The vertex
                    # belonging to the circuit are renamed as v_i
                    for j in e:
                        if (j.split('-')[0] in v_circuit):
                            new_e.append(j.replace(j.split('-')[0], f'v_{i}'))
                            replaced.append(j.split('-')[0])
                        elif (j.split('-')[1] in v_circuit):
                            new_e.append(j.replace(j.split('-')[1], f'v_{i}'))
                            replaced.append(j.split('-')[1])
                        else:
                            # If an edge do not have vertex in the circuit, they are appended with no changes
                            new_e.append(j)
                            replaced.append('')
                    v.append(f'v_{i}')
                    new_w = []

                    # Replaced vertex are appended to a new list
                    for k in range(len(replaced)):
                        if replaced[k] == '':
                            new_w.append(w[k])
                        else:
                            # Weights for edges directed to the circuit are recalculated
                            w_cir = list(filter(lambda x: x.split('-')[1] == replaced[k], next))[0]
                            ori = new_e[k].replace(f'v_{i}', replaced[k])
                            new_w.append(w_or[e_or.index(ori)] + min_w + -w_or[e_or.index(w_cir)])
                    print(f'New vertex {v}')
                    print(f'New edges {new_e}')
                    print(f'New weights {new_w}')
                    reduced = True

                else:
                    continue
    if reduced == False:
        new_e = e
        new_w = w
    return v, new_e, new_w, reduced, cir, replaced


def choose_edges(v, e, w, i_):
    entradas = []
    pesos = []
    e_final = []
    w_final = []
    for i in range(i_):
        for m in e:
            if m.split('-')[1] == f'v_{i}':
                entradas.append(m)
                pesos.append(w[e.index(m)])

        max_w = max(pesos)
        for n in e:
            if (n not in e_final) and (f'v_{i}' not in n):
                e_final.append(n)
                w_final.append(w[e.index(n)])
            elif (n not in e_final) and (f'v_{i}' in n):
                if w[e.index(n)] == max_w:
                    e_final.append(n)
                    w_final.append(w[e.index(n)])

    return v, e_final, w_final, i

