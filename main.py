import pygame as p
import Functions.Read_Maze as rm
import collections
import numpy as np
from queue import PriorityQueue

from Functions import UCS,IDDFS,DFS,BFS,Greedy,Astar


p.init()








#-------------------Muros------------------------
def construir_mapa(mapa, n):
    listaMuros = []
    x= 0
    y= 0
    for fila in mapa:
        for muro in fila:
            if muro == "X":
                listaMuros.append(p.Rect(x,y,Ancho/n,Alto/n))
            x+= Ancho/n
        x= 0
        y+=Alto/n
    return listaMuros
#-------------------Puntos-------------------------
def construir_puntos(mapa, n):
    listaPuntos = []
    x= (Ancho/n)/4
    y= (Alto/n)/4
    for fila in mapa:
        for muro in fila:
            if muro == " ":
                listaPuntos.append(p.Rect(x,y,(Ancho/n)/2,(Alto/n)/2))
            x+= Ancho/n
        x= (Ancho/n)/4
        y+=Alto/n
    return listaPuntos


def dibujar_muro ( superficie , rectangulo, color ) : #Dibujamos un rectángulo
   p.draw.rect( superficie , color , rectangulo )

def dibujar_mapa ( superficie , listaMuros , listaPuntos) : #Dibujamos ListaMuros con los rectángulos muro
    for muro in listaMuros :
        dibujar_muro ( superficie , muro , AZUL )
    for puntos in listaPuntos :
        dibujar_muro ( superficie , puntos , NEGRO )


y=int(input("size of maze: "))

ventana = p.display.set_mode((800,800), p.RESIZABLE)
Pantalla = p.display.get_surface()
Ancho = Pantalla.get_width()
Alto= Pantalla.get_height()

p.display.set_caption('Muro')
reloj = p.time.Clock()

AZUL=(0,0,128)
NEGRO=(0,0,0)
BLANCO=(255,255,255)


m= rm.ReadMaze(f"maze_{y}x{y}.csv")
mapa = rm.ConvertMatrixToMap(m)

gameOver = False


# STARTING POINT AND OBJECTIVE
# THEY ARE GIVEN IN (y,x) AND ALL THE CODE USES THAT COORDINATE DISTRIBUTION
# SO IT'S BETTER TO KEEP IT (y = vertical, x = horizontal)

###     NOTE: BOTH USE A DIFFERENT COORDINATE SYSTEM
###     startPosition takes the LOWER RIGHT CORNER AS (0,0)
###     objectivePosition takes the THE UPPER LEFT CORNER AS (0,0)

# TO CHANGE STARTING POINT CHANGE THE MULTIPLES:
# EXAMPLE: TO SET STARTING POSITION TO (3,4)
#     THIRD ROW FROM THE BOTTOM, FOURTH COLUMN FROM THE RIGHT
#     startPosition = (3 * (Alto/y), 4 * (Ancho/y))

# TO CHANGE OBJECTIVE POSITION, COUNT FROM THE UPPER LEFT CORNER
# BECAUSE (0,0) IS THE UPPER LEFT CORNER
# TO MOVE AN SPACE TO THE LEFT (FOR EXAMPLE (0,4)), ADD TO THE MULTIPLIER OF (Ancho/y)
#     objecitvePosition = (0, 4 * (Ancho/y))
# TO MOVE AN SPACE BELOW, (FOR EXAMPLE (5,0)), ADD TO THE MULTIPLIER OF (Alto/y)
#     objecitvePosition = (5 * (Alto/y), 0)
# SUBTRACT TO MOVE TO THE RIGHT OR TO MOVE UP, RESPECTIVELY
# another example: set objectivePosition to second row from the top, third column from the left
#     objecitvePosition = (2 * (Alto/y), 3 * (Ancho/y))


horizontalStep = Ancho/y
verticalStep = Alto/y


#startPosition = (0 * (Alto/y), 1 * (Ancho/y))
#objecitvePosition = (Alto - 1 * (Alto/y), Ancho - 2 * (Ancho/y))




listaMuros = construir_mapa(mapa, y)
listaPuntos = construir_puntos(mapa, y)

validPositions = [(muro[1] - verticalStep/4,muro[0] - horizontalStep/4) for muro in listaPuntos]

startPosition = validPositions[0]
objecitvePosition = validPositions[-1]

DFSagent = DFS.DFSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
BFSagent = BFS.BFSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
IDDFSagent = IDDFS.IDDFSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
UCSagent = UCS.UCSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
Greedyagent = Greedy.GreedyPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
Astaragent = Astar.AstarPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)

state = 0

while not gameOver:



    reloj.tick(30)



    for event in p.event.get():
        if event.type == p.QUIT:
            gameOver=True

    #-------------Fondo------------------
    ventana.fill(BLANCO)
    #------------Dibujo------------------
    dibujar_mapa (ventana , listaMuros, listaPuntos)



    p.draw.rect(ventana,(255,0,0),p.Rect(startPosition[1] + (Alto/y)/4,startPosition[0] + (Ancho/y)/4,(Ancho/y)/2,(Alto/y)/2))
    p.draw.rect(ventana,(0,255,0),p.Rect(objecitvePosition[1] + (Alto/y)/4,objecitvePosition[0] + (Ancho/y)/4,(Ancho/y)/2,(Alto/y)/2))








    """
    if state == 0:
        state = DFSagent.explore()
        p.draw.rect(ventana,(255,255,0),p.Rect(DFSagent.actualPosition[1] + (Ancho/(4*y)),DFSagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    elif state == 1:
        for position in DFSagent.totalPath:
            p.draw.rect(ventana,(255,255,0),p.Rect(position[1] + (Ancho/(4*y)),position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    """


    """
    if state == 0:
        state = BFSagent.explore()

        for possiblePath in BFSagent.Paths:
                p.draw.rect(ventana,(255,255,0),p.Rect(possiblePath.position[1] + (Ancho/(4*y)),possiblePath.position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    if state not in [0,-1]:
        for action in state.path:
            p.draw.rect(ventana,(255,255,0),p.Rect(action[1] + (Ancho/(4*y)),action[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))
    """



    """
    if state == 0:
        state = IDDFSagent.explore()
        p.draw.rect(ventana,(255,255,0),p.Rect(IDDFSagent.actualPosition[1] + (Ancho/(4*y)),IDDFSagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    elif state == 1:
        for position in IDDFSagent.actualPath:
            p.draw.rect(ventana,(255,255,0),p.Rect(position[1] + (Ancho/(4*y)),position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))
    """



    """
    if state == 0:
        state = UCSagent.explore()

    if state in [0,1]:
        for item in UCSagent.fringe.queue:
                p.draw.rect(ventana,(255,255,0),p.Rect(item[1].position[1] + (Ancho/(4*y)),item[1].position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    if state not in [0,-1]:
        for position in state[0].actualPath:
            p.draw.rect(ventana,(255,255,0),p.Rect(position[1] + (Ancho/(4*y)),position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    """

    """
    if state == 0:
        state = Greedyagent.explore()
        p.draw.rect(ventana,(255,255,0),p.Rect(Greedyagent.actualPosition[1] + (Ancho/(4*y)),Greedyagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    elif state == 1:
        for position in Greedyagent.actualPath:
            p.draw.rect(ventana,(255,255,0),p.Rect(position[1] + (Ancho/(4*y)),position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    """



    """
    if state == 0:
        state = Astaragent.explore()

    if state in [0,1]:
        for item in Astaragent.fringe.queue:
                p.draw.rect(ventana,(255,255,0),p.Rect(item.position[1] + (Ancho/(4*y)),item.position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    if state not in [0,-1]:
        for position in state[0].actualPath:
            p.draw.rect(ventana,(255,255,0),p.Rect(position[1] + (Ancho/(4*y)),position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    """



    p.display.flip()




p.quit()

