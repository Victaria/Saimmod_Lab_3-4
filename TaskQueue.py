class TaskQueue:

    def __init__(self, size):
        self.size = size
        self.tasks = []
        self.sum_of_sizes = 0
        self.sum_of_middle_sizes = 0
        self.num = 0

    def tick(self):
        for task in self.tasks:
            task.inc_tick()
        self.sum_of_sizes += len(self.tasks)
        self.sum_of_middle_sizes += len(self.tasks) + 1

    def enqueue(self, task):
        if len(self.tasks) == self.size:
            raise Exception('The queue is full')
        else:
            self.tasks.append(task)

    def dequeue(self):
        task = self.tasks[0]
        self.tasks = self.tasks[1:]
        return task

    def has_place(self):
        return len(self.tasks) < self.size

    def __len__(self):
        return len(self.tasks)

    def __str__(self):
        return str(len(self))