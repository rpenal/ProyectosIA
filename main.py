from turtle import ycor
import pygame as p
import Functions.Read_Maze as rm
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
        dibujar_muro ( superficie , muro , VERDE )
    for puntos in listaPuntos :
        dibujar_muro ( superficie , puntos , NEGRO )

ventana = p.display.set_mode((800,600), p.RESIZABLE)
Pantalla = p.display.get_surface()
Ancho = Pantalla.get_width()
Alto= Pantalla.get_height()

p.display.set_caption('Muro')
reloj = p.time.Clock()

VERDE=(0,255,0)
NEGRO=(0,0,0)
BLANCO=(255,255,255)

x=input("Name of the maze: ")
y=int(input("size of maze: "))

m= rm.ReadMaze(x)
mapa = rm.ConvertMatrixToMap(m)

listaMuros = construir_mapa(mapa, y)
listaPuntos = construir_puntos(mapa, y)

gameOver = False

while not gameOver:

    reloj.tick(60)
    Ancho = Pantalla.get_width()
    Alto= Pantalla.get_height()
    listaMuros = construir_mapa(mapa, y)
    listaPuntos = construir_puntos(mapa, y)
    
    for event in p.event.get():
        if event.type == p.QUIT:
            gameOver=True

    #-------------Fondo------------------
    ventana.fill(BLANCO)
    #------------Dibujo------------------
    dibujar_mapa (ventana , listaMuros, listaPuntos)
    p.display.flip()

p.quit()

