import Brick

import random

# State of the Tetris game
PAUSE = 0
RUNNING = 1
OVER = 2

HEIGHT = 20
WIDTH = 10

HEIGHT_WITH_BORDER = HEIGHT + 1
WIDTH_WITH_BORDER = WIDTH + 2

SINGLE_MODE = True

# Abstraction of the Tetris game
class Tetris(object):
    def __init__(self, name):
        # Player Name
        self.name = name
            
        self.lines = 0
        self.score = 0
        self.time = 0
        
        self.level = 1
        self.levelChanged = False
        
        self.__linesCount = 0  
        
        # A 2D-map indicating if the cell is occupied
        self.occupancyMap = [[0] * WIDTH_WITH_BORDER for i in xrange(HEIGHT_WITH_BORDER)]
        for i in range(HEIGHT_WITH_BORDER):
            for j in range(WIDTH_WITH_BORDER):
                if j == 0 or j == WIDTH_WITH_BORDER - 1 or i == HEIGHT_WITH_BORDER - 1:
                    self.occupancyMap[i][j] = 1
                    
        # A 2D-map indicating each cell's brick color
        self.colorMap = [[0] * WIDTH_WITH_BORDER for i in xrange(HEIGHT_WITH_BORDER)]
         
        # Game State
        self.gameOver  = False
            
        self._newNextBrick()
        
        
    def setBricks(self):
        self.currentBrick = self.nextBrick
        self.currentBrick.left = WIDTH / 2 - 1
        self.currentBrick.top = 0
        
        self._newNextBrick()
    
    # Generate a new brick with random shape and color        
    def _newNextBrick(self):
        which = random.randint(0, 6)
        if which == 0:
            self.nextBrick = Brick.BrickSquare()
        elif which == 1:
            self.nextBrick = Brick.BrickLine()
        elif which == 2:
            self.nextBrick = Brick.BrickL()
        elif which == 3:
            self.nextBrick = Brick.BrickMirrorL()
        elif which == 4:
            self.nextBrick = Brick.BrickZ()
        elif which == 5:
            self.nextBrick = Brick.BrickMirrorZ()  
        elif which == 6:
            self.nextBrick = Brick.BrickOther()
            
        self.nextBrick.imageNum = random.randint(0, 6)
        if self.nextBrick.imageNum == 0:
            self.nextBrick.image = r'Images\BlueBrick.jpg'
        elif self.nextBrick.imageNum == 1:
            self.nextBrick.image = r'Images\DarkblueBrick.jpg'
        elif self.nextBrick.imageNum == 2:
            self.nextBrick.image = r'Images\GreenBrick.jpg'
        elif self.nextBrick.imageNum == 3:
            self.nextBrick.image = r'Images\OrangeBrick.jpg'
        elif self.nextBrick.imageNum == 4:
            self.nextBrick.image = r'Images\PurpleBrick.jpg'
        elif self.nextBrick.imageNum == 5:
            self.nextBrick.image = r'Images\RedBrick.jpg'
        elif self.nextBrick.imageNum == 6:
            self.nextBrick.image = r'Images\YellowBrick.jpg'
        
    # Check if it's occupied on the four directions side        
    def isOccupied(self, direction):
        occupied = False
        for i in range(4):
            for j in range(4):
                if direction == 'DOWN':
                    if (self.currentBrick.imageMap[i][j] and self.occupancyMap[self.currentBrick.top + i + 1][self.currentBrick.left + j + 1]) == 1:
                        occupied = True
                        break
                elif direction == 'LEFT':
                    if (self.currentBrick.imageMap[i][j] and self.occupancyMap[self.currentBrick.top + i][self.currentBrick.left + j]) == 1:
                        occupied = True
                        break
                elif direction == 'RIGHT':
                    if (self.currentBrick.imageMap[i][j] and self.occupancyMap[self.currentBrick.top + i][self.currentBrick.left + j + 2]) == 1:
                        occupied = True
                        break
                elif direction == 'ROTATE':
                    if (self.currentBrick.imageMap[i][j] and self.occupancyMap[self.currentBrick.top + i][self.currentBrick.left + j + 1]) == 1:
                        occupied = True
                        break
        return occupied
            
            
    def checkElimination(self):       
        # Update the map with the current brick 
        for i in range(4):
            for j in range(4):
                if self.currentBrick.imageMap[i][j] == 1:
                    self.colorMap[self.currentBrick.top + i][self.currentBrick.left + j + 1] = self.currentBrick.imageNum
                    self.occupancyMap[self.currentBrick.top + i][self.currentBrick.left + j + 1] = 1
        
        # Check if there are lines formed
        for i in range(self.currentBrick.height):
            flagEliminate = True
            for j in range(WIDTH_WITH_BORDER):
                if self.occupancyMap[self.currentBrick.top + i][j] == 0:
                    flagEliminate = False
                    break
            if flagEliminate:
                bottomLine = self.currentBrick.top + i + 1
                
                self.score += 10
                self.lines += 1
                self.__linesCount += 1
                # Update the map
                for i in reversed(range(1, bottomLine)):
                    self.occupancyMap[i] = list(self.occupancyMap[i - 1])
                    self.colorMap[i] = list(self.colorMap[i - 1])
        
        # Check if the game is over
        gameState = RUNNING
        for j in range(WIDTH):
            if self.occupancyMap[0][j + 1] == 1:
                gameState = OVER
                self.gameOver = True
                break
                
        # Check if it's time to level up
        levelChanged = False
        if self.__linesCount >= 10:
            levelChanged = True
            
            if SINGLE_MODE:
                self.levelChanged = True
                levelChanged = False
                
            self.__linesCount -= 10
            
        # Update the bricks    
        self.setBricks()
        
        return {'GameState': gameState, 'LevelChanged': levelChanged}
    
    
    
    
    
        