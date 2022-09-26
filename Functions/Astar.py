import collections
import numpy as np
from queue import PriorityQueue
import math

class AstarNode:

    """
    g = cost for going from the start to this node's position
    h = (aproximate) cost from the node to the objective
    """
    def __init__(self,position,directions,actualPath,g,h):
        self.position = position
        self.directions = directions
        self.actualPath = actualPath
        self.g = g
        self.h = h


        self.f = g+h

    def __lt__(self,other):
        return self.f < other.f

    def __le__(self,other):
        return self.f <= other.f

    def __gt__(self,other):
        return self.f > other.f

    def __ge__(self,other):
        return self.f >= other.f

    def __eq__(self,other):
        return self.f == other.f


class AstarPath:

    Alto = 0
    Ancho = 0
    y = 1
    validPositions = None

    verticalStep = None
    horizontalStep = None


    #the agent has a starting point
    #and an objective
    def __init__(self,startPoint,objective, alto, ancho, size, ValidPositions):

        AstarPath.Alto = alto
        AstarPath.Ancho = ancho
        AstarPath.y = size
        AstarPath.validPositions = ValidPositions

        AstarPath.horizontalStep = AstarPath.Ancho/AstarPath.y
        AstarPath.verticalStep = AstarPath.Alto/AstarPath.y


        #adjust the starting point to the coordinate system
        self.start = tuple(np.subtract((AstarPath.Alto,AstarPath.Ancho),startPoint))
        self.objective = objective

        self.validPositions = AstarPath.validPositions.copy()
        self.validPositions.remove(self.start)

        self.fringe = PriorityQueue()

        dist = self.calcDistanceToObjective(self.start)
        self.fringe.put(AstarNode(self.start,[],[self.start],0,dist))



    def CheckObjective(self,position):
        return (position == self.objective)


    #Calculate manhattan distance from a point to the objective
    def calcDistanceToObjective(self,position):
        difference = np.subtract(self.objective,position)
        distance = abs(difference[0]) + abs(difference[1])
        return distance


    #functions to check if it can move
    def tryUp(self,position):

        #calculate the next move of a given node
        nextMove = tuple(np.subtract(position,(AstarPath.verticalStep,0)))

        #check if the position is in the list of valid Positions
        validMove = nextMove in self.validPositions

        return validMove

    def tryDown(self,position):
        nextMove = tuple(np.add(position,(AstarPath.verticalStep,0)))

        validMove = nextMove in self.validPositions

        return validMove

    def tryLeft(self,position):
        nextMove = tuple(np.subtract(position,(0,AstarPath.horizontalStep)))

        validMove =  nextMove in self.validPositions

        return validMove

    def tryRight(self,position):
        nextMove = tuple(np.add(position,(0,AstarPath.horizontalStep)))

        validMove = nextMove in self.validPositions


        return validMove


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

            #if it isn't in the objective
            if not self.CheckObjective(item.position):

                    #check if it can move up
                if self.tryUp(item.position):

                    #calculate the new position
                    newPosition = tuple(np.subtract(item.position,(AstarPath.verticalStep,0)))
                    self.validPositions.remove(newPosition)

                    #create a new node
                    #remember to pass a copy of directions and path
                    #not the originals
                    distance = self.calcDistanceToObjective(newPosition)
                    newNode = AstarNode(newPosition,item.directions.copy(),item.actualPath.copy(),item.g+1,distance)

                    #add the instruction to this new node's directions
                    newNode.directions.append("up")
                    newNode.actualPath.append(newPosition)


                    #add the node to the queue
                    self.fringe.put(newNode)

                if self.tryLeft(item.position):
                    newPosition = tuple(np.subtract(item.position,(0,AstarPath.horizontalStep)))
                    self.validPositions.remove(newPosition)

                    distance = self.calcDistanceToObjective(newPosition)
                    newNode = AstarNode(newPosition,item.directions.copy(),item.actualPath.copy(),item.g+1,distance)

                    newNode.directions.append("left")
                    newNode.actualPath.append(newPosition)

                    self.fringe.put(newNode)

                if self.tryDown(item.position):
                    newPosition = tuple(np.add(item.position,(AstarPath.verticalStep,0)))
                    self.validPositions.remove(newPosition)

                    distance = self.calcDistanceToObjective(newPosition)
                    newNode = AstarNode(newPosition,item.directions.copy(),item.actualPath.copy(),item.g+1,distance)

                    newNode.directions.append("down")
                    newNode.actualPath.append(newPosition)

                    self.fringe.put(newNode)

                if self.tryRight(item.position):
                    newPosition = tuple(np.add(item.position,(0,AstarPath.horizontalStep)))
                    self.validPositions.remove(newPosition)

                    distance = self.calcDistanceToObjective(newPosition)
                    newNode = AstarNode(newPosition,item.directions.copy(),item.actualPath.copy(),item.g+1,distance)

                    newNode.directions.append("right")
                    newNode.actualPath.append(newPosition)

                    self.fringe.put(newNode)

                return 0


            #if we are in the objective
            else:
                print("Objective found")
                print("Path:")

                for action in item.directions:
                    print(action)

                return item, self.fringe.queue.copy()


        return -1


