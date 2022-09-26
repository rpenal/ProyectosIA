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


    #Calculate manhattan distance from a point to the objective
    def calcDistanceToObjective(self,position):
        difference = np.subtract(self.objective,position)
        distance = abs(difference[0]) + abs(difference[1])
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

            #take the adjacent valid positions
            adjacents = self.adjacentPositions(self.actualPosition)

            #if the list isn't void (there's at least one
            #adjacent valid position)
            if len(adjacents) != 0:

                #initialize a variable to store minimum distance
                #and the position corresponding to it
                minDistance = math.inf
                minPosition = None

                #for each position
                for pos in adjacents:

                    #if the manhattan distance from it to the objective
                    #is lesser than our current minimum position
                    dist = self.calcDistanceToObjective(pos[0])
                    if  dist < minDistance:

                        #set this position and its distance as minimums
                        minDistance = dist
                        minPosition = pos

                #change the actual position to the position with the minimum distance
                self.actualPosition = minPosition[0]

                #remove our actual position from the list of valid positions
                #to avoid loops
                GreedyPath.validPositions.remove(self.actualPosition)

                #append the direction we took to the direction list
                self.directions.append(minPosition[1])

                #and the position we are to our path
                self.actualPath.append(minPosition[0])


            #if there's no adjacent valid position
            else:
                #check if the path is not void (we aren't in the start)
                if self.actualPath:

                    #take out the last position
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


