import collections
import numpy as np
from queue import PriorityQueue


class UCSNode:
    def __init__(self,position,directions,actualPath):
        self.position = position
        self.directions = directions
        self.actualPath = actualPath

    def __lt__(self,other):
        return True

    def __le__(self,other):
        return False

    def __gt__(self,other):
        return False

    def __ge__(self,other):
        return True

    def __eq__(self,other):
        return True




class UCSPath:

    Alto = 0
    Ancho = 0
    y = 1
    validPositions = []

    verticalStep = 0
    horizontalStep = 0

    def __init__(self,startingPoint,objective,alto,ancho,size,ValidPositions):

        UCSPath.Alto = alto
        UCSPath.Ancho = ancho
        UCSPath.y = size
        UCSPath.validPositions = ValidPositions

        UCSPath.horizontalStep = UCSPath.Ancho/UCSPath.y
        UCSPath.verticalStep = UCSPath.Alto/UCSPath.y


        #adjust the starting point to the coordinate system
        self.start = startingPoint
        self.objective = objective

        self.validPositions = UCSPath.validPositions.copy()
        self.validPositions.remove(self.start)

        self.fringe = PriorityQueue()

        self.fringe.put((0,UCSNode(self.start,[],[self.start])))




    #obtain the adjacent valid positions to a given position
    def adjacentPositions(self,position):
        adjacent = []
        adjacent.append(tuple(np.subtract(position,(UCSPath.verticalStep,0))))
        adjacent.append(tuple(np.add(position,(UCSPath.verticalStep,0))))
        adjacent.append(tuple(np.subtract(position,(0,UCSPath.horizontalStep))))
        adjacent.append(tuple(np.add(position,(0,UCSPath.horizontalStep))))

        for possible in adjacent:
            if possible not in UCSPath.validPositions:
                adjacent.remove(possible)

        return adjacent

    #functions to check if it can move
    def tryUp(self,position):

        #calculate the next move of a given node
        nextMove = tuple(np.subtract(position,(UCSPath.verticalStep,0)))

        #check if the position is in the list of valid Positions
        validMove = nextMove in self.validPositions

        return validMove

    def tryDown(self,position):
        nextMove = tuple(np.add(position,(UCSPath.verticalStep,0)))

        validMove = nextMove in self.validPositions

        return validMove

    def tryLeft(self,position):
        nextMove = tuple(np.subtract(position,(0,UCSPath.horizontalStep)))

        validMove =  nextMove in self.validPositions

        return validMove

    def tryRight(self,position):
        nextMove = tuple(np.add(position,(0,UCSPath.horizontalStep)))

        validMove = nextMove in self.validPositions


        return validMove



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
        if not self.fringe.empty():

            #get the highest priority item
            item = self.fringe.get()
            priority = item[0]
            node = item[1]

            #if it isn't in the objective
            if not self.CheckObjective(node.position):

                #check if it can move up
                if self.tryUp(node.position):

                    #calculate the new position
                    newPosition = tuple(np.subtract(node.position,(UCSPath.verticalStep,0)))
                    self.validPositions.remove(newPosition)

                    #create a new node
                    #remember to pass a copy of directions and path
                    #not the originals
                    newNode = UCSNode(newPosition,node.directions.copy(),node.actualPath.copy())

                    #add the instruction to this new node's directions
                    newNode.directions.append("up")
                    newNode.actualPath.append(newPosition)

                    #add the node to the queue
                    self.fringe.put((priority+1,newNode))

                if self.tryLeft(node.position):
                    newPosition = tuple(np.subtract(node.position,(0,UCSPath.horizontalStep)))
                    self.validPositions.remove(newPosition)

                    newNode = UCSNode(newPosition,node.directions.copy(),node.actualPath.copy())
                    newNode.directions.append("left")
                    newNode.actualPath.append(newPosition)

                    self.fringe.put((priority+1,newNode))

                if self.tryDown(node.position):
                    newPosition = tuple(np.add(node.position,(UCSPath.verticalStep,0)))
                    self.validPositions.remove(newPosition)

                    newNode = UCSNode(newPosition,node.directions.copy(),node.actualPath.copy())
                    newNode.directions.append("down")
                    newNode.actualPath.append(newPosition)

                    self.fringe.put((priority+1,newNode))

                if self.tryRight(node.position):
                    newPosition = tuple(np.add(node.position,(0,UCSPath.horizontalStep)))
                    self.validPositions.remove(newPosition)

                    newNode = UCSNode(newPosition,node.directions.copy(), node.actualPath.copy())
                    newNode.directions.append("right")
                    newNode.actualPath.append(newPosition)

                    self.fringe.put((priority+1,newNode))

                return 0


            #if we are in the objective
            else:
                print("Objective found")
                print("Path:")

                for action in node.directions:
                    print(action)

                return node, self.fringe.queue.copy()


        return -1

