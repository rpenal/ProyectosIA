import pygame as p
import Functions.Read_Maze as rm
p.init()

class Pared(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image= p.image.load("Images/Wall.png").convert()
        self.rect=self.image.get_rect()

#-------------------Muros------------------------
def construir_mapa(mapa):
    listaMuros = []
    x= 0
    y= 0
    for fila in mapa:
        for muro in fila:
            if muro == "X":
                listaMuros.append(p.Rect(x,y,80,80))
            x+= 80
        x= 0
        y+=80
    return listaMuros

def dibujar_muro ( superficie , rectangulo ) : #Dibujamos un rectángulo
   p.draw.rect ( superficie , VERDE , rectangulo )

def dibujar_mapa ( superficie , listaMuros ) : #Dibujamos ListaMuros con los rectángulos muro
    for muro in listaMuros :
        dibujar_muro ( superficie , muro )

Ancho = 1280
movil= p.Rect(600,600,40,40)
Alto = 720

ventana = p.display.set_mode((Ancho,Alto))
p.display.set_caption('Muro')
reloj = p.time.Clock()

listaPared= p.sprite.Group()
pared=Pared()
listaPared.add(pared)

VERDE=(0,255,0)
NEGRO=(0,0,0)

m= rm.ReadMaze("maze_10x10.csv")
mapa = rm.ConvertMatrixToMap(m)

listaMuros = construir_mapa(mapa)

gameOver = False

while not gameOver:
    #-------------Fondo------------------
    ventana.fill(NEGRO)

    #------------Dibujo------------------
    x=0
    y=0

    for fila in mapa:
        for muro in fila:
            if muro=="X":
                pared.rect.x=x
                pared.rect.y=y
                listaPared.add(pared)
                listaPared.draw(ventana)
            x+=80
        x=0
        y=+80
    dibujar_mapa (ventana , listaMuros)
    p.display.flip()

p.quit()

