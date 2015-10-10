import Tetris
# Abstract base brick class for other concrete brick classes
class BrickBase(object):
    def __init__(self):
              
        self._left = 0
        self._top = 0
        self._width = 0
        self._height = 0
        
        self._rotate = 0
        
        self._imageNum = 0
        self._image = r'Images\BlueBrick.jpg'
         
    # Left Property     
    def getLeft(self):
        return self._left 
    def setLeft(self, left):
        if left < 0: 
            self._left = 0
        elif left + self._width > Tetris.WIDTH:
            self._left = Tetris.WIDTH - self._width
        else:
            self._left = left       
    left = property(getLeft, setLeft)
    
    # Top Property
    def getTop(self):
        return self._top
    def setTop(self, top):
        if top < 0: 
            self._top = 0
        elif top + self._height > Tetris.HEIGHT:
            self._top = Tetris.HEIGHT - self._height
        else:
            self._top = top
    top = property(getTop, setTop)
    
    # Right Property
    @property
    def right(self):
        return self._left + self._width
    
    # Bottom Property
    @property
    def bottom(self):
        return self._top + self._height
    
    # Width Property        
    @property        
    def width(self):
        return self._width
    
    # Height Property
    @property
    def height(self):
        return self._height
    
    # Image Property
    def getImage(self):
        return self._image
    def setImage(self, image):
        self._image = image
    image = property(getImage, setImage)
    
# ----
# |  |
# ----
class BrickSquare(BrickBase):
    def __init__(self):
        BrickBase.__init__(self)
        
        
        self._width = 2
        self._height = 2
        
        # The shape of the brick
        self.imageMap = ((1, 1, 0, 0),
                         (1, 1, 0, 0),
                         (0, 0, 0, 0),
                         (0, 0, 0, 0))
        
    # No need to change the shape 
    def rotate(self, counterclockwise):
        pass

# |
# |
# |   
class BrickLine(BrickBase):
    def __init__(self):
        BrickBase.__init__(self)
             
        self._width = 1
        self._height = 4
        
        # The shape of the brick
        self.imageMap = ((1, 0, 0, 0),
                         (1, 0, 0, 0),
                         (1, 0, 0, 0),
                         (1, 0, 0, 0))
        
    # Change the shape of the brick       
    def rotate(self, counterclockwise):
        temp = self._width
        self._width = self._height
        self._height = temp
        
        self._rotate += counterclockwise;
        if self._rotate == 2:
            self._rotate = 0
        elif self._rotate == -1:
            self._rotate = 1
        
        if self._rotate == 0:
            self.imageMap = ((1, 0, 0, 0),
                             (1, 0, 0, 0),
                             (1, 0, 0, 0),
                             (1, 0, 0, 0))
            
        elif self._rotate == 1:
            self.imageMap = ((1, 1, 1, 1),
                             (0, 0, 0, 0),
                             (0, 0, 0, 0),
                             (0, 0, 0, 0))

# |
# |_         
class BrickL(BrickBase):
    def __init__(self):
        BrickBase.__init__(self)
        
        self._width = 2
        self._height = 3
        
        # The shape of the brick
        self.imageMap = ((1, 0, 0, 0),
                         (1, 0, 0, 0),
                         (1, 1, 0, 0),
                         (0, 0, 0, 0))
        
    # Change the shape of the brick        
    def rotate(self, counterclockwise):
        temp = self._width
        self._width = self._height
        self._height = temp
        
        self._rotate += counterclockwise;
        if self._rotate == 4:
            self._rotate = 0
        elif self._rotate == -1:
            self._rotate = 3
        
        if self._rotate == 0:
            self.imageMap = ((1, 0, 0, 0),
                             (1, 0, 0, 0),
                             (1, 1, 0, 0),
                             (0, 0, 0, 0))
            
        elif self._rotate == 1:
            self.imageMap = ((0, 0, 1, 0),
                             (1, 1, 1, 0),
                             (0, 0, 0, 0),
                             (0, 0, 0, 0))
        
        elif self._rotate == 2:
            self.imageMap = ((1, 1, 0, 0),
                             (0, 1, 0, 0),
                             (0, 1, 0, 0),
                             (0, 0, 0, 0))
            
        elif self._rotate == 3:
            self.imageMap = ((1, 1, 1, 0),
                             (1, 0, 0, 0),
                             (0, 0, 0, 0),
                             (0, 0, 0, 0))
#  |
# _|       
class BrickMirrorL(BrickBase):
    def __init__(self):
        BrickBase.__init__(self)
             
        self._width = 2
        self._height = 3
        
        # The shape of the brick
        self.imageMap = ((0, 1, 0, 0),
                         (0, 1, 0, 0),
                         (1, 1, 0, 0),
                         (0, 0, 0, 0))
        
    # Change the shape of the brick        
    def rotate(self, counterclockwise):
        temp = self._width
        self._width = self._height
        self._height = temp
        
        self._rotate += counterclockwise;
        if self._rotate == 4:
            self._rotate = 0
        elif self._rotate == -1:
            self._rotate = 3
        
        if self._rotate == 0:
            self.imageMap = ((0, 1, 0, 0),
                             (0, 1, 0, 0),
                             (1, 1, 0, 0),
                             (0, 0, 0, 0))
            
        elif self._rotate == 1:
            self.imageMap = ((1, 1, 1, 0),
                             (0, 0, 1, 0),
                             (0, 0, 0, 0),
                             (0, 0, 0, 0))
        
        elif self._rotate == 2:
            self.imageMap = ((1, 1, 0, 0),
                             (1, 0, 0, 0),
                             (1, 0, 0, 0),
                             (0, 0, 0, 0))
            
        elif self._rotate == 3:
            self.imageMap = ((1, 0, 0, 0),
                             (1, 1, 1, 0),
                             (0, 0, 0, 0),
                             (0, 0, 0, 0))
# _
#  |_   
class BrickZ(BrickBase):
    def __init__(self):
        BrickBase.__init__(self)
             
        self._width = 3
        self._height = 2
        
        # The shape of the brick
        self.imageMap = ((1, 1, 0, 0),
                         (0, 1, 1, 0),
                         (0, 0, 0, 0),
                         (0, 0, 0, 0))
    
    # Change the shape of the brick    
    def rotate(self, counterclockwise):
        temp = self._width
        self._width = self._height
        self._height = temp
        
        self._rotate += counterclockwise;
        
        if self._rotate == 2:
            self._rotate = 0
        elif self._rotate == -1:
            self._rotate = 1
        
        if self._rotate == 0:
            self.imageMap = ((1, 1, 0, 0),
                             (0, 1, 1, 0),
                             (0, 0, 0, 0),
                             (0, 0, 0, 0))
            
        elif self._rotate == 1:
            self.imageMap = ((0, 1, 0, 0),
                             (1, 1, 0, 0),
                             (1, 0, 0, 0),
                             (0, 0, 0, 0))
#   _
# _|   
class BrickMirrorZ(BrickBase):
    def __init__(self):
        BrickBase.__init__(self)
                
        self._width = 3
        self._height = 2
        
        # The shape of the brick
        self.imageMap = ((0, 1, 1, 0),
                         (1, 1, 0, 0),
                         (0, 0, 0, 0),
                         (0, 0, 0, 0))
        
    # Change the shape of the brick   
    def rotate(self, counterclockwise):
        temp = self._width
        self._width = self._height
        self._height = temp
        
        self._rotate += counterclockwise;
        if self._rotate == 2:
            self._rotate = 0
        elif self._rotate == -1:
            self._rotate = 1
        
        if self._rotate == 0:
            self.imageMap = ((0, 1, 1, 0),
                             (1, 1, 0, 0),
                             (0, 0, 0, 0),
                             (0, 0, 0, 0))
            
        elif self._rotate == 1:
            self.imageMap = ((1, 0, 0, 0),
                             (1, 1, 0, 0),
                             (0, 1, 0, 0),
                             (0, 0, 0, 0))

# __|__ 
class BrickOther(BrickBase):
    def __init__(self):
        BrickBase.__init__(self)
        
        self._width = 3
        self._height = 2
        
        # The shape of the brick
        self.imageMap = ((0, 1, 0, 0),
                         (1, 1, 1, 0),
                         (0, 0, 0, 0),
                         (0, 0, 0, 0))
        
    # Change the shape of the brick    
    def rotate(self, counterclockwise):
        temp = self._width
        self._width = self._height
        self._height = temp
        
        self._rotate += counterclockwise;
        if self._rotate == 4:
            self._rotate = 0
        elif self._rotate == -1:
            self._rotate = 3
        
        if self._rotate == 0:
            self.imageMap = ((0, 1, 0, 0),
                             (1, 1, 1, 0),
                             (0, 0, 0, 0),
                             (0, 0, 0, 0))
            
        elif self._rotate == 1:
            self.imageMap = ((0, 1, 0, 0),
                             (1, 1, 0, 0),
                             (0, 1, 0, 0),
                             (0, 0, 0, 0))
        
        elif self._rotate == 2:
            self.imageMap = ((1, 1, 1, 0),
                             (0, 1, 0, 0),
                             (0, 0, 0, 0),
                             (0, 0, 0, 0))
            
        elif self._rotate == 3:
            self.imageMap = ((1, 0, 0, 0),
                             (1, 1, 0, 0),
                             (1, 0, 0, 0),
                             (0, 0, 0, 0))
