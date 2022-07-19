# Задание № 1


def is_even_fast(value: int):
    """
    Эффективный алгорим провреки целочисленного значения на четность.
    Побитовые операции выполняются гораздо быстре арифметических.
    Недостаток: неочевидность решения.
    """
    return value & 1 == 0


def is_even_slow(value: int):
    """
    Альтернативный алгоритм провреки целочисленного значения на четность.
    Выполняется дольше исходного и быстрого алгоритмов, но не использует побитовые операции.
    """
    value = abs(value)
    if value in [0, 2]:
        return True
    value = 0.5 * value
    return value == int(value)


# Задание № 2

from collections import deque


class NaiveCircularBuffer:
    """
    Простейший циклический буффер на основе списка.
    params: size - размер буффера
    methods: enqueue(*values) - добавляет элементы в очередь
             dequeue() - извлекает следующий элемент из очереди

    В качестве контейнера используется список.
    Для удаления данных используется неэффективный метод pop(0),
    смещающий все элементы списка на одну позицию по направлению к началу.
    """

    def __init__(self, size: int):
        if size < 1:
            raise ValueError('Buffer size should not be less than 1!')
        self.size = size
        self.queue = []

    def __repr__(self):
        return str(self.queue)

    @property
    def is_full(self):
        return len(self.queue) == self.size

    @property
    def head_index(self):
        return 0

    def enqueue(self, *values):
        for value in values:
            if self.is_full:
                self.queue.pop(0)
            self.queue.append(value)

    def dequeue(self):
        """ Возвращает элемент из буффера согласно принципу FIFO"""
        return self.queue[self.head_index]


class ListCircularBuffer(NaiveCircularBuffer):
    """
    В качестве контейнера используется список ограниченного размера.
    Элементы списка модифицируются позиционно, что значительно эффективнее
    по сравнению с базовой реализацией
    """

    def __init__(self, size: int):
        super().__init__(size)
        self.__insert_index = 0

    def enqueue(self, *values):
        for value in values:
            if self.__insert_index >= self.size:
                self.__insert_index = 0

            if self.is_full:
                self.queue[self.__insert_index] = value
            else:
                self.queue.append(value)

            self.__insert_index += 1

    @property
    def head_index(self):
        if self.is_full:
            if self.__insert_index > self.size:
                return max(1, self.size - 1)
            elif self.__insert_index == self.size:
                return 0
            else:
                return self.__insert_index
        return 0


class QueueCircularBuffer(NaiveCircularBuffer):
    """
    Альтернативный циклический буффер на основе коллекции deque.
    Коллекция реализована на С и предоставляет эффективные методы модификации очереди
    как с правой, так и с левой стороны.
    """

    def __init__(self, size: int):
        super().__init__(size)
        self.queue = deque(maxlen=size)
        self.__count_added = 0

    def enqueue(self, *values):
        for value in values:
            self.__count_added += 1

            if self.is_full:
                self.queue.appendleft(value)
            else:
                self.queue.append(value)

    @property
    def head_index(self):
        sub = self.__count_added % self.size
        if self.__count_added >= 2 * self.size:
            sub = 1
        return self.size - sub


def test_buffer(buffer_class):
    buffer = buffer_class(size=3)
    buffer.enqueue(1, 2, 3, 4)
    assert 4 in buffer.queue
    assert buffer.dequeue() == 2
    buffer.enqueue(5, 6)
    assert buffer.dequeue() == 4
    buffer.enqueue(7, 8, 9)
    assert buffer.dequeue() == 7


test_buffer(NaiveCircularBuffer)
test_buffer(ListCircularBuffer)
test_buffer(QueueCircularBuffer)

# Задание № 3

"""
Ввиду отсутствия дополнительных данных, следует предположить,
что сортируемые числа могут быть вещественными.

Для решения такой обобщенной задачи выбран алгоритм быстрой сортировки.
Это рекурсивный алгоритм, позволяющий отсортировать заданную последовательность "на месте"
без дополнительных затрат памяти и времени на ее аллокацию (не создаются структуры данных).
В худшем случае сложность данного алгоритма будет порядка O(n^2), в среднем - О(nLogN)
Произвольный выбор опороного элемента значительно снижает вероятность возникновения худшего случая.

Одним из недостатков этого алгоритма является потенциальная возможность переполнения стека вызовов
из-за большой глубины рекурсии.

"""

from random import randint


def quick_sort(data: list, start: int, end: int):
    if len(data) < 2 or start >= end:
        return

    pivot = data[randint(start, end)]

    i, j = start, end

    while i <= j:
        while data[i] < pivot:
            i += 1
        while data[j] > pivot:
            j -= 1

        if i <= j:
            data[i], data[j] = data[j], data[i]
            i, j = i + 1, j - 1

    quick_sort(data, start, j)
    quick_sort(data, i, end)


def sort_numbers(data: list):
    quick_sort(data, 0, len(data) - 1)


numbers = [-5, -2, 9, 2, 2, 9, -7, 6, -6, -8]
sort_numbers(numbers)
assert numbers == [-8, -7, -6, -5, -2, 2, 2, 6, 9, 9]
