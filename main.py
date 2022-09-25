import pygame as p
import Functions.Read_Maze as rm
import collections
import numpy as np
from queue import PriorityQueue

from Functions import UCS,IDDFS,DFS,BFS


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

ventana = p.display.set_mode((800,600), p.RESIZABLE)
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

startPosition = (1 * (Alto/y),2 * (Ancho/y))
objecitvePosition = (0, 0 + (Ancho/y))

horizontalStep = Ancho/y
verticalStep = Alto/y






listaMuros = construir_mapa(mapa, y)
validPositions = [(muro[1],muro[0]) for muro in listaMuros]
listaPuntos = construir_puntos(mapa, y)

DFSagent = DFS.DFSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
BFSagent = BFS.BFSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
IDDFSagent = IDDFS.IDDFSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
UCSagent = UCS.UCSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)

state = 0

while not gameOver:



    reloj.tick(15)



    for event in p.event.get():
        if event.type == p.QUIT:
            gameOver=True

    #-------------Fondo------------------
    ventana.fill(BLANCO)
    #------------Dibujo------------------
    dibujar_mapa (ventana , listaMuros, listaPuntos)
    p.draw.rect(ventana,(0,255,0),p.Rect(Ancho-startPosition[1] + (Ancho/(4*y)),Alto-startPosition[0] + (Alto/(4*y)),(Ancho/y)/2,(Alto/y)/2))
    p.draw.rect(ventana,(255,0,0),p.Rect(objecitvePosition[1] + (Ancho/(4*y)),objecitvePosition[0] + (Alto/(4*y)),(Ancho/y)/2,(Alto/y)/2))



    DFSagent.explore()
    p.draw.rect(ventana,(255,255,0),p.Rect(DFSagent.actualPosition[1] + (Ancho/(4*y)),DFSagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))



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
    state = IDDFSagent.explore()
    print(IDDFSagent.maxDepth)

    p.draw.rect(ventana,(255,255,0),p.Rect(IDDFSagent.actualPosition[1] + (Ancho/(4*y)),IDDFSagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))
    """


    """

    if state == 0:
        state = UCSagent.explore()

    if state in [0,1]:
        for item in UCSagent.fringe.queue:
                p.draw.rect(ventana,(255,255,0),p.Rect(item[1].position[1] + (Ancho/(4*y)),item[1].position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    if state not in [0,-1]:
        for item in state[1]:
                p.draw.rect(ventana,(255,255,0),p.Rect(item[1].position[1] + (Ancho/(4*y)),item[1].position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    """




    p.display.flip()




p.quit()

