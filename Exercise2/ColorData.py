# -*- coding: UTF-8 -*-

import ColorUtil

import pickle

# Class implements observable protocol
class ColorData(object):
    def __init__(self):
        self.__r = 0
        self.__g = 0
        self.__b = 0
        
        self.__h = 0
        self.__s = 0
        self.__v = 0
        
        # Cache for preventing value oscillation
        self.__hCache = 0
        self.__sCache = 0
        self.__vCache = 0
        
        self.__rCache = 0
        self.__gCache = 0
        self.__bCache = 0
        
        self.__colorFile = None
        
        self.__observers = []
        
    # Register observer
    def addObserver(self, observer):
        self.__observers.append(observer)
    
    # Call all the observers' update
    def notifyObservers(self):
        for eachObserver in self.__observers:
            eachObserver.update()
    
    # Getter functions    
    def getR(self):
        return self.__r;
    
    def getG(self):
        return self.__g;
    
    def getB(self):
        return self.__b;
    
    def getH(self):
        return self.__h;
    
    def getS(self):
        return self.__s;
    
    def getV(self):
        return self.__v;
    
    # Setter functions    
    def setRGB(self, r, g, b):
        # To prevent value oscillation               
        if (round(r), round(g), round(b)) == (round(self.__rCache), round(self.__gCache), round(self.__bCache)):
            return
              
        self.__r = r
        self.__g = g
        self.__b = b

        (self.__h, self.__s, self.__v) = ColorUtil.rgb2hsv(self.__r, self.__g, self.__b)
        (self.__hCache, self.__sCache, self.__vCache) = (self.__h, self.__s, self.__v)
        
        self.notifyObservers()
        
    def setHSV(self, h, s, v):
        # To prevent value oscillation 
        if (round(h), round(s), round(v)) == (round(self.__hCache), round(self.__sCache), round(self.__vCache)):
            return
           
        self.__h = h
        self.__s = s
        self.__v = v

        (self.__r, self.__g, self.__b) = ColorUtil.hsv2rgb(self.__h, self.__s, self.__v)
        (self.__rCache, self.__gCache, self.__bCache) = (self.__r, self.__g, self.__b)
        
        self.notifyObservers()
            
    # Load from and save to the color file         
    def loadColor(self):
        try:
            self.__colorFile = open(r'Color.pickle', 'rb')
        except IOError:
            print '[ColorData::loadColor] No Color File Found'
        else:
            print '[ColorData::loadColor] Load Color File'
            colorTuple = pickle.load(self.__colorFile)
            self.__colorFile.close()
            self.setRGB(colorTuple[0], colorTuple[1], colorTuple[2])
    
    # Save the Color to disk       
    def saveColor(self):    
        try:
            self.__colorFile = open(r'Color.pickle', 'wb')
        except IOError:
            print '[ColorData::saveColor] Cannot write the color file'
        else:
            print '[ColorData::saveColor] Write color file'
            colorTuple = (self.__r, self.__g, self.__b)
            pickle.dump(colorTuple, self.__colorFile)
            self.__colorFile.close()
            
            
            
            