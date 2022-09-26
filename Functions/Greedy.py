import collections
import numpy as np
from queue import PriorityQueue
import math

class GreedyPath:
    Alto = 0
    Ancho = 0
    y = 1
    validPositions = None

    verticalStep = None
    horizontalStep = None


    #the agent has a starting point
    #and an objective
    def __init__(self,startPoint,objective, alto, ancho, size, ValidPositions):

        GreedyPath.Alto = alto
        GreedyPath.Ancho = ancho
        GreedyPath.y = size
        GreedyPath.validPositions = ValidPositions.copy()

        GreedyPath.horizontalStep = GreedyPath.Ancho/GreedyPath.y
        GreedyPath.verticalStep = GreedyPath.Alto/GreedyPath.y

        #adjust the starting point to the coordinate system
        self.start = tuple(np.subtract((GreedyPath.Alto,GreedyPath.Ancho),startPoint))
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



    #obtain the adjacent valid positions to a given position
    def adjacentPositions(self,position):
        adjacent = []
        adjacent.append(((tuple(np.subtract(position,(GreedyPath.verticalStep,0)))),"up"))
        adjacent.append(((tuple(np.add(position,(GreedyPath.verticalStep,0)))),"down"))
        adjacent.append(((tuple(np.subtract(position,(0,GreedyPath.horizontalStep)))),"left"))
        adjacent.append(((tuple(np.add(position,(0,GreedyPath.horizontalStep)))),"right"))


        ind = 0
        while ind < len(adjacent):
            if adjacent[ind][0] not in GreedyPath.validPositions:
                adjacent.remove(adjacent[ind])
                ind-=1
            ind+=1

        return adjacent


    #check if the actual position is the objective
    def CheckObjective(self):
        return (self.actualPosition == self.objective)

    def calcDistanceToObjective(self,position):
        difference = np.subtract(self.objective,position)
        distance = difference[0]**2 + difference[1]**2
        return distance


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
            adjacents = self.adjacentPositions(self.actualPosition)
            if len(adjacents) != 0:
                minDistance = math.inf
                minPosition = None
                for pos in adjacents:
                    dist = self.calcDistanceToObjective(pos[0])
                    if  dist < minDistance:
                        minDistance = dist
                        minPosition = pos

                self.actualPosition = minPosition[0]
                GreedyPath.validPositions.remove(self.actualPosition)
                self.directions.append(minPosition[1])
                self.actualPath.append(minPosition[0])


            else:
                #check if the path is not void (we aren't in the start)
                if self.actualPath:
                    self.actualPath.pop()

                    #"take one step back"
                    #(change position to the last position in the path)
                    if self.actualPath:
                        self.actualPosition = self.actualPath[-1]

                    #if our actualPath is empty
                    #we ran out of options
                    else:
                        return -1

                #remove the last direction taken
                if self.directions:
                    self.directions.pop()

            return 0

        #if we are in our objective
        else:
            print("Objective found")
            print("Path:")
            for action in self.directions:
                print(action)

            return 1


