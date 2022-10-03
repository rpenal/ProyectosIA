import igraph
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
import numpy as np

#obtain the adjacent valid positions to a given position
def adjacentPositions(position):
    adjacent = []
    adjacent.append(tuple(np.subtract(position,(1,0))))
    adjacent.append(tuple(np.add(position,(1,0))))
    adjacent.append(tuple(np.subtract(position,(0,1))))
    adjacent.append(tuple(np.add(position,(0,1))))

    i = 0
    while len(adjacent) > i:
        if adjacent[i] not in validPositions:
            adjacent.remove(adjacent[i])
            i-=1
        i+=1

    ind = validPositions.index(position)
    adjacent = [(ind,validPositions.index(pos)) for pos in adjacent]
    return adjacent

#def graphTree(path):

validPositions = [(1.0, 0.0), (1.0, 1.0), (3.0, 1.0), (1.0, 2.0), (2.0, 2.0), (3.0, 2.0), (1.0, 3.0), (3.0, 3.0), (3.0, 4.0)]
layers = [[0], [1], [3], [4, 6], [5], [2, 7], [8]]


v_label = list(map(str, range(len(validPositions))))






E = [] # list of edges
for pos in validPositions:
    E += adjacentPositions(pos)

depths = {0: 0, 1: 1, 3: 2, 4: 3, 6: 3, 5: 4, 2: 5, 7: 5, 8: 6}

positions = {}

for ind in range(len(layers)):
    if len(layers[ind]) == 1:
        positions[layers[ind][0]] = [0,depths[layers[ind][0]]]
    elif len(layers[ind]) == 2:
        positions[layers[ind][0]] = [-1,depths[layers[ind][0]]]
        positions[layers[ind][1]] = [1,depths[layers[ind][1]]]



L = len(positions)
Xn = [positions[k][0] for k in range(L)]
Yn = [12-positions[k][1] for k in range(L)]
Xe = []
Ye = []
for edge in E:
    Xe+=[positions[edge[0]][0],positions[edge[1]][0], None]
    Ye+=[12-positions[edge[0]][1],12-positions[edge[1]][1], None]

labels = [(validPositions[int(label)][0] * 160, validPositions[int(label)][1] * 160)  for label in v_label]

path = [(0.0, 160.0), (160.0, 160.0), (320.0, 160.0), (320.0, 320.0), (320.0, 480.0), (480.0, 480.0), (640.0, 480.0)]
path = [(pos[1]/160,pos[0]/160) for pos in path]

pathway = []
for ind in range(len(path)-1):
    pathway.append((validPositions.index(path[ind]),validPositions.index(path[ind+1])))
print(pathway)

Xp = []
Yp = []

for edge in pathway:
    Xp+=[positions[edge[0]][0],positions[edge[1]][0], None]
    Yp+=[12-positions[edge[0]][1],12-positions[edge[1]][1], None]

fig = go.Figure()
fig.add_trace(go.Scatter(x=Xe,
                   y=Ye,
                   mode='lines',
                   line=dict(color='rgb(210,210,210)', width=3),
                   hoverinfo='none'
                   ))

fig.add_trace(go.Scatter(x=Xp,
                   y=Yp,
                   mode='lines',
                   line=dict(color='rgb(210,0,0)', width=5),
                   hoverinfo='none'
                   ))


fig.add_trace(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers+text',
                  name="text",
                  marker=dict(symbol='circle-dot',
                                size=18,
                                color='#6175c1',    #'#DB4551',
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                  text=labels,
                  textposition= "middle left",
                  opacity=0.8
                  ))

fig.show()