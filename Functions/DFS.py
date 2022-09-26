import collections
import numpy as np
from queue import PriorityQueue

class DFSPath:

    Alto = 0
    Ancho = 0
    y = 1
    validPositions = None

    verticalStep = None
    horizontalStep = None

    #The agent need a starting point and an objective
    def __init__(self,start,objective, alto, ancho, size, ValidPositions):

        DFSPath.Alto = alto
        DFSPath.Ancho = ancho
        DFSPath.y = size
        DFSPath.validPositions = ValidPositions

        DFSPath.horizontalStep = DFSPath.Ancho/DFSPath.y
        DFSPath.verticalStep = DFSPath.Alto/DFSPath.y

        #adjust the starting point to the coordinate system
        self.start = tuple(np.subtract((DFSPath.Alto,DFSPath.Ancho),start))
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

        self.totalPath = []
        self.totalDirections = []


    #check if the agent can move up
    def tryUp(self):

        #Calculate the next move (take a vertical step up)
        nextMove = tuple(np.subtract(self.actualPosition,(DFSPath.verticalStep,0)))

        #Check if this step is in the valid positions
        validMove = nextMove in DFSPath.validPositions

        #check if the agent already went through that point
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack


    #check if the agent can move down
    def tryDown(self):
        nextMove = tuple(np.add(self.actualPosition,(DFSPath.verticalStep,0)))

        validMove = nextMove in DFSPath.validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    #check if the agent can move left
    def tryLeft(self):
        nextMove = tuple(np.subtract(self.actualPosition,(0,DFSPath.horizontalStep)))

        validMove =  nextMove in DFSPath.validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    #check if the agent can move right
    def tryRight(self):
        nextMove = tuple(np.add(self.actualPosition,(0,DFSPath.horizontalStep)))

        validMove = nextMove in DFSPath.validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    #check if the actual position is the objective
    def CheckObjective(self):
        return (self.actualPosition == self.objective)

    def oppositeDirection(self,direction):
        if direction == "up":
            return "down"
        elif direction == "down":
            return "up"
        elif direction == "left":
            return "right"
        elif direction == "right":
            return "left"


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
                self.actualPosition = tuple(np.subtract(self.actualPosition,(DFSPath.verticalStep,0)))

                #append the new direction
                self.directions.append("up")
                self.totalDirections.append("up")

                #add the new position to our path
                self.actualPath.append(self.actualPosition)
                self.totalPath.append(self.actualPosition)

            elif self.tryLeft():
                self.actualPosition = tuple(np.subtract(self.actualPosition,(0,DFSPath.horizontalStep)))
                self.directions.append("left")
                self.totalDirections.append("left")
                self.actualPath.append(self.actualPosition)
                self.totalPath.append(self.actualPosition)

            elif self.tryDown():
                self.actualPosition = tuple(np.add(self.actualPosition,(DFSPath.verticalStep,0)))
                self.directions.append("down")
                self.totalDirections.append("down")
                self.actualPath.append(self.actualPosition)
                self.totalPath.append(self.actualPosition)

            elif self.tryRight():
                self.actualPosition = tuple(np.add(self.actualPosition,(0,DFSPath.horizontalStep)))
                self.directions.append("right")
                self.totalDirections.append("right")
                self.actualPath.append(self.actualPosition)
                self.totalPath.append(self.actualPosition)

            #if it cannot move
            else:
                #check if the path is not void (we aren't in the start)
                if self.actualPath:

                    #if so, remove the last action and take that
                    #position out of our valid positions
                    DFSPath.validPositions.remove(self.actualPath.pop())

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
                    direction = self.directions.pop()
                    self.totalDirections.append(self.oppositeDirection(direction))

            return 0


        #if we are in out objective
        else:
            print("Objective found")
            print("Path:")
            for action in self.directions:
                print(action)

            print("\n \n \n")
            print("Total path traversed:")
            for action in self.totalDirections:
                print(action)

            return 1




