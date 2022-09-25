import pygame as p
import Functions.Read_Maze as rm
import collections
import numpy as np
p.init()



#A node to let the agent take multiple paths
class BFSNode:

    #it has a position, a list of directions taken
    # a path (a list of the positions it went through)
    # and a list of the valid positions for this node
    # (to remember where it can go back)
    def __init__(self,position,directions,path,validPositions):
        self.position = position
        self.directions = directions
        self.path = path
        self.validPositions = validPositions




class BFSPath:

    """

    TODO: check if the validPositions atribute can be removed
          using the only the path in its place

    TODO: check if the reference to validPositions needs to be per node
          (instead of using newValidPositions and node.validPositions, just use
          validPositions [the globalvariable] and remove the reference per node)
    """

    #the agent has a starting point
    #and an objective
    def __init__(self,startPoint,objective):

        #adjust the starting point to the coordinate system
        self.start = tuple(np.subtract((Alto,Ancho),startPoint))
        self.objective = objective


        #create a queue for the list of possible paths
        self.Paths = collections.deque()

        #create a copy of the valid positions
        valPos = validPositions.copy()

        #and add a firt node to the queue
        self.Paths.append(BFSNode(self.start,[],[self.start],valPos))


    #functions to check if it can move
    def tryUp(self,node):

        #calculate the next move of a given node
        nextMove = tuple(np.subtract(node.position,(verticalStep,0)))

        #check if the node is in the list of valid Positions
        validMove = nextMove in node.validPositions

        #if the node has a path
        if node.path != None:

            #check if this next move isn't in the path
            Backtrack = nextMove in node.path


        return validMove and not Backtrack

    def tryDown(self,node):
        nextMove = tuple(np.add(node.position,(verticalStep,0)))

        validMove = nextMove in node.validPositions
        if node.path != None:
            Backtrack = nextMove in node.path

        return validMove and not Backtrack

    def tryLeft(self,node):
        nextMove = tuple(np.subtract(node.position,(0,horizontalStep)))

        validMove =  nextMove in node.validPositions
        if node.path != None:
            Backtrack = nextMove in node.path

        return validMove and not Backtrack

    def tryRight(self,node):
        nextMove = tuple(np.add(node.position,(0,horizontalStep)))

        validMove = nextMove in node.validPositions
        if node.path != None:
            Backtrack = nextMove in node.path

        return validMove and not Backtrack



    def CheckObjective(self,position):
        return (position == self.objective)



    def explore(self):

        """
        Function to explore

        returns:
            0 (still exploring)
            1 (found the objective)
            -1 (ran out of valid positions and asumes the objective is unreachable)
        """

        #if there's node in the queue
        if self.Paths:

            #take the first
            node = self.Paths.popleft()

            #if it isn't in the objective
            if not self.CheckObjective(node.position):

                #check if it can move up
                if self.tryUp(node):

                    #calculate the new position
                    newPosition = tuple(np.subtract(node.position,(verticalStep,0)))

                    #remove the position of the node from the list of valid positions
                    newValidPositions = node.validPositions
                    if node.position in newValidPositions:
                        newValidPositions.remove(node.position)

                    #create a new node
                    #remember to pass a copy of directions and path
                    #not the originals
                    newNode = BFSNode(newPosition,node.directions.copy(),node.path.copy(),newValidPositions)

                    #add the instruction to this new node's directions
                    newNode.directions.append("up")

                    #add the new position to the path
                    newNode.path.append(newPosition)

                    #add the node to the queue
                    self.Paths.append(newNode)

                if self.tryLeft(node):
                    newPosition = tuple(np.subtract(node.position,(0,horizontalStep)))
                    newValidPositions = node.validPositions
                    if node.position in newValidPositions:
                        newValidPositions.remove(node.position)
                    newNode = BFSNode(newPosition,node.directions.copy(),node.path.copy(),newValidPositions)
                    newNode.directions.append("left")
                    newNode.path.append(newPosition)
                    self.Paths.append(newNode)

                if self.tryDown(node):
                    newPosition = tuple(np.add(node.position,(verticalStep,0)))
                    newValidPositions = node.validPositions
                    if node.position in newValidPositions:
                        newValidPositions.remove(node.position)
                    newNode = BFSNode(newPosition,node.directions.copy(),node.path.copy(),newValidPositions)
                    newNode.directions.append("down")
                    newNode.path.append(newPosition)
                    self.Paths.append(newNode)

                if self.tryRight(node):
                    newPosition = tuple(np.add(node.position,(0,horizontalStep)))
                    newValidPositions = node.validPositions
                    if node.position in newValidPositions:
                        newValidPositions.remove(node.position)
                    newNode = BFSNode(newPosition,node.directions.copy(),node.path.copy(),newValidPositions)
                    newNode.directions.append("right")
                    newNode.path.append(newPosition)
                    self.Paths.append(newNode)

                return 0


            #if we are in the objective
            else:
                print("Objective found")
                print("Path:")

                for action in node.directions:
                    print(action)

                return node


        return -1



class DFSPath:

    #The agent need a starting point and an objective
    def __init__(self,start,objective):

        #adjust the starting point to the coordinate system
        self.start = tuple(np.subtract((Alto,Ancho),start))
        self.objective = objective


        #Set the agent's currrent position to the start
        self.actualPosition = self.start

        #Start a stack to store the actual path
        self.actualPath = collections.deque()
        #And add the actual position (start) to the stack
        self.actualPath.append(self.actualPosition)

        #also, a stack to add the instructions
        #"up","down","left","right" (always lowercase)
        self.directions = collections.deque()


    #check if the agent can move up
    def tryUp(self):

        #Calculate the next move (take a vertical step up)
        nextMove = tuple(np.subtract(self.actualPosition,(verticalStep,0)))

        #Check if this step is in the valid positions
        validMove = nextMove in validPositions

        #check if the agent already went through that point
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack


    #check if the agent can move down
    def tryDown(self):
        nextMove = tuple(np.add(self.actualPosition,(verticalStep,0)))

        validMove = nextMove in validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    #check if the agent can move left
    def tryLeft(self):
        nextMove = tuple(np.subtract(self.actualPosition,(0,horizontalStep)))

        validMove =  nextMove in validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    #check if the agent can move right
    def tryRight(self):
        nextMove = tuple(np.add(self.actualPosition,(0,horizontalStep)))

        validMove = nextMove in validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    #check if the actual position is the objective
    def CheckObjective(self):
        return (self.actualPosition == self.objective)



    def explore(self):
        """
        Function to explore

        returns:
            0 (still exploring)
            1 (found the objective)
            -1 (ran out of valid positions and asumes the objective is unreachable)
        """

        #check if we have reached the objective yet
        #if not
        if not self.CheckObjective():

            #check if it can move (priorizes up > left > down > right)
            if self.tryUp():

                #if it can move, calculate the new position
                self.actualPosition = tuple(np.subtract(self.actualPosition,(verticalStep,0)))

                #append the new direction
                self.directions.append("up")

                #add the new position to our path
                self.actualPath.append(self.actualPosition)

            elif self.tryLeft():
                self.actualPosition = tuple(np.subtract(self.actualPosition,(0,horizontalStep)))
                self.directions.append("left")
                self.actualPath.append(self.actualPosition)

            elif self.tryDown():
                self.actualPosition = tuple(np.add(self.actualPosition,(verticalStep,0)))
                self.directions.append("down")
                self.actualPath.append(self.actualPosition)

            elif self.tryRight():
                self.actualPosition = tuple(np.add(self.actualPosition,(0,horizontalStep)))
                self.directions.append("right")
                self.actualPath.append(self.actualPosition)

            #if it cannot move
            else:
                #check if the path is not void (we aren't in the start)
                if self.actualPath:

                    #if so, remove the last action and take that
                    #position out of our valid positions
                    validPositions.remove(self.actualPath.pop())

                    #if actualPath is not empty
                    if self.actualPath:
                        #"take one step back"
                        #(change position to the last position in the path)
                        self.actualPosition = self.actualPath[-1]

                    #if our actualPath is empty
                    #we ran out of options
                    else:
                        return -1

                #remove the last direction taken
                if self.directions:
                    self.directions.pop()


            return 0


        #if we are in out objective
        else:
            print("Objective found")
            print("Path:")
            for action in self.directions:
                print(action)

            return 1








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

ventana = p.display.set_mode((800,600), p.RESIZABLE)
Pantalla = p.display.get_surface()
Ancho = Pantalla.get_width()
Alto= Pantalla.get_height()

p.display.set_caption('Muro')
reloj = p.time.Clock()

AZUL=(0,0,128)
NEGRO=(0,0,0)
BLANCO=(255,255,255)

y=int(input("size of maze: "))

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

DFSagent = DFSPath(startPosition,objecitvePosition)
BFSagent = BFSPath(startPosition,objecitvePosition)

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


    """
    DFSagent.explore()
    print(DFSagent.actualPosition)
    p.draw.rect(ventana,(255,255,0),p.Rect(DFSagent.actualPosition[1] + (Ancho/(4*y)),DFSagent.actualPosition[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    """

    if state == 0:
        state = BFSagent.explore()

        for possiblePath in BFSagent.Paths:
                p.draw.rect(ventana,(255,255,0),p.Rect(possiblePath.position[1] + (Ancho/(4*y)),possiblePath.position[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))

    if state not in [0,-1]:
        for action in state.path:
            p.draw.rect(ventana,(255,255,0),p.Rect(action[1] + (Ancho/(4*y)),action[0] + (Alto/(4*y)),(Ancho/(2*y)),(Alto/(2*y))))


    p.display.flip()




p.quit()

