import random

from utils import BoundCollisionError


class Shape:
    def __init__(self, shape=None):

        # Fields relative to the figure centroid
        # Must be iterable OF 2 dim tuples
        self.shape = shape or ((0, 0), (1, 0), (2, 0), (3, 0), (0, -1), (0, -2), (0, -3))


class Figure:

    def __init__(self, range_rows, range_cols, shape=None):
        self.range_rows = range_rows
        self.range_cols = range_cols
        self.centroid = (random.randint(0, range_cols), 0)
        self.rotations = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        self.rotation_index = 3
        self.rotation = self.rotations[self.rotation_index]
        self.on_bottom = False
        self.shape = shape.shape

    @property
    def points(self):
        return {self.calculate_coords(vector) for vector in self.shape if self.calculate_coords(vector)}

    def calculate_coords(self, vector: tuple) -> tuple:
        self.rotation = self.rotations[self.rotation_index]
        if self.rotation_index % 2 == 0:
            point = self.centroid[0] + (vector[0] * self.rotation[0]), self.centroid[1] + (vector[1] * self.rotation[1])
        else:
            point = self.centroid[0] + (vector[1] * self.rotation[0]), self.centroid[1] + (vector[0] * self.rotation[1])
        if point[0] < 0 or point[0] > self.range_cols - 1:
            raise BoundCollisionError
        if point[1] == self.range_rows - 1:
            self.on_bottom = True
        return point if point[1] in set(range(self.range_rows)) else None

    def rotate(self, key):
        if key == 's':
            if self.rotation_index < 3:
                self.rotation_index += 1
            else:
                self.rotation_index = 0

        else:
            if self.rotation_index > 0:
                self.rotation_index -= 1
            else:
                self.rotation_index = 3
        return self.move_down()

    def move(self, key):
        if key == 'a':
            self.centroid = (self.centroid[0] - 1, self.centroid[1])
        else:
            self.centroid = (self.centroid[0] + 1, self.centroid[1])
        return self.move_down()

    def move_down(self):
        self.centroid = (self.centroid[0], self.centroid[1] + 1)
        print(f'{self.centroid=}')
        return self.points
