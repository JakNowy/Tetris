import random

from utils import BoundCollisionError, InvalidInputError


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
        self.points = []
        self.key = None

    def handle(self, key):
        try:
            rotation_index = self.rotate(key)
            centroid = self.move(key)
            centroid = self.move_down(centroid)
            rotation = self.rotations[rotation_index]
            points = {self.calculate_point(vector, rotation, rotation_index, centroid) for vector in self.shape if
                      self.calculate_point(vector, rotation, rotation_index, centroid)}
        except BoundCollisionError:
            raise InvalidInputError
        else:
            self.rotation_index = rotation_index
            self.centroid = centroid
            self.rotation = rotation
            self.points = points
        finally:
            return self.points

    @property
    def get_points(self):
        points = {self.calculate_point(vector, self.rotation, self.rotation_index, self.centroid) for vector in
                  self.shape if
                  self.calculate_point(vector, self.rotation, self.rotation_index, self.centroid)}
        return points

    def calculate_point(self, vector: tuple, rotation, rotation_index, centroid) -> tuple:

        if rotation_index % 2 == 0:
            point = centroid[0] + (vector[0] * rotation[0]), centroid[1] + (vector[1] * rotation[1])
        else:
            point = centroid[0] + (vector[1] * rotation[0]), centroid[1] + (vector[0] * rotation[1])

        if point[0] < 0 or point[0] > self.range_cols - 1:
            raise BoundCollisionError

        if point[1] == self.range_rows - 1:
            self.on_bottom = True

        return point if point[1] in set(range(self.range_rows)) else None

    def rotate(self, key):
        rotation_index = self.rotation_index
        if key == 's':
            if self.rotation_index < 3:
                rotation_index = self.rotation_index + 1
            else:
                rotation_index = 0

        elif key == 'w':
            if self.rotation_index > 0:
                rotation_index = self.rotation_index - 1
            else:
                rotation_index = 3
        return rotation_index

    def move(self, key):
        centroid = self.centroid
        if key == 'a':
            centroid = (self.centroid[0] - 1, self.centroid[1])
        if key == 'd':
            centroid = (self.centroid[0] + 1, self.centroid[1])
        return centroid

    def move_down(self, centroid):
        centroid = centroid[0], centroid[1] + 1
        return centroid
