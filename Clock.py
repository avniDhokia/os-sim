import time

class Clock:

    def __init__(self):
        self.start = time.time()
        self.checkpoint = time.time()
    
    def get_time_passed(self):
        now = time.time()
        return now - self.start
    
    def set_checkpoint(self):
        self.checkpoint = time.time()
        return
    
    def get_time_since_checkpoint(self):
        now = time.time()
        return now - self.checkpoint