class Media(object):
    def __init__(self):
        self.fileName = ''
        self.durationMin = 0
        self.durationSec = 0
        self.totalSec = 0 # equals durationMin * 60 + durationSec
        self.currentPositionMin = 0
        self.currentPositionSec = 0
