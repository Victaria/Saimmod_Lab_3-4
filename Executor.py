from collections import Counter

from Handler import Handler
from TaskQueue import TaskQueue
from Source import Source


class Executor:

    def __init__(self, pi1, pi2):
        self.iteration_count = 100000
        self.current_tick = 0
        self.handled_count = 0
        self.refused_count = 0
        self.states = []

        self.source = Source()
        self.queue = TaskQueue(2)
        self.handlers = [Handler(pi1), Handler(pi2)]

    def run(self):
        self.queue.tick()

        # для каждого такта
        for i in range(self.iteration_count):
            self.tick(i)

        # поиск количества повторений каждого состояния
        counter = Counter(self.states)

        # для каждого состояния подсчитываем вероятность
        for key in counter.keys():
            counter[key] = counter[key] / self.iteration_count
            print('P{0} = {1}'.format(key, counter[key]))

        print()
        print('A = {0}'.format(self.handled_count / self.iteration_count))
        print('Potk = {0}'.format(2 * self.refused_count / self.iteration_count))
        print('Q = {0}'.format((self.iteration_count - 2 * self.refused_count) / self.iteration_count))
        print()
        print('Lq = {0}'.format(self.queue.sum_of_sizes / self.iteration_count))
        print('Lc = {0}'.format(self.queue.sum_of_middle_sizes / self.iteration_count))
        print()
        print('Wq = {0}'.format((self.queue.sum_of_sizes / self.handled_count)))
        print('Wc = {0}'.format(self.queue.sum_of_sizes/self.handled_count + (self.handlers[0].busy/self.handlers[0].task_count) + (self.handlers[1].busy/self.handlers[1].task_count)))
        print('Kkan1 = {0}'.format(self.handlers[0].busy / self.iteration_count))
        print('Kkan2 = {0}'.format(self.handlers[1].busy / self.iteration_count))

    def tick(self, count):
        self.current_tick += 1

        # если 2-й обработчик закончил выполнение и очередь не пуста
        # - назначить новую задачу
        handler_result = self.handlers[1].tick()
        if handler_result is not None:
            self.handled_count += 1
            if len(self.queue) > 0:
                task = self.queue.dequeue()
                self.handlers[1].set_task(task)

        # если 1-й обработчик закончил выполнение задачи
        # и 2-й обработчик не занят - передать задачу
        # если 2-й обработчик занят - в очередь
        # очередь занята - откинуть
        handler_result = self.handlers[0].tick()
        if handler_result is not None:
            if not self.handlers[1].is_busy():
                self.handlers[1].set_task(handler_result)
            else:
                if self.queue.has_place():
                    self.queue.enqueue(handler_result)
                else:
                    self.refused_count += 1

        # если пришла новая заявка, передать 1-му обработчику
        # если занят - отбросить
        source_result = self.source.tick()
        if source_result is not None:
            if not self.handlers[0].is_busy():
                self.handlers[0].set_task(source_result)
            else:
                self.refused_count += 1

        self.queue.tick()

        # состояния записываем в массив
        state = '{0}{1}{2}{3}'.format(
            str(self.source),
            str(self.handlers[0]),
            str(self.queue),
            str(self.handlers[1])
        )

        self.states.append(state)
