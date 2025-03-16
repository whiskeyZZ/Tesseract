from random import randrange, choice

class Target:

    def __init__(self, first: bool):
        self.position = (960, 540)
        self.first = first
        self.dead = False
        self.timer_value = self.set_time()
        self.counter = self.timer_value
        self.set_position()

    def set_time(self) -> int:
        return randrange(200, 500, 100)

    def call_timer(self):
        if not self.dead:
            self.counter -= 1
        if self.counter == 0:
            self.dead = True 

    def set_position(self): 
        pos = [(960, 540), (760, 540), (1160, 540), (560, 540), (1360, 540), (960, 640), (760, 640), (1160, 640), (560, 640), (1360, 640), (960, 440), (760, 440), (1160, 440), (560, 440), (1360, 440)]
        if not self.first:
            self.position = choice(pos)

    def get_position(self):
        return self.position
    
    def get_timer(self):
        return self.counter
        

    