class Task:

    def __init__(self):
        self.ticks = 0
        self.sys_ticks = 0

    def inc_tick(self):
        self.ticks += 1

    def get_ticks(self):
        return self.ticks
