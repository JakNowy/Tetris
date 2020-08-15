import random


class Figure:

    def __init__(self, range_X):
        self.shape = ((), (), (), )
        self.X = random.randint(0, range_X)
        self.Y = 0


class Shape:

    def __init__(self):
        pass