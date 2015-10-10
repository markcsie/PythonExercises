# -*- coding: UTF-8 -*-

import sys
# for double-clicking the script to execute the program, needed to be changed for different users
sys.path.append(r"C:\Users\MarkKC_Ma\Desktop\KoanSDK\DLLs")
sys.path.append(r"C:\Users\MarkKC_Ma\Desktop\KoanSDK")

import koan
from Widgets.window import Window
from Widgets.component import Component
from Widgets.slider import Slider
from Widgets.edit import Edit
from Widgets.text import Text
from Widgets import color

import math

from ColorData import ColorData

# Observer base class
class Observer(object):
    def __init__(self, subject):
        self.subject = subject
        subject.addObserver(self);

    # Should always be overridden
    def update(self):
        print "[Observer::update] Error!! This method shouldn't be called"
        pass
    
    # Should always be overridden
    def display(self):
        print "[Observer::display] Error!! This method shouldn't be called"
        pass
    
# RGBEdit Class implements observer protocol
class RGBEditObserver(Observer):
    def __init__(self, parent, colorSubject):
        self.colorSubject = colorSubject
        Observer.__init__(self, colorSubject)
             
        self._rEdit = parent.initEdit(parent, str(0), (400, 50, 100, 20))
        self._gEdit = parent.initEdit(parent, str(0), (400, 70, 100, 20))
        self._bEdit = parent.initEdit(parent, str(0), (400, 90, 100, 20))
        
        self._rEdit.changeEvent('text', self._onEditTextChanged, 'R')
        self._gEdit.changeEvent('text', self._onEditTextChanged, 'G')
        self._bEdit.changeEvent('text', self._onEditTextChanged, 'B')
    
    # Update edit text
    def update(self):
        self._rEdit.text = str(int(round(self.colorSubject.getR())))
        self._gEdit.text = str(int(round(self.colorSubject.getG())))
        self._bEdit.text = str(int(round(self.colorSubject.getB())))
    
    # Callback function for text changed  
    def _onEditTextChanged(self, which):
        if which == 'R':
            tempEdit = self._rEdit
        elif which == 'G':
            tempEdit = self._gEdit   
        elif which == 'B':
            tempEdit = self._bEdit
            
        if tempEdit.text == '':
            tempEdit.text = '0'
            
        try:
            tempR = float(self._rEdit.text)
            tempG = float(self._gEdit.text)
            tempB = float(self._bEdit.text)
                
            if tempR > 255:
                tempR = 255
                self._rEdit.text = '255'
            if tempG > 255:
                tempG = 255
                self._gEdit.text = '255'
            if tempB > 255:
                tempB = 255
                self._bEdit.text = '255'
                    
            if tempR < 0:
                tempR = 0
            if tempG < 0:
                tempG = 0
            if tempB < 0:
                tempB = 0
                    
            self.colorSubject.setRGB(tempR, tempG, tempB)
        except ValueError:
            self._rEdit.text = str(int(round(self.colorSubject.getR())))
            self._gEdit.text = str(int(round(self.colorSubject.getG())))
            self._bEdit.text = str(int(round(self.colorSubject.getB())))

# HSVEdit Class implements observer protocol       
class HSVEditObserver(Observer):
    def __init__(self, parent, colorSubject):
        self.colorSubject = colorSubject
        Observer.__init__(self, colorSubject)
               
        self._hEdit = parent.initEdit(parent, str(0), (400, 120, 100, 20))
        self._sEdit = parent.initEdit(parent, str(0), (400, 140, 100, 20))
        self._vEdit = parent.initEdit(parent, str(0), (400, 160, 100, 20))
        
        self._hEdit.changeEvent('text', self._onEditTextChanged, 'H')
        self._sEdit.changeEvent('text', self._onEditTextChanged, 'S')
        self._vEdit.changeEvent('text', self._onEditTextChanged, 'V')
        
    # Update edit text    
    def update(self):
        self._hEdit.text = str(int(round(self.colorSubject.getH())))
        self._sEdit.text = str(int(round(self.colorSubject.getS())))
        self._vEdit.text = str(int(round(self.colorSubject.getV())))
        
    # Callback function for text changed 
    def _onEditTextChanged(self, which):      
        if which == 'H':
            tempEdit = self._hEdit
        elif which == 'S':
            tempEdit = self._sEdit
        elif which == 'V':
            tempEdit = self._vEdit
            
        if tempEdit.text == '':
            tempEdit.text = '0'
            
        try:
            tempH = float(self._hEdit.text)
            tempS = float(self._sEdit.text)
            tempV = float(self._vEdit.text)
                
            if tempH > 360:
                tempH = 360
                self._hEdit.text = '360'
            if tempS > 100:
                tempS = 100
                self._sEdit.text = '100'
            if tempV > 100:
                tempV = 100
                self._vEdit.text = '100'
                    
            if tempH < 0:
                tempH = 0
            if tempS < 0:
                tempS = 0
            if tempV < 0:
                tempV = 0    
                
            self.colorSubject.setHSV(tempH, tempS, tempV)
        except ValueError:
            self._hEdit.text = str(int(round(self.colorSubject.getH())))
            self._sEdit.text = str(int(round(self.colorSubject.getS())))
            self._vEdit.text = str(int(round(self.colorSubject.getV())))
         
# RGBSlider Class implements observer protocol    
class RGBSliderObserver(Observer):
    def __init__(self, parent, colorSubject):
        self.colorSubject = colorSubject
        Observer.__init__(self, colorSubject)
        
        self._rSlider = parent.initSlider(parent, (100, 50, 255, 10))
        self._gSlider = parent.initSlider(parent, (100, 70, 255, 10))
        self._bSlider = parent.initSlider(parent, (100, 90, 255, 10))
        
        self._rSlider.bind('Slide', self._onSlide, 'R')
        self._gSlider.bind('Slide', self._onSlide, 'G')
        self._bSlider.bind('Slide', self._onSlide, 'B')
    
    # Update slider value      
    def update(self):          
        self._rSlider.setValue(self.colorSubject.getR() / 255.0)
        self._gSlider.setValue(self.colorSubject.getG() / 255.0)
        self._bSlider.setValue(self.colorSubject.getB() / 255.0)

    # RGB Slider callback function
    def _onSlide(self, which, offset):   
        if which == 'R': 
            self.colorSubject.setRGB(self._rSlider.getValue() * 255.0, self.colorSubject.getG(), self.colorSubject.getB())   
        elif which == 'G':
            self.colorSubject.setRGB(self.colorSubject.getR(), self._gSlider.getValue() * 255.0, self.colorSubject.getB())   
        elif which == 'B':
            self.colorSubject.setRGB(self.colorSubject.getR(), self.colorSubject.getG(), self._bSlider.getValue() * 255.0)   
        
# HSVSlider Class implements observer protocol         
class HSVSliderObserver(Observer):
    def __init__(self, parent, colorSubject):
        self.colorSubject = colorSubject
        Observer.__init__(self, colorSubject)
        
        self._hSlider = parent.initSlider(parent, (100, 120, 255, 10))
        self._sSlider = parent.initSlider(parent, (100, 140, 255, 10))
        self._vSlider = parent.initSlider(parent, (100, 160, 255, 10))
        
        self._hSlider.bind('Slide', self._onSlide, 'H')
        self._sSlider.bind('Slide', self._onSlide, 'S')
        self._vSlider.bind('Slide', self._onSlide, 'V')
    
    # Update slider value        
    def update(self):    
        self._hSlider.setValue(self.colorSubject.getH() / 360.0)
        self._sSlider.setValue(self.colorSubject.getS() / 100.0)
        self._vSlider.setValue(self.colorSubject.getV() / 100.0)
          
    # HSV Slider callback function
    def _onSlide(self, which, offset):     
        if which == 'H':
            self.colorSubject.setHSV(self._hSlider.getValue() * 360.0, self.colorSubject.getS(), self.colorSubject.getV())
        elif which == 'S':
            self.colorSubject.setHSV(self.colorSubject.getH(), self._sSlider.getValue() * 100.0, self.colorSubject.getV())
        elif which == 'V':
            self.colorSubject.setHSV(self.colorSubject.getH(), self.colorSubject.getS(), self._vSlider.getValue() * 100.0)

# ColorMap Class implements observer protocol
class ColorMapObserver(Observer):
    def __init__(self, parent, colorSubject):
        self.colorSubject = colorSubject
        Observer.__init__(self, colorSubject)
        
        # Color Map Component
        self._colorMapComponent = Component(parent)
        self._colorMapComponent.background = r'Images\HSVColorMap.jpg'
        self._colorMapComponent.rect = (100, 200, 200, 200)
        
        self._colorMapComponent.bind('Mouse Move', self._onMouseMoved)
        self._colorMapComponent.bind('Mouse Down', self._onMouseDown)

        # Cursor component on the color Map   
        self._colorMapCursorComponent = Component(parent)
        self._colorMapCursorComponent.bgColor = color.black
        self._colorMapCursorComponent.rect = (200, 200, 5, 5)
    
    # Update the cursor on the color map     
    def update(self):     
        (x, y) = self._hs2xy(self.colorSubject.getH(), self.colorSubject.getS())
        self._colorMapCursorComponent.xy = (x + self._colorMapComponent.left, y + self._colorMapComponent.top)
        
    # Color map component callback function       
    def _onMouseMoved(self, x, y, unused):
        if self._colorMapComponent.getIsMouseDown():
            self._onMouseDown(x, y, unused)
            
    def _onMouseDown(self, x, y, unused):
        (tempH, tempS, tempV) = self._xy2hsv(x, y)
        if tempS <= 100:
            self.colorSubject.setHSV(tempH, tempS, tempV)
            
    # From color map coordinates to HSV
    def _xy2hsv(self, x, y):
        h = math.atan2(y - 100, x - 100) * 180 / math.pi
        if h < 0:
            h = h + 360.0 
        s = ((x - 100) ** 2 + (y - 100) ** 2) ** 0.5
        return (round(h), round(s), 100)

    # From HSV to color map coordinates
    def _hs2xy(self, h, s):
        h = h / 180.0 * math.pi
        x = 100 + s * math.cos(h)
        y = 100 + s * math.sin(h)
        return (int(round(x)), int(round(y)))

# ColorComponent Class implements observer protocol        
class ColorComponentObserver(Observer):
    def __init__(self, parent, colorSubject):
        self.colorSubject = colorSubject
        Observer.__init__(self, colorSubject)
        
        self._colorComponent = Component(parent)
        self._colorComponent.bgColor = color.black
        self._colorComponent.rect = (25, 85, 50, 50)
    
    # Update the color        
    def update(self):     
        self._colorComponent.bgColor = (self._colorComponent.bgColor[0], self.colorSubject.getR(), self.colorSubject.getG(), self.colorSubject.getB())      
     
class ColorPickerWindow(Window):
    def __init__(self):
        Window.__init__(self)
        
        # The main window
        self.create(100, 100, 500, 500, caption=True, minmax=False, resize=False)
        
        # The color data implements observable protocol
        self.color = ColorData()
        
        # Instantiation and Initialization of the components
        self.initText(self, 'R', (80, 45, 15, 15))
        self.initText(self, 'G', (80, 65, 15, 15))
        self.initText(self, 'B', (80, 85, 15, 15))
        
        self.initText(self, 'H', (80, 115, 15, 15))
        self.initText(self, 'S', (80, 135, 15, 15))
        self.initText(self, 'V', (80, 155, 15, 15))
        
        RGBEditObserver(self, self.color)
        RGBSliderObserver(self, self.color)
        
        HSVEditObserver(self, self.color)
        HSVSliderObserver(self, self.color)
        
        ColorMapObserver(self, self.color)
        ColorComponentObserver(self, self.color)
        #####
        
        # Restore color from disk 
        self.color.loadColor()
    
    # Initialization functions    
    def initText(self, parent, text, rect):
        tempText = Text(parent)
        tempText.fontSize = 15
        tempText.text = text
        tempText.rect = rect
        
        return tempText
    
    def initEdit(self, parent, text, rect):
        tempEdit = Edit(parent)
        
        tempEdit.bgColor = color.black
        tempEdit.fontColor = color.white
        tempEdit.rect = rect
        tempEdit.text = text
        
        return tempEdit
    
    def initSlider(self, parent, rect):
        tempSlider = Slider(parent)
        
        tempSlider.bgColor = color.gray
        tempSlider.vertical = False
        tempSlider.rect = rect
        tempSlider.thumbMinSize = 10
        tempSlider.thumbImage = r'Images\SliderThumb.jpg'
        
        return tempSlider
    #####
               
    def close(self):
        print '[ColorPickerWindow::close] Window closed'
        # Save the color data to disk
        self.color.saveColor()
        super(ColorPickerWindow, self).close()
        
    def onDraw(self, render):
        render.Clear(255, 255, 255, 255)
    
if __name__ == '__main__':
    koan.init()
    w = ColorPickerWindow()
    w.show()
    koan.run(1)
    koan.final()

