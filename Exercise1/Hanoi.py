class Hanoi(object):   
    def __init__(self, total_plates):
        self.__total_plates= total_plates
        self.__locations = [_Location([]), _Location([]), _Location([])]
        for i in range(total_plates):
            self.__locations[0].plates.insert(0, _Plate(i, 0))
    
    # Recursive algorithm for solving Hanoi problem
    # Move 'number' plates from 'from_location' to 'to_location'
    def move(self, number, from_location, to_location):
        if number == 1:
            yield self.__move_plate(from_location, to_location)
            return

        other_location = 3 - (from_location + to_location)
        
        for step1 in self.move(number - 1, from_location, other_location):
            yield step1
        yield self.__move_plate(from_location, to_location)
        for step2 in self.move(number - 1, other_location, to_location):
            yield step2
            
    # move one plate from one place to another place        
    def __move_plate(self, from_location, to_location):
        poped_plate = self.__pop_plate(from_location)
        poped_plate.location = to_location
        self.__locations[to_location].plates.append(poped_plate)
        print '[Hanoi::__move_plate] ' +'Move plate ' + str(poped_plate.number) + ' from ' + str(from_location) + ' to ' + str(to_location)
        return _Move(poped_plate.number, from_location, to_location)
    
    # Pop one plate from the location 'which'
    def __pop_plate(self, which):
        return self.__locations[which].plates.pop()
    
    # Get the number of total_plates
    def get_total(self):
        return self.__total_plates
    
    # Get all plates in location 'which'
    def get_plates(self, which):
        return self.__locations[which].plates
    
    # Get the number of plates in location 'which'
    def get_total_in_location(self, which):
        return len(self.__locations[which].plates)
            
class _Location(object):
    def __init__(self, plates):
        self.plates = plates

class _Plate(object):
    def __init__(self, number, location):
        self.number = number
        self.location = location

class _Move(object):
    def __init__(self, number, from_location, to_location):
        self.number = number
        self.from_location = from_location
        self.to_location = to_location
        
        
# Testing Code   
if __name__ == '__main__':    
    hanoi = Hanoi(5)  
    steps = hanoi.move(5, 0, 2)
    for each_step in steps:
        pass
    
  

