import random
from collections import Counter
def max_ram(edges, vertex, weights):
    reduced = True
    i=0
    while reduced == True:
        vertex,edges, weights, reduced = reduce_cicles(vertex,edges, weights, i)
        i=i+1

    aa=0


def reduce_cicles(v, e, w, i=0):
    reduced = False
    e_or = e.copy()
    v_or = v.copy()
    w_or = w.copy()
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
    return v, new_e, new_w, reduced


def step1(g, a, v, weights):
    pass


def step2(g,a,v, weights, i):

    pass
def step3():
    pass