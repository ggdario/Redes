import random
import itertools
import pandas as pd


def exp_tree(ed, v, pesos=None):
    '''
    This functions looks for the best way to connect all vertex (at minimum cost if weights is given)
    Parameters
    ----------
    ed: list(str)
        list containing graph edges
    v: list(str)
        list containing graph vertex
    pesos: list(str) (optional)
        list containing weights for each vertex

    Returns
    -------

    '''
    end = False
    blue = []
    orange = []
    buckets = []

    results = []

    # Edges that begin and end in the same vertex are eliminated
    for edge in ed:
        if edge.split('-')[0] == edge.split('-')[1]:
            ed.pop(edge.index(edge))

    # If weights are not given, first edge is chosen randomly
    edge0 = random.choice(ed)
    edge_ = ed

    #If weights are given, firs edge is the 'minimum cost' one
    if pesos is not None:
        edge_ = [x for x, y in sorted(zip(ed, pesos), key=lambda x: x[1])]
        edge0 = edge_[0]

    # First edge is always included in the final expansion tree, so it is added to blue list. Its vertex are
    # added to a bucket. since this edge has benn analyzed, it is removed from edge list.
    blue.append(edge0)
    edge_.pop(edge_.index(edge0))
    buckets.append([edge0.split('-')[0], edge0.split('-')[1]])
    bu = buckets.copy()
    results.append([0, [edge0], [], bu])

    i = 0

    while not end:
        v1b = None
        v2b = None

        # If weights are not given, next edge is chosen randomly and if weights is given, next edge will be the
        # one with lower cost
        i = i + 1
        if pesos is None:
            edge_random = random.choice(edge_)
        else:
            edge_random = edge_[0]

        # Vertex of the chosen edge are separated
        v1 = edge_random.split('-')[0]
        v2 = edge_random.split('-')[1]

        # For each vertex, it is seen which bucket it corresponds to. (Maybe they ddo not belong to a bucket)
        for bucket in buckets:
            if v1 in bucket: v1b = buckets.index(bucket)
            if v2 in bucket: v2b = buckets.index(bucket)
            if (v1b is not None) and (v2b is not None):
                break

        # If both vertex are in the same bucket, this edge do not belong to the final expansion tree.
        if (v1b == v2b) and (v1b is not None):
            orange.append(edge_random)
            edge_.pop(edge_.index(edge_random))
            results_ = [i, blue[:], orange[:], bu]

        #If both vertex do not belong to a bucket, the edge belongs to final tree and both vertex are placed in a new
        # bucket
        elif (v1b is None) and (v2b is None):
            blue.append(edge_random)
            edge_.pop(edge_.index(edge_random))
            bu = buckets.copy()
            bu.append([v1, v2])
            results_ = [i, blue[:], orange[:], bu]
            buckets.append([v1, v2])



        elif v1b != v2b:
            # If one vertex belongs to a bucket and the other is not in any bucket, this last vertex is added to the
            # same bucket as the other and the edge belongs to the final graph (blue)
            if v1b is None:
                blue.append(edge_random)
                edge_.pop(edge_.index(edge_random))
                bu = buckets.copy()
                results_ = [i, blue[:], orange[:], bu[:]]
                buckets[v2b].append(v1)


            # The same thing happens here
            elif v2b is None:
                blue.append(edge_random)
                edge_.pop(edge_.index(edge_random))
                bu = buckets.copy()
                results_ = [i, blue[:], orange[:], bu[:]]
                buckets[v1b].append(v2)

            # If each vertex belongs to different buckets, edge belongs to final silution (blue) and both buckets
            # are merged
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

        # If there is just one bucket containing all vertex, the algorithm ends
        if (len(buckets) == 1) and (sorted(list(itertools.chain.from_iterable(buckets))) == sorted(v)):
            end = True

    coste = 0

    results_df = pd.DataFrame(results, columns=["Iter", "Blue", "Orange", "Buckets"])

    print(results_df.to_string(index=False))

    # Final cost is calculated by the sum of all the edges belonging to the final solution
    if pesos is not None:
        for i in blue:
            coste = coste + pesos[ed.index(i)]
        print(f'\n El coste total es {coste}')