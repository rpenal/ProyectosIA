import collections
import numpy as np
from queue import PriorityQueue


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

    Alto = 0
    Ancho = 0
    y = 1
    validPositions = None

    verticalStep = None
    horizontalStep = None

    """

    TODO: check if the validPositions atribute can be removed
          using the only the path in its place

    TODO: check if the reference to validPositions needs to be per node
          (instead of using newValidPositions and node.validPositions, just use
          validPositions [the globalvariable] and remove the reference per node)
    """

    #the agent has a starting point
    #and an objective
    def __init__(self,startPoint,objective, alto, ancho, size, ValidPositions):

        BFSPath.Alto = alto
        BFSPath.Ancho = ancho
        BFSPath.y = size
        BFSPath.validPositions = ValidPositions

        BFSPath.horizontalStep = BFSPath.Ancho/BFSPath.y
        BFSPath.verticalStep = BFSPath.Alto/BFSPath.y

        #adjust the starting point to the coordinate system
        self.start = startPoint
        self.objective = objective


        #create a queue for the list of possible paths
        self.Paths = collections.deque()

        #create a copy of the valid positions
        valPos = BFSPath.validPositions.copy()

        #and add a firt node to the queue
        self.Paths.append(BFSNode(self.start,[],[self.start],valPos))


    #functions to check if it can move
    def tryUp(self,node):

        #calculate the next move of a given node
        nextMove = tuple(np.subtract(node.position,(BFSPath.verticalStep,0)))

        #check if the node is in the list of valid Positions
        validMove = nextMove in node.validPositions

        #if the node has a path
        if node.path != None:

            #check if this next move isn't in the path
            Backtrack = nextMove in node.path


        return validMove and not Backtrack

    def tryDown(self,node):
        nextMove = tuple(np.add(node.position,(BFSPath.verticalStep,0)))

        validMove = nextMove in node.validPositions
        if node.path != None:
            Backtrack = nextMove in node.path

        return validMove and not Backtrack

    def tryLeft(self,node):
        nextMove = tuple(np.subtract(node.position,(0,BFSPath.horizontalStep)))

        validMove =  nextMove in node.validPositions
        if node.path != None:
            Backtrack = nextMove in node.path

        return validMove and not Backtrack

    def tryRight(self,node):
        nextMove = tuple(np.add(node.position,(0,BFSPath.horizontalStep)))

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
                    newPosition = tuple(np.subtract(node.position,(BFSPath.verticalStep,0)))

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
                    newPosition = tuple(np.subtract(node.position,(0,BFSPath.horizontalStep)))
                    newValidPositions = node.validPositions
                    if node.position in newValidPositions:
                        newValidPositions.remove(node.position)
                    newNode = BFSNode(newPosition,node.directions.copy(),node.path.copy(),newValidPositions)
                    newNode.directions.append("left")
                    newNode.path.append(newPosition)
                    self.Paths.append(newNode)

                if self.tryDown(node):
                    newPosition = tuple(np.add(node.position,(BFSPath.verticalStep,0)))
                    newValidPositions = node.validPositions
                    if node.position in newValidPositions:
                        newValidPositions.remove(node.position)
                    newNode = BFSNode(newPosition,node.directions.copy(),node.path.copy(),newValidPositions)
                    newNode.directions.append("down")
                    newNode.path.append(newPosition)
                    self.Paths.append(newNode)

                if self.tryRight(node):
                    newPosition = tuple(np.add(node.position,(0,BFSPath.horizontalStep)))
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

