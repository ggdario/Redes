
def fp(vertex, edges, inicio, final):
    e = edges
    ini = inicio
    end = final
    found = False
    paths = pos_path(e,ini,end, found )

    if paths == []:
        return

    # Starting at the beginning, all possible paths are calculated to reach the end
    result = final_path(paths, final)

    result.reverse()

    print(f'Final path is: {result}')

    aa = 0
def pos_path(edges, inicio, final, found):
    used = []
    i_ = [inicio]
    path = []


    #Loop is eprformed until final node is reached
    while not found:
        exists = False
        pos_e = []
        pos_v = []
        e_remove = []
        for ed in edges:
            # For each edge, it is checked if it continues the existing path.
            # If both vertex have been already used, the edge is removed
            if (ed.split('-')[1] in used) and (ed.split('-')[0] in used):
                e_remove.append(ed)
                continue
            elif ed.split('-')[0] not in i_[-1]:
                continue
            else:
                if ed.split('-')[1] in used:
                    continue
                else:
                    used.append(ed.split('-')[1])
                    pos_e.append(ed)
                    pos_v.append(ed.split('-')[1])
                    e_remove.append(ed)
                    exists = True

        path.append([item for item in pos_e])
        i_.append([j for j in pos_v])
        for k in e_remove:
            edges.remove(k)

        if not exists:
            print('Path does not exist')
            return []
        if final in i_[-1]: found = True

    return path

def final_path(paths, final):
    end_path = []

    # Starting from the end, the path is built reversed
    for item in reversed(paths):
        for k in item:
            if k.split('-')[1] == final:
                end_path.append(k)
                final = k.split('-')[0]
                break

    return end_path

