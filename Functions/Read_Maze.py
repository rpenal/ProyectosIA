import csv

x= input("Escriba el Laberinto: ")
matrix= []
with open('Mazes/%s' %x) as maze:
    contador= 0
    reader = csv.reader(maze)
    for row in reader:
        if contador == 0 and row != '':
            matrix.append(row)
            contador= 1
        else:
            contador= 0
            pass

print(matrix)

