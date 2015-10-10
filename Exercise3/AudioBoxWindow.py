# -*- coding: UTF-8 -*-
import os
import pickle

# for py2exe
import sys
sys.path.append("DLLs")

import koan
from Widgets.component import Component
from Widgets.window import Window
from Widgets.slider import Slider 
from Widgets.text import Text
from Widgets.button import TextButton, Group, TextBase, CheckBase, TipBase, RadioBase
from Widgets import color

# C++ functions
from AudioFunctions import AudioFunctions 

from Media import Media

# State of the AudioBox
STOP_STATE = 0
PAUSE_STATE = 1
PLAY_STATE = 2

# Button class for playlist
class RadioTextButton(Component, TextBase, TipBase, RadioBase, CheckBase):
    def __init__(self, parent):
        Component.__init__(self, parent)
        TextBase.__init__(self)
        RadioBase.__init__(self)
        CheckBase.__init__(self)
        TipBase.__init__(self)
        self.command = ''
        self.changeEvent('checked', self.__onCheckChanged, postevent=False)

    def __onCheckChanged(self):
        if self.command:
            self.invokeCmd(self.command, self.checked)

    def onDraw(self, render):
        super(RadioTextButton, self).onDraw(render)
        TextBase.onDraw(self, render)

class AudioBoxWindow(Window):
    def __init__(self):
        Window.__init__(self)
        
        # Initialization of the C++ DirectShow Library
        self.audioFunctions = AudioFunctions()
        self.audioFunctions.InitDirectShow()
        
        # Media Information
        self.media = Media()
        
        # The main window
        self.create(100, 100, 700, 300, caption=True, resize=False)
        
        # Button for 'OpenFile'
        self._openFileButton = TextButton(self)
        self._openFileButton.rect = (0, 0, 50, 30)
        self._openFileButton.text = 'OpenFile'
        self._openFileButton.background = r'Images\Root_button.png'
        self.autoRemove(self._openFileButton.bind('Click', self._onOpenFile))
        
        # Button for 'Play' and 'Pause'
        self._triggerButton = TextButton(self)
        self._triggerButton.rect = (60, 0, 50, 30)
        self._triggerButton.text = 'Play'
        self._triggerButton.background = r'Images\Root_button.png'
        self.autoRemove(self._triggerButton.bind('Click', self._onTrigger))
        
        # Button for 'Stop'
        self._stopButton = TextButton(self)
        self._stopButton.rect = (120, 0, 50, 30)
        self._stopButton.text = 'Stop'
        self._stopButton.background = r'Images\Root_button.png'
        self.autoRemove(self._stopButton.bind('Click', self._onStop))
        
        # Button for 'Remove'
        self._stopButton = TextButton(self)
        self._stopButton.rect = (450, 0, 50, 30)
        self._stopButton.text = 'Remove'
        self._stopButton.background = r'Images\Root_button.png'
        self.autoRemove(self._stopButton.bind('Click', self._onRemove))
        
        # PlayTime
        self._playTimeText = Text(self)
        self._playTimeText.autosize = True
        self._playTimeText.text = 'PlayTime'
        self._playTimeText.fontSize = 15
        self._playTimeText.xy = (30, 155) 
        
        # Slider for 'playTime'
        self._playTimeSlider = Slider(self)
        self._playTimeSlider.bgColor = color.gray
        self._playTimeSlider.vertical = False
        self._playTimeSlider.rect = (100, 160, 255, 10)
        self._playTimeSlider.thumbMinSize = 10
        self._playTimeSlider.thumbImage = r'Images\ScrollBarThumb.jpg'
        self.autoRemove(self._playTimeSlider.bind('Slide', self._onPlayTimeSlide))
        self.autoRemove(self._playTimeSlider.bind('Slide Start', self._onPlayTimeSlideStart))  
        self.autoRemove(self._playTimeSlider.bind('Slide End', self._onPlayTimeSlideEnd))
        
        # Slider for 'Volume'
        self._volumeSlider = Slider(self)
        self._volumeSlider.bgColor = color.gray
        self._volumeSlider.vertical = True
        self._volumeSlider.rect = (400, 50, 10, 100)
        self._volumeSlider.thumbMinSize = 10
        self._volumeSlider.thumbImage = r'Images\ScrollBarThumb.jpg'
        self.autoRemove(self._volumeSlider.bind('Slide', self._onVolumeSlide))
        
        # Volume
        self._volumeText = Text(self)
        self._volumeText.autosize = True
        self._volumeText.text = 'Volume'
        self._volumeText.fontSize = 15
        self._volumeText.xy = (380, 155)
        
        # Media Information text
        self._mediaInfoText = Text(self)
        self._mediaInfoText.autosize = True
        self._mediaInfoText.fontSize = 15
        self._mediaInfoText.xy = (20, 45)
        self._mediaInfoText.text = 'FileName: \n' \
                                   'Duration: 0 min 0 sec\n'
                   
        # Media Position text
        self._mediaPositionText = Text(self)
        self._mediaPositionText.autosize = True
        self._mediaPositionText.fontSize = 15
        self._mediaPositionText.xy = (20, 80)
        self._mediaPositionText.text = 'Position: 0 min 0 sec\n'    
                       
        # Playlist text
        self._playlistText = Text(self)
        self._playlistText.autosize = True
        self._playlistText.text = 'Playlist'
        self._playlistText.fontSize = 15
        self._playlistText.fontColor = color.blue
        self._playlistText.xy = (450, 30)
        
        # Restore the playlist from disk
        self.playList = {}
        self.workingDir = os.getcwd() # Locate the current working directory
        
        try:
            playListFile = open(self.workingDir + r'\PlayList.pickle', 'rb')
        except IOError:
            print '[AudioBoxWindow::__init__] No Playlist File Found'
        else:
            print '[AudioBoxWindow::__init__] Load Playlist File'
            self.playList = pickle.load(playListFile) # Dictionary storing the playlist
            playListFile.close()
        
        # Radio button group
        self._platListGroup = Group(self)
        self._platListGroup.xy = (450, 50)
        self._platListGroup.size = (200, 500)
        self._platListGroup.autosize = True
        
        # Display the playlist
        self.mediaButtonList = []
        self._refreshPlayList()
        
        # Flag indicating if the playTime slider is sliding
        self.playTimeSliding = False
        
        self.displayAnim = None
        self.displayAnimRunning = False
        
    def _refreshPlayList(self):
        # Delete all the the buttons 
        for eachMedia in self.mediaButtonList:
            eachMedia.close()
        self.mediaButtonList = [] 
           
        # Reinsert the items from the playlist
        for key in self.playList.keys():
            self._addMediaButton(key)
            
        self.nowPlaying = -1 # Index of the media which is playing now, -1 means no one is playing
        
    # Insert the media button into the platListGroup
    def _addMediaButton(self, fileName):
        i = len(self.mediaButtonList)
        
        self.mediaButtonList.append(RadioTextButton(self._platListGroup))
        self.mediaButtonList[-1].autosize = True
        self.mediaButtonList[-1].text = fileName
        self.mediaButtonList[-1].rect = (0, i * 20, 300, 20)
        self.autoRemove(self.mediaButtonList[-1].bind('Click', self._playListOnClicked, i))
        self.mediaButtonList[-1].bindData('bgColor', self.mediaButtonList[-1], 'checked', dir='<-', converter=lambda x: color.lightgray if x else color.white)
        self.autoRemove(self.mediaButtonList[-1].changeEvent('checked', self._onMediaChanged, fileName, i))
        self.mediaButtonList[-1].checked = False
   
    # Callback function for button 'Start' and 'Pause'    
    def _onTrigger(self):
        currentState = self.audioFunctions.GetCurrentState()
        
        if currentState == STOP_STATE:
            if self.nowPlaying != -1:
                self.audioFunctions.PlayMedia()
                self._triggerButton.text = 'Pause'         
                # Timer for refreshing the media information
                self.displayAnim = koan.anim.IntervalExecute(1, self._onTimer)
                self.displayAnimRunning = True
                  
        elif currentState == PAUSE_STATE:
            if self.nowPlaying != -1:
                self.audioFunctions.PlayMedia()
                self._triggerButton.text = 'Pause'     
                # Timer for refreshing the media information
                self.displayAnim = koan.anim.IntervalExecute(1, self._onTimer)
                self.displayAnimRunning = True
            
        elif currentState == PLAY_STATE:
            self.audioFunctions.PauseMedia()
            self._triggerButton.text = 'Play'
                
            self.displayAnim.remove()
            self.displayAnimRunning = False
       
    # Callback function for button 'Stop'
    def _onStop(self):
        if self.displayAnimRunning:
            self.displayAnim.remove()
        
        self.audioFunctions.StopMedia()
        self._triggerButton.text = 'Play'
        
        self._playTimeSlider.setValue(0)
                  
    # Callback function for volume slider 
    def _onVolumeSlide(self, value):
        self.audioFunctions.SetVolume(value)
        
    # Callback functions for playtime slider
    def _onPlayTimeSlide(self, value):      
        if self.playTimeSliding:
            self.media.totalSec = int((self.media.durationMin * 60 + self.media.durationSec) * value)
        if self._playTimeSlider.isMouseDown and self.nowPlaying != -1:
            self.audioFunctions.SetMediaPosition(self._playTimeSlider.value)
            
        self._displayMediaPosition()
            
    def _onPlayTimeSlideEnd(self):
        self.playTimeSliding = False
        if self.nowPlaying != -1:
            self.audioFunctions.SetMediaPosition(self._playTimeSlider.value)     
    def _onPlayTimeSlideStart(self):
        self.playTimeSliding = True
        
    # Callback function for refreshing the media info
    def _onTimer(self):
        if self.playTimeSliding == False:
            self._displayMediaPosition()
              
            try:
                self._playTimeSlider.setValue(float(self.media.totalSec) / float(self.media.durationMin * 60 + self.media.durationSec))
            except ZeroDivisionError:
                self._playTimeSlider.setValue(0)
                
            # It's the end of the media
            if self.media.currentPositionMin == self.media.durationMin and self.media.currentPositionSec == self.media.durationSec:
                self._onStop()
                
    def _displayMediaPosition(self):
        if self.playTimeSliding == False:
            self.media.totalSec = self.audioFunctions.GetMediaPosition()
            
        self.media.currentPositionSec = self.media.totalSec % 60
        self.media.currentPositionMin = self.media.totalSec / 60
        
        self._mediaPositionText.text = 'Position: ' + str(self.media.currentPositionMin) + ' min ' + str(self.media.currentPositionSec) + ' sec\n'
    
    def _displayMediaInfo(self):
        self._mediaInfoText.text = 'FileName: ' + self.media.fileName + '\n' \
                                   'Duration: ' + str(self.media.durationMin) + ' min ' + str(self.media.durationSec) + ' sec\n'
    
    # Callback function for button 'OpenFile'
    def _onOpenFile(self):
        fileName = self.audioFunctions.OpenFileDialog() # Call the MFC open file dialog
        if fileName != None:
            self.media.fileName = fileName
            self.media.totalSec = self.audioFunctions.GetMediaDuration()
            tempTotalSec = self.media.totalSec
            
            if (tempTotalSec == 0): # Sometimes we can't open the file due to unknown file name or wrong file format
                self.media.fileName = 'File Not Supported'
                self.nowPlaying = -1 
            
            # Insert the newly opened file into playlist
            if fileName not in self.playList.keys() and tempTotalSec != 0:
                self.playList[fileName] = self.audioFunctions.GetFilePath()
                self._addMediaButton(self.media.fileName)
                self.mediaButtonList[-1].checked = True # this step would have the _onMediaChanged get called
            else: # If it's already existed
                for eachMedia in self.mediaButtonList:
                    if eachMedia.text == fileName:
                        self._triggerButton.text = 'Play'
                        eachMedia.checked = True # this step would have the _onMediaChanged get called
                        
    # Callback function when user changes the media in the list or opens a file   
    def _onMediaChanged(self, key, which):
        if self.mediaButtonList[which].checked == True and which != self.nowPlaying:
            self._onStop()
            self.nowPlaying = which
            self.media.fileName = key
            self.audioFunctions.OpenMedia(self.playList[key])
            self.audioFunctions.SetVolume(self._volumeSlider.getValue())
        
            self.media.totalSec = self.audioFunctions.GetMediaDuration()
            tempTotalSec = self.media.totalSec
            self.media.durationMin = tempTotalSec / 60
            self.media.durationSec = tempTotalSec % 60
            self._triggerButton.text = 'Play'
            
            self._displayMediaInfo()        
            
    # Callback function when user changes the media in the list, this function would have the _onMediaChanged get called
    def _playListOnClicked(self, i):
        self.mediaButtonList[i].checked = True
    
    # Callback function when user removes an item from the list
    def _onRemove(self):
        for eachMedia in self.mediaButtonList: # Search the one which is removed
            if eachMedia.checked:
                del self.playList[eachMedia.text] # Remove it from the dictionary
                self.media.durationMin = 0
                self.media.durationSec = 0
                self.media.fileName = ''
                self._onStop()
                self.nowPlaying = -1
                
                self._displayMediaInfo()
        
        self._refreshPlayList()
            
        
    def close(self):
        self.audioFunctions.FreeDirectShow()
            
        # Save the playlist to disk
        try:
            playListFile = open(self.workingDir + r'\PlayList.pickle', 'wb')
        except IOError:
            print '[AudioBoxWindow::close] Cannot write the playlist file'          
        else:
            print '[AudioBoxWindow::close] Write playlist file'
            pickle.dump(self.playList, playListFile)
            playListFile.close()
                
        print '[AudioBoxWindow::close] Window closed'
        super(AudioBoxWindow, self).close()
        
    def onDraw(self, render):
        render.Clear(255, 255, 255, 255)
    
if __name__ == '__main__':
    koan.init()
    w = AudioBoxWindow()
    w.show()
    koan.run(1)
    koan.final()



