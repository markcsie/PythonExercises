# -*- coding: UTF-8 -*-

# for py2exe
import sys
sys.path.append("DLLs")

# for double-clicking the script to execute the program, needed to be changed for different users
sys.path.append(r"C:\Users\MarkKC_Ma\Desktop\KoanSDK\DLLs")
sys.path.append(r"C:\Users\MarkKC_Ma\Desktop\KoanSDK")

import koan
from Widgets.button import TextButton
from Widgets.window import Window
from Widgets.panel import Canvas
import Tetris

from Widgets import color

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

CANVAS_WIDTH = WINDOW_WIDTH / 4
GRID_LENGTH = CANVAS_WIDTH / Tetris.WIDTH
CANVAS_HEIGHT = GRID_LENGTH * Tetris.HEIGHT

# Canvas for the animation of the tetris bricks
class TetrisCanvas(Canvas):
    def __init__(self, parent, tetris):
        Canvas.__init__(self, parent)
        self.__tetris = tetris
        
        # Pre-load the brick textures
        self._blueBrickTexture = self.parent.imageTextureManager.GetTexture(r'Images\BlueBrick.jpg')
        self._darkblueBrickTexture = self.parent.imageTextureManager.GetTexture(r'Images\DarkblueBrick.jpg')
        self._greenBrickTexture = self.parent.imageTextureManager.GetTexture(r'Images\GreenBrick.jpg')
        self._orangeBrickTexture = self.parent.imageTextureManager.GetTexture(r'Images\OrangeBrick.jpg')
        self._purpleBrickTexture = self.parent.imageTextureManager.GetTexture(r'Images\PurpleBrick.jpg')
        self._redBrickTexture = self.parent.imageTextureManager.GetTexture(r'Images\RedBrick.jpg')
        self._yellowBrickTexture = self.parent.imageTextureManager.GetTexture(r'Images\YellowBrick.jpg')
        
        self._backgroundBrickTexture = self.parent.imageTextureManager.GetTexture(r'Images\BackgroundBrick.jpg')
           
        
    def onDraw(self, render):
        # Draw background bricks
        render.SetTexture(self._backgroundBrickTexture)
        for i in range(20):
            for j in range(10):
                if self.__tetris.occupancyMap[i][j + 1] == 0:
                    tempTop = i * GRID_LENGTH
                    tempLeft = j * GRID_LENGTH
                    render.DrawRect(tempLeft, tempTop, tempLeft + GRID_LENGTH, tempTop + GRID_LENGTH)

        # Draw current moving brick
        brickTexture = self.parent.imageTextureManager.GetTexture(self.__tetris.currentBrick.image)
        render.SetTexture(brickTexture)
        for i in range(4):
            for j in range(4):
                if self.__tetris.currentBrick.imageMap[i][j] == 1:
                    tempTop = (self.__tetris.currentBrick.top + i) * GRID_LENGTH
                    tempLeft = (self.__tetris.currentBrick.left + j) * GRID_LENGTH
                    render.DrawRect(tempLeft, tempTop, tempLeft + GRID_LENGTH, tempTop + GRID_LENGTH)
        
        # Draw bricks dropped
        for i in range(20):
            for j in range(10):
                if self.__tetris.occupancyMap[i][j + 1] == 1:
                    
                    if self.__tetris.colorMap[i][j + 1] == 0:
                        render.SetTexture(self._blueBrickTexture)
                    elif self.__tetris.colorMap[i][j + 1] == 1:
                        render.SetTexture(self._darkblueBrickTexture)
                    elif self.__tetris.colorMap[i][j + 1] == 2:
                        render.SetTexture(self._greenBrickTexture)
                    elif self.__tetris.colorMap[i][j + 1] == 3:
                        render.SetTexture(self._orangeBrickTexture)
                    elif self.__tetris.colorMap[i][j + 1] == 4:
                        render.SetTexture(self._purpleBrickTexture)
                    elif self.__tetris.colorMap[i][j + 1] == 5:
                        render.SetTexture(self._redBrickTexture)
                    elif self.__tetris.colorMap[i][j + 1] == 6:
                        render.SetTexture(self._yellowBrickTexture)
                    
                    tempTop = i * GRID_LENGTH
                    tempLeft = j * GRID_LENGTH                
                    
                    render.DrawRect(tempLeft, tempTop, tempLeft + GRID_LENGTH, tempTop + GRID_LENGTH)
                    
# Main window for displaying the player information
class TetrisWindow(Window):
    def __init__(self):
        Window.__init__(self)
               
        self.create(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, caption=True, resize=False)
        
        self._initTetris()
               
        # Button for 'Start' and 'Tetris.PAUSE'
        self._triggerButton = TextButton(self)
        self._triggerButton.rect = (0, 0, 50, 30)
        self._triggerButton.fontColor = color.red
        self._triggerButton.text = 'Start'
        self._triggerButton.background = r'Images\Button.jpg'     
        self.autoRemove(self._triggerButton.bind('Click', self._onTrigger))
        
        # Button for 'Restart'
        self._restartButton = TextButton(self)
        self._restartButton.rect = (60, 0, 50, 30)
        self._restartButton.fontColor = color.red
        self._restartButton.text = 'Restart'
        self._restartButton.background = r'Images\Button.jpg' 
        self.autoRemove(self._restartButton.bind('Click', self._onRestart))
        
        self._backgroundTexture = self.imageTextureManager.GetTexture(r'Images\Background.jpg')
        self._backgroundEffect = self.effectManager.GetEffect(r'backgroundEffects\Background.fx')
        
        self._fontEffect = self.effectManager.GetEffect(r'fontEffects\font.fx')
        
    # Initialization     
    def _initTetris(self):
        self._gameState = Tetris.PAUSE
        
        self._tetrisP1 = Tetris.Tetris('P1')  
        self._tetrisP1.setBricks()
        self._canvasP1 = TetrisCanvas(self, self._tetrisP1)
        self._canvasP1.rect = (WINDOW_WIDTH / 20, WINDOW_HEIGHT / 6, CANVAS_WIDTH, CANVAS_HEIGHT)
        # Create a new animation attribute for tetrisP1
        self._tetrisP1.animation = None
        
        self._tetrisP2 = Tetris.Tetris('P2')  
        self._tetrisP2.setBricks()
        self._canvasP2 = TetrisCanvas(self, self._tetrisP2)
        self._canvasP2.rect = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 6, CANVAS_WIDTH, CANVAS_HEIGHT)
        # Create a new animation attribute for tetrisP2
        self._tetrisP2.animation = None
    
    # Callback function for key events
    def onKey(self, key):
        if self._gameState != Tetris.OVER and self._gameState != Tetris.PAUSE:
            
            self._controlP1(key)
            if not Tetris.SINGLE_MODE:
                self._controlP2(key)
        
        return super(TetrisWindow, self).onKey(key)
            
    # Key controls for player1
    def _controlP1(self, key):
        if key == 'UP':
            self._tetrisP1.currentBrick.rotate(1)
            if self._tetrisP1.isOccupied('ROTATE') == True:
                self._tetrisP1.currentBrick.rotate(-1)
            
        elif key == 'DOWN':
            if self._tetrisP1.isOccupied('DOWN') == False:
                self._tetrisP1.currentBrick.top += 1
            else:
                returnStatus = self._tetrisP1.checkElimination()
                self._gameState = returnStatus['GameState']
                self._tetrisP2.levelChanged = returnStatus['LevelChanged']
                
        elif key == 'LEFT':
            if self._tetrisP1.isOccupied('LEFT') == False:
                self._tetrisP1.currentBrick.left -= 1
            
        elif key == 'RIGHT':
            if self._tetrisP1.isOccupied('RIGHT') == False:
                self._tetrisP1.currentBrick.left += 1
                
        elif key == ' ':
            while self._tetrisP1.isOccupied('DOWN') == False:
                self._tetrisP1.currentBrick.top += 1
            
            returnStatus = self._tetrisP1.checkElimination()
            self._gameState = returnStatus['GameState']
            self._tetrisP2.levelChanged = returnStatus['LevelChanged']
            
        self._canvasP1.setDirty()
    
    # Key controls for player2    
    def _controlP2(self, key):
        if key == 'w':
            self._tetrisP2.currentBrick.rotate(1)
            if self._tetrisP2.isOccupied('ROTATE') == True:
                self._tetrisP2.currentBrick.rotate(-1)
            
        elif key == 's':
            if self._tetrisP2.isOccupied('DOWN') == False:
                self._tetrisP2.currentBrick.top += 1
            else:
                returnStatus = self._tetrisP2.checkElimination()
                self._gameState = returnStatus['GameState']
                self._tetrisP1.levelChanged = returnStatus['LevelChanged']
                
        elif key == 'a':
            if self._tetrisP2.isOccupied('LEFT') == False:
                self._tetrisP2.currentBrick.left -= 1
            
        elif key == 'd':
            if self._tetrisP2.isOccupied('RIGHT') == False:
                self._tetrisP2.currentBrick.left += 1
                
        elif key == '`':
            while self._tetrisP2.isOccupied('DOWN') == False:
                self._tetrisP2.currentBrick.top += 1
            
            returnStatus = self._tetrisP2.checkElimination()
            self._gameState = returnStatus['GameState']
            self._tetrisP1.levelChanged = returnStatus['LevelChanged']
            
        self._canvasP2.setDirty()
         
    # Callback function for button 'Start' and 'Pause'       
    def _onTrigger(self):
        if self._gameState == Tetris.PAUSE:
            self._gameState = Tetris.RUNNING
            self._triggerButton.text = 'PAUSE'
            self._restartButton.fontColor = color.black
            
            self._tetrisP1.animation = koan.anim.IntervalExecute(3.0 / (2 + self._tetrisP1.level), self._onTimer, self._tetrisP1, self._canvasP1)
            if not Tetris.SINGLE_MODE:
                self._tetrisP2.animation = koan.anim.IntervalExecute(3.0 / (2 + self._tetrisP2.level), self._onTimer, self._tetrisP2, self._canvasP2)
        
        elif self._gameState == Tetris.RUNNING:
            self._gameState = Tetris.PAUSE
            self._restartButton.fontColor = color.red 
            self._triggerButton.text = 'Start'
            
            self._tetrisP1.animation.remove()
            if not Tetris.SINGLE_MODE:
                self._tetrisP2.animation.remove() 
                
    # Callback function for button 'Restart'       
    def _onRestart(self):
        if self._gameState == Tetris.PAUSE or self._gameState == Tetris.OVER:
            self._triggerButton.fontColor = color.red
            
            self._triggerButton.text = 'Start'
            
            if self._tetrisP1.animation:
                self._tetrisP1.animation.remove()
            
            if self._tetrisP2.animation:
                self._tetrisP2.animation.remove()
            
            self._initTetris()
            
            
    # Callback function for refreshing players' info and brick's location
    def _onTimer(self, tetris, canvas):
        # Level up, re-register the timer interval to change the speed of the brick 
        if tetris.levelChanged:
            tetris.level += 1
            tetris.levelChanged = False
            tetris.animation.remove()
            tetris.animation = koan.anim.IntervalExecute(3.0 / (2 + tetris.level), self._onTimer, tetris, canvas)
        
        # Check if the game is over
        if self._gameState == Tetris.OVER:
            self._restartButton.fontColor = color.red
            self._triggerButton.fontColor = color.black
            tetris.animation.remove()
            return
        
        # Check if the game is paused
        if self._gameState == Tetris.PAUSE:
            return
        
        if tetris.isOccupied('DOWN') == False:
            tetris.currentBrick.top += 1
        else:
            returnStatus = tetris.checkElimination()
            self._gameState = returnStatus['GameState']
            levelChanged = returnStatus['LevelChanged']
            
            if tetris.name == 'P1':
                self._tetrisP2.levelChanged = levelChanged  
            elif tetris.name == 'P2':
                self._tetrisP1.levelChanged = levelChanged

        tetris.time += 3.0 / (2 + tetris.level)
        
        self.setDirty()
        canvas.setDirty()
        
            
    def onDraw(self, render):
        render.Clear(*color.translucent)
        
        # Background color
        render.SetColor(*color.green)
        render.SetTexture(self._backgroundTexture)
        render.PushEffect(self._backgroundEffect)
        render.DrawRect(0, 0, self.right, self.bottom)
        render.PopEffect()
        
        self._drawGameState(render)
          
        self._drawPlayerInfo(render, self._tetrisP1, left=280)
        self._drawNextBrick(render, self._tetrisP1, left=300)
        
        self._drawNextBrick(render, self._tetrisP2, left=670)
        self._drawPlayerInfo(render, self._tetrisP2, left=650)
    
    def _drawGameState(self, render):
        render.SetColor(*color.white)
        render.PushEffect(self._fontEffect)
        
        if self._gameState == Tetris.OVER:
            if self._tetrisP1.gameOver and self._tetrisP2.gameOver:
                render.DrawText('Draw!!! Press "Restart" Button to restart', (200, 45), 20, color.white)
            elif self._tetrisP1.gameOver:
                render.DrawText('P2 Wins!!! Press "Restart" Button to restart', (200, 45), 20, color.white)
            elif self._tetrisP2.gameOver:
                render.DrawText('P1 Wins!!! Press "Restart" Button to restart', (200, 45), 20, color.white)             
        elif self._gameState == Tetris.PAUSE:
            render.DrawText('Press "Start" Button to start', (200, 45), 20, color.white)
        else:
            render.DrawText('Time: ' + str(int(self._tetrisP1.time)), (330, 45), 20, color.white)
            
        render.PopEffect()
        
    def _drawPlayerInfo(self, render, tetris, left=280, top=80, size=20):
        render.SetColor(*color.white)
        
        render.PushEffect(self._fontEffect)
        render.DrawText('Level: ' + str(tetris.level), (left, top), size, color.white)
        render.DrawText('Lines: ' + str(tetris.lines), (left, top + 25), size, color.white)
        render.DrawText('Score: ' + str(tetris.score), (left, top + 50), size, color.white)
        render.DrawText('Next:', (left, top + 100), size, color.white)
        render.PopEffect()
        
    def _drawNextBrick(self, render, tetris, left=300, top=220):
        brickTexture = self.imageTextureManager.GetTexture(tetris.nextBrick.image)
        render.SetTexture(brickTexture)
        for i in range(4):
            for j in range(4):
                if tetris.nextBrick.imageMap[i][j] == 1:
                    tempTop = top + i * GRID_LENGTH
                    tempLeft = left + j * GRID_LENGTH
                    
                    render.DrawRect(tempLeft, tempTop, tempLeft + GRID_LENGTH, tempTop + GRID_LENGTH)
                    
    def close(self):
        if self._tetrisP1.animation:
            self._tetrisP1.animation.remove()
            self._tetrisP1.animation = None
        
        if self._tetrisP2.animation:
            self._tetrisP2.animation.remove()
            self._tetrisP2.animation = None
                
        print '[TetrisWindow::close] Window closed'
        super(TetrisWindow, self).close()
 
if __name__ == '__main__':
    try:
        playerNum = int(raw_input('Enter "1" for Single-Mode "2" for two players Battle-Mode\n'))

        if playerNum < 2:
            Tetris.SINGLE_MODE = True
        elif playerNum >= 2:
            Tetris.SINGLE_MODE = False
    except NameError:
        print 'Wrong Input!!!'
    else:
        koan.init()
        w = TetrisWindow()
        w.show()
        koan.run(1)
        koan.final()
    



