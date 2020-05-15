import random
import itertools
import pandas as pd


def exp_tree(ed, v, pesos=None):
    end = False
    blue = []
    orange = []
    buckets = []

    results = []

    for edge in ed:
        if edge.split('-')[0] == edge.split('-')[1]:
            ed.pop(edge.index(edge))

    edge0 = random.choice(ed)
    edge_ = ed
    if pesos is not None:
        edge_ = [x for x, y in sorted(zip(ed, pesos), key=lambda x: x[1])]
        edge0 = edge_[0]
    blue.append(edge0)
    edge_.pop(edge_.index(edge0))
    buckets.append([edge0.split('-')[0], edge0.split('-')[1]])
    bu = buckets.copy()
    results.append([0, [edge0], [], bu])

    i = 0

    while not end:
        v1b = None
        v2b = None

        i = i + 1
        if pesos is None:
            edge_random = random.choice(edge_)
        else:
            edge_random = edge_[0]
        v1 = edge_random.split('-')[0]
        v2 = edge_random.split('-')[1]

        for bucket in buckets:
            if v1 in bucket: v1b = buckets.index(bucket)
            if v2 in bucket: v2b = buckets.index(bucket)
            if (v1b is not None) and (v2b is not None):
                break

        if (v1b == v2b) and (v1b is not None):
            orange.append(edge_random)
            edge_.pop(edge_.index(edge_random))
            results_ = [i, blue[:], orange[:], bu]


        elif (v1b is None) and (v2b is None):
            blue.append(edge_random)
            edge_.pop(edge_.index(edge_random))
            bu = buckets.copy()
            bu.append([v1, v2])
            results_ = [i, blue[:], orange[:], bu]
            buckets.append([v1, v2])


        elif v1b != v2b:
            if v1b is None:
                blue.append(edge_random)
                edge_.pop(edge_.index(edge_random))
                bu = buckets.copy()
                results_ = [i, blue[:], orange[:], bu[:]]
                buckets[v2b].append(v1)


            elif v2b is None:
                blue.append(edge_random)
                edge_.pop(edge_.index(edge_random))
                bu = buckets.copy()
                results_ = [i, blue[:], orange[:], bu[:]]
                buckets[v1b].append(v2)
            else:
                blue.append(edge_random)
                edge_.pop(edge_.index(edge_random))
                bu = buckets.copy()
                bu[v1b] = bu[v1b] + bu[v2b]
                bu.pop(bu.index(bu[v2b]))
                results_ = [i, blue[:], orange[:], bu[:]]
                buckets[v1b] = buckets[v1b] + buckets[v2b]
                buckets.pop(buckets.index(buckets[v2b]))

        results.append(results_.copy())

        if (len(buckets) == 1) and (sorted(list(itertools.chain.from_iterable(buckets))) == sorted(v)):
            end = True

    coste = 0

    results_df = pd.DataFrame(results, columns=["Iter", "Blue", "Orange", "Buckets"])

    print(results_df.to_string(index=False))
    if pesos is not None:
        for i in blue:
            coste = coste + pesos[ed.index(i)]
        print(f'\n El coste total es {coste}')