import collections
import numpy as np
from queue import PriorityQueue



class IDDFSPath:

    Alto = 0
    Ancho = 0
    y = 1
    validPositions = None

    verticalStep = None
    horizontalStep = None

    def __init__(self, start, objective, alto, ancho, size, ValidPositions):

        IDDFSPath.Alto = alto
        IDDFSPath.Ancho = ancho
        IDDFSPath.y = size
        IDDFSPath.validPositions = ValidPositions

        IDDFSPath.horizontalStep = IDDFSPath.Ancho/IDDFSPath.y
        IDDFSPath.verticalStep = IDDFSPath.Alto/IDDFSPath.y

        #adjust the starting point to the coordinate system
        self.start = start
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

        #Initialize our max depth
        self.maxDepth = 0

        #and use an internal list of validPositions
        self.validPositions = IDDFSPath.validPositions.copy()

        self.positionToRestore = collections.deque()
        self.deadEnd = []


    #check if the agent can move up
    def tryUp(self):

        #Calculate the next move (take a vertical step up)
        nextMove = tuple(np.subtract(self.actualPosition,(IDDFSPath.verticalStep,0)))

        #Check if this step is in the valid positions
        validMove = nextMove in self.validPositions

        #check if the agent already went through that point
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack


    #check if the agent can move down
    def tryDown(self):
        nextMove = tuple(np.add(self.actualPosition,(IDDFSPath.verticalStep,0)))

        validMove = nextMove in self.validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    #check if the agent can move left
    def tryLeft(self):
        nextMove = tuple(np.subtract(self.actualPosition,(0,IDDFSPath.horizontalStep)))

        validMove =  nextMove in self.validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    #check if the agent can move right
    def tryRight(self):
        nextMove = tuple(np.add(self.actualPosition,(0,IDDFSPath.horizontalStep)))

        validMove = nextMove in self.validPositions
        Backtrack = nextMove in self.actualPath

        return validMove and not Backtrack

    #check if the actual position is the objective
    def CheckObjective(self):
        return (self.actualPosition == self.objective)


    #obtain the adjacent valid positions to a given position
    def adjacentPositions(self,position):
        adjacent = []
        adjacent.append(tuple(np.subtract(position,(IDDFSPath.verticalStep,0))))
        adjacent.append(tuple(np.add(position,(IDDFSPath.verticalStep,0))))
        adjacent.append(tuple(np.subtract(position,(0,IDDFSPath.horizontalStep))))
        adjacent.append(tuple(np.add(position,(0,IDDFSPath.horizontalStep))))

        for possible in adjacent:
            if possible not in IDDFSPath.validPositions:
                adjacent.remove(possible)

        return adjacent


    #remove deadEnds that are adjacent to another deadEnd
    def checkDeadEnd(self,deadEnd):
        possibleMoves = self.adjacentPositions(deadEnd)

        for move in possibleMoves:
            if move in self.deadEnd:
                self.deadEnd.remove(move)
                self.positionToRestore.append(move)





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

            #check if we have reached the maxDepth
            #if so, we can move normaly
            if len(self.actualPath) < self.maxDepth:

                #check if it can move (priorizes up > left > down > right)
                if self.tryUp():

                    #if it can move, calculate the new position
                    self.actualPosition = tuple(np.subtract(self.actualPosition,(IDDFSPath.verticalStep,0)))

                    #append the new direction
                    self.directions.append("up")

                    #add the new position to our path
                    self.actualPath.append(self.actualPosition)



                elif self.tryLeft():
                    self.actualPosition = tuple(np.subtract(self.actualPosition,(0,IDDFSPath.horizontalStep)))
                    self.directions.append("left")
                    self.actualPath.append(self.actualPosition)

                elif self.tryDown():
                    self.actualPosition = tuple(np.add(self.actualPosition,(IDDFSPath.verticalStep,0)))
                    self.directions.append("down")
                    self.actualPath.append(self.actualPosition)

                elif self.tryRight():
                    self.actualPosition = tuple(np.add(self.actualPosition,(0,IDDFSPath.horizontalStep)))
                    self.directions.append("right")
                    self.actualPath.append(self.actualPosition)

                #if it cannot move
                else:
                    #check if the path is greater than one (we aren't in the start)
                    if len(self.actualPath) >= 1:


                        #restore the positions to restore
                        while self.positionToRestore:
                            self.validPositions.append(self.positionToRestore.popleft())

                        #if so, remove the last action and take that
                        #position out of our valid positions
                        #and mark the position to restore
                        posToRestore = self.actualPath.pop()


                        #if we are not in the start
                        if len(self.actualPath) > 1:

                            #if positionToRestore is not empty
                            if not self.positionToRestore:

                                #mark posToRestore as a dead end
                                self.deadEnd.append(posToRestore)

                            #if we don't have positions to restore
                            else:

                                #add posToRestore to our list of
                                #positions to restore
                                self.positionToRestore.append(posToRestore)


                        #if we have dead ends
                        if len(self.deadEnd) > 0:

                            #check if those can be restored
                            self.checkDeadEnd(self.deadEnd[-1])

                        #remove posToRestore from validPositions
                        self.validPositions.remove(posToRestore)

                        #if actualPath is not empty
                        if self.actualPath:
                            #"take one step back"
                            #(change position to the last position in the path)
                            self.actualPosition = self.actualPath[-1]

                        #if our actualPath is empty
                        #we ran out of options
                        else:
                            if self.positionToRestore:
                                self.positionToRestore.clear()

                            self.deadEnd.clear()
                            self.actualPath.append(self.start)
                            self.maxDepth +=1
                            self.validPositions = IDDFSPath.validPositions.copy()
                            return 0

                    #remove the last direction taken
                    if self.directions:
                        self.directions.pop()


                return 0


            #backtrack (act as if we found a wall)
            else:
                #check if the path is greater than one (we aren't in the start)
                    if len(self.actualPath) >= 1:
                        #if so, remove the last action and take that
                        #position out of our valid positions
                        #and mark the position to restore
                        posToRestore = self.actualPath.pop()

                        if self.maxDepth > 3:
                            if len(self.actualPath) > self.maxDepth-2:
                                self.positionToRestore.append(posToRestore)

                        self.validPositions.remove(posToRestore)

                        #if actualPath is not empty
                        if self.actualPath:
                            #"take one step back"
                            #(change position to the last position in the path)
                            self.actualPosition = self.actualPath[-1]

                        #if our actualPath is empty
                        #we ran out of options
                        else:
                            if self.positionToRestore:
                                self.positionToRestore.clear()
                            self.actualPath.append(self.start)
                            self.maxDepth +=1
                            self.validPositions = IDDFSPath.validPositions.copy()
                            return 0

                    #if our path is one
                    else:
                        #if our actualPath is lenght one
                        #we ran out of options
                        self.maxDepth +=1
                        self.deadEnd.clear()
                        self.validPositions = validPositions.copy()
                        return 0

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

