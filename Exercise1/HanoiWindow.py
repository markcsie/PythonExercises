import koan
from Widgets.button import TextButton
from Widgets.window import Window

# Module implementing the Hanoi algorithm
from Hanoi import Hanoi

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000

# Width and height of the hanoi plate image
PLATE_BASE_WIDTH = 20
PLATE_HEIGHT = 30

# Speed of the animation
VERTICAL_SPEED = -100
HORIZONTAL_SPEED = 50
TIME_INTERVAL = 0.05

class HanoiWindow(Window):
    def __init__(self):
        Window.__init__(self)
                    
        self.create(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, caption = True)
        self._plate_images = []        
        
        # Button for 'Start' and 'Pause'
        self._trigger_button = TextButton(self)
        self._trigger_button.rect = 0, 0, 50, 30
        self._trigger_button.text = 'Start'
        self._trigger_button.background = r'Images\Root_button.png'     
        self.autoRemove(self._trigger_button.bind('Click', self._on_trigger_button_click))
        
        # Button for 'Restart'
        self._restart_button = TextButton(self)
        self._restart_button.rect = 60, 0, 50, 30
        self._restart_button.text = 'Restart'
        self._restart_button.background = r'Images\Root_button.png'
        self.autoRemove(self._restart_button.bind('Click', self._on_restart_button_click))
        
        # Button for 'Next'
        self._next_button = TextButton(self)
        self._next_button.rect = 120, 0, 50, 30
        self._next_button.text = 'Next'
        self._next_button.background = r'Images\Root_button.png'
        self.autoRemove(self._next_button.bind('Click', self._on_next_button_click))
         
        self._init_hanoi()
        
    def _init_hanoi(self):
        # Variables for the animation
        self._next_move = True
        self._move = 0
        self._starting_left = 0
        self._starting_top = 0
        self._target_left = 0
        self._target_top = 0
        self._acceleration = 0
        self._time_spent = 0
        
        # Flags indicating the state of the program
        self._running_flag = False
        self._step_by_step_flag = False
        self._over_flag = False
        
        # Reset the trigger_button to 'Start'
        self._trigger_button.text = 'Start'
        
        # Hanoi algorithm object
        self._hanoi = Hanoi(input('Please enter the number of plates\n'))
        
        # Initialization of the plate images    
        for each_plate in self._hanoi.get_plates(0):
            plate_image = TextButton(self)
            plate_image.rect = (70 + self._hanoi.get_total() * PLATE_BASE_WIDTH / 2) - each_plate.number * PLATE_BASE_WIDTH / 2, \
                               (WINDOW_HEIGHT - self._hanoi.get_total() * PLATE_HEIGHT) + each_plate.number * PLATE_HEIGHT, \
                               PLATE_BASE_WIDTH * (each_plate.number + 1), \
                               PLATE_HEIGHT     
            
            plate_image.background = r'Images\Root_button.png'
            self._plate_images.insert(0, plate_image)
            
        # Start running the hanoi algorithm and animation    
        self._steps = self._hanoi.move(self._hanoi.get_total(), 0, 2)
        self._animation = koan.anim.IntervalExecute(TIME_INTERVAL, self._onTimer)
        
    def _on_trigger_button_click(self):
        if self._over_flag:
            return  
        if self._trigger_button.text == 'Start': 
            self._running_flag = True
            self._trigger_button.text = 'Pause'
        else:
            self._running_flag = False
            self._trigger_button.text = 'Start'
        
    def _on_restart_button_click(self):
        if self._running_flag:
            return
        # Remove the registered animation and images
        self._animation.remove()
        for each_plate_image in self._plate_images:
            each_plate_image.close()
    
        # Re-initialization of the program
        self._init_hanoi()
        
    def _on_next_button_click(self):
        if not self._running_flag:
            self._step_by_step_flag = True
    
    def _onTimer(self):
        # No update of the animation when it's in step by step state
        if not self._running_flag and not self._step_by_step_flag:
            return
        
        try:
            if self._next_move:
                self._next_move = False
                
                # Generating the next move
                self._move = self._steps.next()
                
                # Calculating the __starting point and __target point of the animation
                self._time_spent = 0           
                self._starting_left = self._plate_images[self._move.number].left
                self._starting_top = self._plate_images[self._move.number].top
                self._target_left = (70 + self._hanoi.get_total() * PLATE_BASE_WIDTH / 2) + self._move.to_location * (WINDOW_WIDTH / 3) - self._move.number * (PLATE_BASE_WIDTH / 2)
                self._target_top = WINDOW_HEIGHT - self._hanoi.get_total_in_location(self._move.to_location) * PLATE_HEIGHT
                
                # Calculating the total time and __acceleration needed from start to the __target
                total_time = abs((self._target_left - self._starting_left) / HORIZONTAL_SPEED)
                self._acceleration = 2 * (self._target_top - self._starting_top - VERTICAL_SPEED * total_time) / (total_time ** 2)
                
        # Indicating there's no move left
        except StopIteration:
            print '[HanoiWindow::_onTimer] Over!!!'
            self._running_flag = False
            self._over_flag = True
            return
        
        # The plate's moved to the __target point        
        if self._plate_images[self._move.number].left == self._target_left:
            self._plate_images[self._move.number].top = self._target_top
            self._next_move = True
            if self._step_by_step_flag:
                self._step_by_step_flag = False
            return
        
        # Update the new location of the plate    
        if self._target_left > self._plate_images[self._move.number].left:
            self._plate_images[self._move.number].left += HORIZONTAL_SPEED    
        elif self._target_left < self._plate_images[self._move.number].left:
            self._plate_images[self._move.number].left -= HORIZONTAL_SPEED     
        self._time_spent += 1
        self._plate_images[self._move.number].top = self._starting_top + VERTICAL_SPEED * self._time_spent + self._acceleration * (self._time_spent ** 2) / 2
                      
    def close(self):
        # Remove the registered animation
        self._animation.remove()
        super(HanoiWindow, self).close()
    
    def onDraw(self, render):
        render.Clear(255, 0, 0, 0)

if __name__ == '__main__':
    koan.init()
    w = HanoiWindow()
    w.allSightDirty = 0
    w.show()
    koan.run(0)




