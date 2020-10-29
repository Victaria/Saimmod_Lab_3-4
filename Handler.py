import random


class Handler:

    def __init__(self, probability):
        self.probability = probability
        self.task = None
        self.busy = 0
        self.task_count = 0

    def tick(self):

        if not self.is_busy():
            return None

        # генерируем число от 0 до 1 и
        # сравниваем с вероятностью необработки заявки системой
        # меньше - не обработана, больше - обработана
        ev = random.random()
        if ev <= self.probability:
            self.busy += 1
            return None
        else:
            task = self.task
            self.task = None
            return task

    def set_task(self, task):
        self.task_count += 1
        self.task = task
        self.busy += 1

    def is_busy(self):
        return self.task is not None

    def __str__(self):
        return '1' if self.is_busy() else '0'
