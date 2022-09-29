from tkinter import filedialog
import pygame as p
import Functions.Read_Maze as rm

from pygame.locals import *

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
   p.draw.rect( superficie , color , rectangulo, 2,5)

def dibujar_mapa ( superficie , listaMuros , listaPuntos) : #Dibujamos ListaMuros con los rectángulos muro
    for muro in listaMuros :
        dibujar_muro ( superficie , muro , NEGRO )
    for puntos in listaPuntos :
        dibujar_muro ( superficie , puntos ,CAMINO )


# y=int(input("size of maze: "))

ventana = p.display.set_mode((1300,700))
Pantalla = p.display.get_surface()
Ancho = Pantalla.get_width()
Alto= Pantalla.get_height()
c= 0

p.display.set_caption('MazeSolver')
reloj = p.time.Clock()

########## FONTS ##########

myfont = p.font.SysFont('Lucida Console', 20)
timer_font = p.font.SysFont("Calibri", 40)

########## BACKGROUNDS ########## 

menuBg = p.image.load("Images\Background.jpeg").convert_alpha()

########## COLORS ##########

RED = (255, 0, 0)
GREEN = (20, 255, 140)
BLUE = (100, 100, 255)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (194,9,84)
AZUL=(131,223,240)
ROJO=(249,152,144)
VERDE=(173,255,153)
MORADO=(186,117,255)
FRONTERA=(179,31,25)
CAMINO=(104,121,123)
NEGRO=(5,32,10)
PISO=(37,67,67)
BLANCO=(211,223,225)


# m= rm.ReadMaze(f"maze_{y}x{y}.csv")
# mapa = rm.ConvertMatrixToMap(m)
gameOver = False

########## CLASSES, INSTANCES, GROUPS ##########

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        if outline:
            p.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0,5)

        p.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0,5)

        if self.text != '':
            text = myfont.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        pos = p.mouse.get_pos()
        if self.isOver(pos):
            self.color = WHITE
        else:
            self.color = GREY

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

okBtn = button(RED, 250, 300, 200, 25, "ok")

class InputBox:

    COLOR_INACTIVE = BLACK
    COLOR_ACTIVE = WHITE

    def __init__(self, x, y, w, h, text=''):
        self.rect = p.Rect(x, y, w, h)
        self.color = InputBox.COLOR_INACTIVE
        self.text = text
        self.txt_surface = myfont.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):

        if event.type == p.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
        if event.type == p.KEYDOWN:
            if self.active:
                if event.key == p.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == p.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < 10:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = myfont.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        p.draw.rect(screen, self.color, self.rect, 2)

input_box1 = InputBox(300, 300, 140, 32)


def changescn(scn):

    # ~ continuar haciendo lo mismo que abajo
    global menu_s, importMaze_s, mainLoop_s, selectMaze_s, selectAlg_s, importMaze_s
    menu_s = mainLoop_s= importMaze_s = selectMaze_s= selectAlg_s=False

    if scn == "menu":
        menu_s = True
        menu()

    elif scn == "importMaze":
        importMaze_s = True
        importMaze()

    elif scn == "selectMaze":
        selectMaze_s = True
        selectMaze()

    elif scn == "selectAlg":
        selectAlg_s = True
        selectAlg()

    elif scn == "mainLoop":
        mainLoop_s = True
        mainloop()

def openFile():
 
    archivo = filedialog.askopenfilename(title="Import Maze", initialdir="C:/", filetypes = (("CSV Files","*.csv"),("All","*.*")))
    
    return archivo

######### ESCENAS ##########

##### menu

menu_s = bool
def menu():


    global menu_s, gameOver, selectAlg_s, selectMaze_s, mainLoop_s, importMaze_s

    ventana.blit(menuBg, (0, 0))
    mazesBtn = button(RED, 550, 270, 200, 25, "Mazes")
    importBtn = button(RED, 550, 300, 200, 25, "Import")
    exitBtn = button(RED, 550, 360, 200, 25, "EXIT")


    while menu_s:

        
        ##### RENDER #####
        ventana.fill(PISO)
        ventana.blit(menuBg, (0, 0))
        mazesBtn.draw(ventana, (0,0,0))
        importBtn.draw(ventana, (0,0,0))
        exitBtn.draw(ventana, (0,0,0))
        

        ##### EVENTOS #####

        for event in p.event.get():
            pos = p.mouse.get_pos() # toma la posicion del mouse

            if event.type == p.QUIT:
                gameOver = True
                menu_s = False
            if event.type == p.KEYDOWN:
                if event.key == K_ESCAPE:
                    gameOver=True
                    menu_s = False
            if event.type == p.MOUSEBUTTONDOWN:

                ############ control de los botones

                if mazesBtn.isOver(pos):
                    changescn("selectMaze")

                if importBtn.isOver(pos):
                    changescn("importMaze")

                if exitBtn.isOver(pos):
                    importMaze_s = False
                    mainLoop_s = False
                    selectAlg_s = False
                    selectMaze_s= False
                    menu_s = False
                    gameOver = True

        # Refresh Screen
        p.display.flip()

selectMaze_s= bool
def selectMaze():

    global menu_s, selectMaze_s, gameOver, listaMuros, listaPuntos, pause, validPositions, startPosition, objecitvePosition, Ancho, Alto, found, on, route, state, start_tick, verticalStep, horizontalStep, y, start_tick

    mazes5Btn = button(RED, 550, 270, 200, 25, "Maze 5x5")
    mazes10Btn = button(RED, 550, 300, 200, 25, "Maze 10x10")
    mazes50Btn = button(RED, 550, 330, 200, 25, "Maze 50x50")
    mazes100Btn = button(RED, 550, 360, 200, 25, "Maze 100x100")
    mazes400Btn = button(RED, 550, 390, 200, 25, "Maze 400x400")
    backBtn = button(RED, 0, 685, 100, 15, "Back")


    while selectMaze_s:

        ##### RENDER #####
        ventana.blit(menuBg, (0, 0))
        mazes5Btn.draw(ventana, (0,0,0))
        mazes10Btn.draw(ventana, (0,0,0))
        mazes50Btn.draw(ventana, (0,0,0))
        mazes100Btn.draw(ventana, (0,0,0))
        mazes400Btn.draw(ventana, (0,0,0))
        backBtn.draw(ventana, (0,0,0))

        

        ##### EVENTOS #####

        for event in p.event.get():
            pos = p.mouse.get_pos() # toma la posicion del mouse

            if event.type == p.QUIT:
                importMaze_s = False
                mainLoop_s = False
                selectAlg_s = False
                selectMaze_s= False
                menu_s = False
                gameOver = True
            if event.type == p.KEYDOWN:
                if event.key == K_ESCAPE:
                    changescn("menu")
            if event.type == p.MOUSEBUTTONDOWN:

                ############ control de los botones

                if mazes5Btn.isOver(pos):
                    y= 5
                    m= rm.ReadMaze(f"maze_{y}x{y}.csv")
                    mapa = rm.ConvertMatrixToMap(m)
                    listaMuros = construir_mapa(mapa, y)
                    listaPuntos = construir_puntos(mapa, y)
                    horizontalStep= Ancho/y
                    verticalStep= Alto/y
                    validPositions = [(muro[1] - verticalStep/4,muro[0] - horizontalStep/4) for muro in listaPuntos]
                    startPosition = validPositions[0]
                    objecitvePosition = validPositions[-1]
                    pause = False
                    route=[]
                    found=False
                    state= 0
                    on = True
                    changescn("selectAlg")

                if mazes10Btn.isOver(pos):
                    y= 10
                    m= rm.ReadMaze(f"maze_{y}x{y}.csv")
                    mapa = rm.ConvertMatrixToMap(m)
                    listaMuros = construir_mapa(mapa, y)
                    listaPuntos = construir_puntos(mapa, y)
                    horizontalStep= Ancho/y
                    verticalStep= Alto/y
                    validPositions = [(muro[1] - verticalStep/4,muro[0] - horizontalStep/4) for muro in listaPuntos]
                    startPosition = validPositions[0]
                    objecitvePosition = validPositions[-1]
                    pause = False
                    route=[]
                    found=False
                    state= 0
                    on = True
                    changescn("selectAlg")

                if mazes50Btn.isOver(pos):
                    y= 50
                    m= rm.ReadMaze(f"maze_{y}x{y}.csv")
                    mapa = rm.ConvertMatrixToMap(m)
                    listaMuros = construir_mapa(mapa, y)
                    listaPuntos = construir_puntos(mapa, y)
                    horizontalStep= Ancho/y
                    verticalStep= Alto/y
                    validPositions = [(muro[1] - verticalStep/4,muro[0] - horizontalStep/4) for muro in listaPuntos]
                    startPosition = validPositions[0]
                    objecitvePosition = validPositions[-1]
                    pause = False
                    route=[]
                    found=False
                    state= 0
                    on = True
                    changescn("selectAlg")

                if mazes100Btn.isOver(pos):
                    y= 100
                    m= rm.ReadMaze(f"maze_{y}x{y}.csv")
                    mapa = rm.ConvertMatrixToMap(m)
                    listaMuros = construir_mapa(mapa, y)
                    listaPuntos = construir_puntos(mapa, y)
                    horizontalStep= Ancho/y
                    verticalStep= Alto/y
                    validPositions = [(muro[1] - verticalStep/4,muro[0] - horizontalStep/4) for muro in listaPuntos]
                    startPosition = validPositions[0]
                    objecitvePosition = validPositions[-1]
                    pause = False
                    route=[]
                    found=False
                    state= 0
                    on = True
                    changescn("selectAlg")

                if mazes400Btn.isOver(pos):
                    y= 400
                    m= rm.ReadMaze(f"maze_{y}x{y}.csv")
                    mapa = rm.ConvertMatrixToMap(m)
                    listaMuros = construir_mapa(mapa, y)
                    listaPuntos = construir_puntos(mapa, y)
                    horizontalStep= Ancho/y
                    verticalStep= Alto/y
                    validPositions = [(muro[1] - verticalStep/4,muro[0] - horizontalStep/4) for muro in listaPuntos]
                    startPosition = validPositions[0]
                    objecitvePosition = validPositions[-1]
                    pause = False
                    route=[]
                    found=False
                    state= 0
                    on = True
                    changescn("selectAlg")

                if backBtn.isOver(pos):
                    changescn("menu")

        # Refresh Screen
        p.display.flip()


selectAlg_s= bool
def selectAlg():

    global menu_s, selectMaze_s, selectAlg_s, importMaze_s, mainLoop_s, gameOver, Astaragent, DFSagent, BFSagent, IDDFSagent, UCSagent, Greedyagent, Ancho, Alto, gameOver, Alg, y, validPositions, startPosition, objecitvePosition, start_tick, c

    DFSBtn = button(RED, 550, 270, 200, 25, "DFS")
    BFSBtn = button(RED, 550, 300, 200, 25, "BFS")
    UCSBtn = button(RED, 550, 330, 200, 25, "UCS")
    GreedyBtn = button(RED, 550, 360, 200, 25, "Greedy")
    IDDFSBtn = button(RED, 550, 390, 200, 25, "IDDFS")
    AstarBtn = button(RED, 550, 420, 200, 25, "A*")
    backBtn = button(RED, 0, 685, 100, 15, "Back")

    while selectAlg_s:

        ##### RENDER #####

        ventana.fill(PISO)
        ventana.blit(menuBg, (0, 0))
        DFSBtn.draw(ventana, (0,0,0))
        BFSBtn.draw(ventana, (0,0,0))
        UCSBtn.draw(ventana, (0,0,0))
        GreedyBtn.draw(ventana, (0,0,0))
        IDDFSBtn.draw(ventana, (0,0,0))
        AstarBtn.draw(ventana, (0,0,0))
        backBtn.draw(ventana, (0,0,0))
       

        ##### EVENTOS #####

        for event in p.event.get():
            pos = p.mouse.get_pos() # toma la posicion del mouse

            if event.type == p.QUIT:
                importMaze_s = False
                mainLoop_s = False
                selectAlg_s = False
                selectMaze_s= False
                menu_s = False
                gameOver = True
            if event.type == p.KEYDOWN:
                if event.key == K_ESCAPE:
                    changescn("menu")
            if event.type == p.MOUSEBUTTONDOWN:

                ############ control de los botones

                if DFSBtn.isOver(pos):
                    DFSagent = DFS.DFSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
                    Alg= 1
                    start_tick=p.time.get_ticks()
                    changescn("mainLoop")

                if BFSBtn.isOver(pos):
                    BFSagent = BFS.BFSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
                    Alg= 2
                    start_tick=p.time.get_ticks()
                    changescn("mainLoop")

                if UCSBtn.isOver(pos):
                    UCSagent = UCS.UCSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
                    Alg= 3
                    start_tick=p.time.get_ticks()
                    changescn("mainLoop")

                if GreedyBtn.isOver(pos):
                    Greedyagent = Greedy.GreedyPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
                    Alg= 4
                    start_tick=p.time.get_ticks()
                    changescn("mainLoop")

                if IDDFSBtn.isOver(pos):
                    IDDFSagent = IDDFS.IDDFSPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
                    Alg= 5
                    start_tick=p.time.get_ticks()
                    changescn("mainLoop")

                if AstarBtn.isOver(pos):
                    Astaragent = Astar.AstarPath(startPosition,objecitvePosition,Alto,Ancho,y,validPositions)
                    Alg= 6
                    start_tick=p.time.get_ticks()
                    changescn("mainLoop")

                if backBtn.isOver(pos) and not c:
                    changescn("selectMaze")

                if backBtn.isOver(pos) and c:
                    changescn("menu")

        # Refresh Screen
        p.display.flip()

importMaze_s= bool
def importMaze():

    global menu_s, gameOver, importMaze_s, mainLoop_s, selectAlg_s, selectMaze_s, listaMuros, listaPuntos, pause, validPositions, startPosition, objecitvePosition, Ancho, Alto, found, on, route, state, start_tick, verticalStep, horizontalStep, y, start_tick, c

    c= 0
    ImportBtn = button(RED, 550, 270, 200, 25, "Import")
    backBtn = button(RED, 0, 685, 100, 15, "Back")

    while importMaze_s:

        ##### RENDER #####

        ventana.fill(PISO)
        ventana.blit(menuBg, (0, 0))
        ImportBtn.draw(ventana, (0,0,0))
        backBtn.draw(ventana, (0,0,0))
        
        ##### EVENTOS #####

        for event in p.event.get():
            pos = p.mouse.get_pos() # toma la posicion del mouse

            if event.type == p.QUIT:
                importMaze_s = False
                mainLoop_s = False
                selectAlg_s = False
                selectMaze_s= False
                menu_s = False
                gameOver = True
            if event.type == p.KEYDOWN:
                if event.key == K_ESCAPE:
                    changescn("menu")
            if event.type == p.MOUSEBUTTONDOWN:

                ############ control de los botones

                if ImportBtn.isOver(pos):
                    try:
                        MazeRoute= openFile()
                        m= rm.ReadMazePath(MazeRoute)
                        y= len(m)
                        mapa = rm.ConvertMatrixToMap(m)
                        listaMuros = construir_mapa(mapa, y)
                        listaPuntos = construir_puntos(mapa, y)
                        horizontalStep= Ancho/y
                        verticalStep= Alto/y
                        validPositions = [(muro[1] - verticalStep/4,muro[0] - horizontalStep/4) for muro in listaPuntos]
                        startPosition = validPositions[0]
                        objecitvePosition = validPositions[-1]
                        pause = False
                        route=[]
                        found=False
                        state= 0
                        on = True
                        c= 1
                        changescn("selectAlg")
                    except:
                        pass
                if backBtn.isOver(pos):
                    changescn("menu")
                    

        # Refresh Screen
        p.display.flip()




mainLoop_s= bool
def mainloop():

    global mainLoop_s, menu_s, importMaze_s, selectMaze_s, selectAlg_s, gameOver, listaMuros, listaPuntos, pause, validPositions, startPosition, objecitvePosition, Astaragent, DFSagent, BFSagent, IDDFSagent, UCSagent, Greedyagent, Ancho, Alto, gameOver, timer_surf, found, on, time_hms, route, state, start_tick, Alg

    time_hms = 0, 0, 0
    timer_surf = timer_font.render(f'{time_hms[0]:02d}:{time_hms[1]:02d}:{time_hms[2]:02d}', True, (255, 255, 255))
    backBtn = button(RED, 0, 685, 100, 15, "Back")

    while mainLoop_s:


        reloj.tick(30)

        for event in p.event.get():
            pos = p.mouse.get_pos()
            if event.type == p.QUIT:
                importMaze_s = False
                mainLoop_s = False
                selectAlg_s = False
                selectMaze_s= False
                menu_s = False
                gameOver = True

            if event.type == p.KEYDOWN:
                if event.key == K_ESCAPE:
                    changescn("menu")
            if event.type == p.MOUSEBUTTONDOWN:
                on = False
                pause = True
                if backBtn.isOver(pos):
                    changescn("menu")

        while pause:
            for event in p.event.get():
                pos = p.mouse.get_pos()
                if event.type == p.QUIT:
                    importMaze_s = False
                    mainLoop_s = False
                    selectAlg_s = False
                    selectMaze_s= False
                    gameOver = True
                if event.type == p.KEYDOWN:
                    if event.key == K_ESCAPE:
                        changescn("menu")
            if event.type == p.MOUSEBUTTONUP:
                on = True
                pause = False
                if backBtn.isOver(pos):
                    changescn("menu")

        while found:
            for event in p.event.get():
                pos = p.mouse.get_pos()
                if event.type == p.QUIT:
                        importMaze_s = False
                        mainLoop_s = False
                        selectAlg_s = False
                        selectMaze_s= False
                        on= False
                        found = False
                        gameOver=True
                if event.type == p.KEYDOWN:
                    if event.key == K_ESCAPE:
                        on= False
                        found = False
                        changescn("menu")
                if event.type == p.MOUSEBUTTONUP:
                    if backBtn.isOver(pos):
                        changescn("menu")
                    


        if on:
            # get the amount of ticks(milliseconds) that passed from the start
            time_ms = p.time.get_ticks() - start_tick
            new_hms = (time_ms//(1000*60))%60, (time_ms//1000)%60, int(((time_ms/1000)-(time_ms//1000))*1000)
            if new_hms != time_hms:
                time_hms = new_hms
                timer_surf = timer_font.render(f'{time_hms[0]:02d}:{time_hms[1]:02d}:{time_hms[2]:02}', True, (255, 255, 255))

        p.display.update()

        #-------------Fondo------------------
        ventana.fill(PISO)
        #------------Dibujo------------------
        dibujar_mapa (ventana , listaMuros, listaPuntos)

        p.draw.rect(ventana,ROJO,p.Rect(startPosition[1],startPosition[0],(Ancho/y),(Alto/y)),5,15)
        p.draw.rect(ventana,VERDE,p.Rect(objecitvePosition[1] ,objecitvePosition[0],(Ancho/y),(Alto/y)),5,15)

        backBtn.draw(ventana, (0,0,0))

        if Alg==1:
            #DFS
            if state == 0:
                state = DFSagent.explore()
                route.append(p.Rect(DFSagent.actualPosition[1] + (Ancho/(4*y)),DFSagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                p.draw.rect(ventana,BLANCO,p.Rect(DFSagent.actualPosition[1] + (Ancho/(4*y)),DFSagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)

            elif state == 1:
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                for position in DFSagent.totalPath:
                    p.draw.rect(ventana,BLANCO,p.Rect(position[1] + (Ancho/(4*y)),position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)
                found= True


        elif Alg==2:
            #BFS
            if state == 0:
                state = BFSagent.explore()
                for possiblePath in BFSagent.Paths:
                    route.append(p.Rect(possiblePath.position[1] + (Ancho/(4*y)),possiblePath.position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                for possiblePath in BFSagent.Paths:
                    p.draw.rect(ventana,BLANCO,p.Rect(possiblePath.position[1] + (Ancho/(4*y)),possiblePath.position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)

            if state not in [0,-1]:
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                for action in state.path:
                    p.draw.rect(ventana,BLANCO,p.Rect(action[1] + (Ancho/(4*y)),action[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)
                found= True


        elif Alg==3:
            #UCS
            if state == 0:
                state = UCSagent.explore()

            if state in [0,1]:
                for item in UCSagent.fringe.queue:
                    route.append(p.Rect(item[1].position[1] + (Ancho/(4*y)),item[1].position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                for item in UCSagent.fringe.queue:
                    p.draw.rect(ventana,BLANCO,p.Rect(item[1].position[1] + (Ancho/(4*y)),item[1].position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)

            if state not in [0,-1]:
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                for position in state[0].actualPath:
                    p.draw.rect(ventana,BLANCO,p.Rect(position[1] + (Ancho/(4*y)),position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)
                found= True

        elif Alg==4:
            #Greedy
            if state == 0:
                state = Greedyagent.explore()
                route.append(p.Rect(Greedyagent.actualPosition[1] + (Ancho/(4*y)),Greedyagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))
                p.draw.rect(ventana,BLANCO,p.Rect(Greedyagent.actualPosition[1] + (Ancho/(4*y)),Greedyagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                p.draw.rect(ventana,BLANCO,p.Rect(Greedyagent.actualPosition[1] + (Ancho/(4*y)),Greedyagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)

            elif state == 1:
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                for position in Greedyagent.actualPath:
                    p.draw.rect(ventana,BLANCO,p.Rect(position[1] + (Ancho/(4*y)),position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)
                found= True
        
        elif Alg==5:
            #IDDFS
            if state == 0:
                state = IDDFSagent.explore()
                route.append(p.Rect(IDDFSagent.actualPosition[1] + (Ancho/(4*y)),IDDFSagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                p.draw.rect(ventana,BLANCO,p.Rect(IDDFSagent.actualPosition[1] + (Ancho/(4*y)),IDDFSagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)

            elif state == 1:
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                for position in IDDFSagent.actualPath:
                    p.draw.rect(ventana,BLANCO,p.Rect(position[1] + (Ancho/(4*y)),position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)
                found= True

        elif Alg==6:
            #Astar
            if state == 0:
                state = Astaragent.explore()

            if state in [0,1]:
                for item in Astaragent.fringe.queue:
                    route.append(p.Rect(item.position[1] + (Ancho/(4*y)),item.position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                for item in Astaragent.fringe.queue:
                    p.draw.rect(ventana,BLANCO,p.Rect(item.position[1] + (Ancho/(4*y)),item.position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)

            if state not in [0,-1]:
                for r in route:
                    p.draw.rect(ventana,FRONTERA,r,0,10)
                for position in state[0].actualPath:
                    p.draw.rect(ventana,BLANCO,p.Rect(position[1] + (Ancho/(4*y)),position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))),0,10)
                found= True

        ventana.blit(timer_surf, (Ancho/2.3, Alto/1000))

        p.display.flip()

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

while not gameOver:

    menu()

p.quit()


