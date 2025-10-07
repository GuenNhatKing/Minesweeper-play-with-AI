import time

class Timer:
    def __init__(self):
        self.reset()
    
    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed # running and not reset
            self.running = True
    
    def stop(self):
        if self.running:
            self.elapsed = time.time() - self.start_time
            self.running = False
    
    def reset(self):
        self.start_time = None
        self.elapsed = 0
        self.running = False
    
    def get_time(self):
        if self.running:
            return int(time.time() - self.start_time)
        return int(self.elapsed)