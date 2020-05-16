import random
from collections import Counter
def max_ram(edges, vertex, weights):
    reduced = True
    v = vertex
    e = edges
    w = weights
    v_f = []
    e_f = []
    w_f = []
    v_f.append([item for item in vertex])
    e_f.append([item for item in edges])
    w_f.append([item for item in weights])
    i=0
    circ = []
    repl = []
    while reduced == True:
        v,e, w, reduced, next, replaced = reduce_cicles(v,e, w, i)
        if reduced == True:
            v_f.append([item for item in v])
            e_f.append([item for item in e])
            w_f.append([item for item in w])
            circ.append([item for item in next])
            repl.append([item for item in replaced])
            i=i+1

    v, e, w, i = choose_edges(v, e, w, i)
    v_f.append([item for item in v])
    e_f.append([item for item in e])
    w_f.append([item for item in w])

    ext_e, ext_w = extend_graph(e_f[-1], w_f[-1],repl,circ,e_f[0], w_f[0],i)

    print(f'Ramificación máxima: {ext_e}')
    print(f' Coste: {sum(ext_w)}')

def extend_graph(e_f,w_f,replaced,circ,e_o,w_o, i):

    extended = []
    w_ext = []
    for j in range(i+1):
        for e in e_f:
            if f'v_' not in e:
                extended.append(e)
                w_ext.append(w_f[e_f.index(e)])
            elif f'v_{j}' == e.split('-')[1]:
                added = []
                for r in replaced[j]:
                    if r in added: continue
                    try:
                        extended.append(e_o[e_o.index(e.replace(f'v_{j}', r ))])
                        w_ext.append(w_o[e_o.index(e.replace(f'v_{j}', r ))])
                        for item in circ[j]:
                            if item.split('-')[1] == r:
                                continue
                            else:
                                extended.append(item)
                                w_ext.append(w_o[e_o.index(item)])
                        added.append(r)
                    except:
                        continue
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
    reduced = False
    cir = []
    e_or = e.copy()
    v_or = v.copy()
    w_or = w.copy()
    replaced = []
    for e_ in e:
        first = e_.split('-')[0]
        next = [e_]
        we = [w[e.index(e_)]]
        v_circuit = [e_.split('-')[0], e_.split('-')[1]]
        for ed in e:
            if ed.split('-')[0]!= next[-1].split('-')[1]:
                continue
            else:
                next.append(ed)
                v_circuit.append(ed.split('-')[1])
                we.append(w[e.index(ed)])
                if next[-1].split('-')[1] == first:
                    v_circuit.pop(-1)
                    print(f'circuit found {next}')
                    cir = [item for item in next]
                    print(f'Circuit vertex {v_circuit}')
                    min_w = min(we)
                    for item in next:
                        w.pop(e.index(item))
                        e.pop(e.index(item))

                    for ver in v_circuit:
                        v.pop(v.index(ver))
                    new_e = []
                    replaced = []
                    for j in e:
                        if (j.split('-')[0] in v_circuit):
                            new_e.append(j.replace(j.split('-')[0], f'v_{i}'))
                            replaced.append(j.split('-')[0])
                        elif (j.split('-')[1] in v_circuit):
                            new_e.append(j.replace(j.split('-')[1], f'v_{i}'))
                            replaced.append(j.split('-')[1])
                        else:
                            new_e.append(j)
                            replaced.append('')
                    v.append(f'v_{i}')
                    new_w = []
                    for k in range(len(replaced)):
                        if replaced[k] == '':
                            new_w.append(w[k])
                        else:
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

