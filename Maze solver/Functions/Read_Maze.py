import csv

def ReadMaze(NameMaze):
    matrix= []
    with open('Mazes/%s' %NameMaze) as maze:
        contador= 0
        reader = csv.reader(maze)
        for row in reader:
            if contador == 0 and row != '':
                matrix.append(row)
                contador= 1
            else:
                contador= 0
                pass
    return matrix

def ReadMazePath(path):
    matrix= []
    with open('%s' %path) as maze:
        contador= 0
        reader = csv.reader(maze)
        for row in reader:
            if contador == 0 and row != '':
                matrix.append(row)
                contador= 1
            else:
                contador= 0
                pass
    return matrix

def ConvertMatrixToMap(matrix):
    map = []
    for i in matrix:
        t = ''
        for x in i:
            if x == 'w':
                t+= 'X'
            if x == 'c':
                t+= ' '
        map.append(t)
    return map



