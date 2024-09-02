import pygame
import math
import random
from collections import deque
locations = deque()
z = random.randint(1,5)
locations.appendleft((0, z))
locations.appendleft((1, z))



class Player:
    
    orientation = 0
    length = 0
    cantgo = 0
    foodplace = ((random.randint(4,5),random.randint(4,5)))
    distright = 0
    diststraight = 0
    distleft = 0
    score = 0
    curplace = ((0,0))
    static_states = 0

    def __init__(self):
        self.length = 2
        self.orientation = 3
        self.cantgo = 9
        self.foodplace = ((random.randint(4,5),random.randint(4,5)))

    def move(self, gamegrid):
        global locations
        self.static_states += 1
        trimsize = True
        gridsize = len(gamegrid)
        def newfood():
            zx = random.randint(0,gridsize-1)
            zy = random.randint(0,gridsize-1)
            test = ((zx,zy))
            while test in locations:
                zx = random.randint(0,gridsize-1)
                zy = random.randint(0,gridsize-1)
                test = ((zx,zy))
            return test

        #logic to end the game
        nextplace = 0
        curplace = locations[0]
        

        if self.orientation ==3:
            nextplace = ((curplace[0] + 1, curplace[1]))
        if self.orientation ==6:
            nextplace = ((curplace[0], curplace[1] + 1))
        if self.orientation ==9:
            nextplace = ((curplace[0] - 1, curplace[1]))
        if self.orientation ==12:
            nextplace = ((curplace[0], curplace[1] - 1))
        
        self.curplace = nextplace
        if nextplace[0] >= gridsize or nextplace[0] < 0:
            return [[-10]],0
        if nextplace[1] >= gridsize or nextplace[1] < 0:
            return [[-10]],0
        
        for location in locations:
            if nextplace == location:
                    return [[-10]],0
        
        locations.appendleft(nextplace)
        i = 0
        for location in locations:
            if location == nextplace:
                gamegrid[location[0]][location[1]] = 2
            else:
                gamegrid[location[0]][location[1]] = 2 + (47 - i)
            i += 1

           

        if nextplace[0] == self.foodplace[0] and nextplace[1] == self.foodplace[1]:
            self.foodplace = newfood()
            trimsize = False
            self.score += 1
            self.static_states = 0
            self.length += 1


        if trimsize:
            deletethis = locations.pop()
            gamegrid[deletethis[0]][deletethis[1]] = 0
        
        gamegrid[self.foodplace[0]][self.foodplace[1]] = 1

        if self.orientation == 12:  # Moving Up
        # Calculate distance to the left
            self.distleft = nextplace[0] + 1
            for val in range(nextplace[0]):
                if gamegrid[val][nextplace[1]] == 1:
                    self.distleft = nextplace[0] - val
                    break

            # Calculate distance to the right
            self.distright = gridsize - nextplace[0]
            for val in range(gridsize - nextplace[0] - 1):
                if nextplace[0] + 1 + val < gridsize and gamegrid[nextplace[0] + 1 + val][nextplace[1]] == 1:
                    self.distright = val + 1
                    break

            # Calculate distance straight
            self.diststraight = nextplace[1] + 1
            for val in range(nextplace[1]):
                if nextplace[1] - (val + 1) >= 0 and gamegrid[nextplace[0]][nextplace[1] - (val + 1)] == 1:
                    self.diststraight = val + 1
                    break

        elif self.orientation == 6:  # Moving Right
            # Calculate distance to the right
            self.distright = nextplace[0] + 1
            for val in range(nextplace[0]):
                if gamegrid[val][nextplace[1]] == 1:
                    self.distright = nextplace[0] - val
                    break

            # Calculate distance to the left
            self.distleft = gridsize - nextplace[0]
            for val in range(gridsize - nextplace[0] - 1):
                if nextplace[0] + 1 + val < gridsize and gamegrid[nextplace[0] + 1 + val][nextplace[1]] == 1:
                    self.distleft = val + 1
                    break

            # Calculate distance straight
            self.diststraight = gridsize - nextplace[1]
            for val in range(gridsize - nextplace[1]):
                if nextplace[1] + val + 1 < gridsize and gamegrid[nextplace[0]][nextplace[1] + val + 1] == 1:
                    self.diststraight = val + 1
                    break

        elif self.orientation == 3:  # Moving Down
            # Calculate distance to the left
            self.distleft = nextplace[1] + 1
            for val in range(nextplace[1]):
                if nextplace[1] - (val + 1) >= 0 and gamegrid[nextplace[0]][nextplace[1] - (val + 1)] == 1:
                    self.distleft = val + 1
                    break

            # Calculate distance to the right
            self.distright = gridsize - nextplace[1]
            for val in range(gridsize - nextplace[1] - 1):
                if nextplace[1] + val + 1 < gridsize and gamegrid[nextplace[0]][nextplace[1] + val + 1] == 1:
                    self.distright = val + 1
                    break

            # Calculate distance straight
            self.diststraight = gridsize - nextplace[0]
            for val in range(gridsize - nextplace[0] - 1):
                if nextplace[0] + 1 + val < gridsize and gamegrid[nextplace[0] + 1 + val][nextplace[1]] == 1:
                    self.diststraight = val + 1
                    break

        elif self.orientation == 9:  # Moving Left
            # Calculate distance to the right
            self.distright = nextplace[1] + 1
            for val in range(nextplace[1]):
                if nextplace[1] - (val + 1) >= 0 and gamegrid[nextplace[0]][nextplace[1] - (val + 1)] == 1:
                    self.distright = val + 1
                    break

            # Calculate distance to the left
            self.distleft = gridsize - nextplace[1]
            for val in range(gridsize - nextplace[1] - 1):
                if nextplace[1] + val + 1 < gridsize and gamegrid[nextplace[0]][nextplace[1] + val + 1] == 1:
                    self.distleft = val + 1
                    break

            # Calculate distance straight
            self.diststraight = nextplace[0] + 1
            for val in range(nextplace[0]):
                if nextplace[0] - val - 1 >= 0 and gamegrid[nextplace[0] - val - 1][nextplace[1]] == 1:
                    self.diststraight = val + 1
                    break
            
        
        return gamegrid, self.score
        



    def updatedir(self, dir):
        if dir ==0:
            return
        
        if dir == self.cantgo:
            return
        

        self.orientation = dir

        self.cantgo = 12 - dir
        if dir == 6:
            self.cantgo = 12
        if dir == 12:
            self.cantgo = 6

        
        


    def reset(self):
        global locations
        self.orientation = 3
        self.cantgo = 9
        self.score = 0
        locations.clear()
        z = random.randint(1,5)
        locations.appendleft((0, z))
        locations.appendleft((1, z))

        
        
