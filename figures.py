import random


class Shape:

    # shape = ((0, 0), (1, 0), (2, 0), (3, 0), (3, 1))
    shape = ((0, 0), (1, 0), (2, 0), (3, 0), (0, -1), (0, -2), (0, -3))


class Figure(Shape):

    def __init__(self, range_cols):
        self.centroid = (random.randint(0, range_cols), 0)
        self.rotations = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        self.rotation_index = 3
        self.rotation = self.rotations[self.rotation_index]

    @property
    def points(self):
        return {self.calculate_coords(vector) for vector in self.shape}

    def calculate_coords(self, vector: tuple) -> tuple:
        self.rotation = self.rotations[self.rotation_index]
        if self.rotation_index % 2 == 0:
            return self.centroid[0] + (vector[0] * self.rotation[0]), self.centroid[1] + (vector[1] * self.rotation[1])
        else:
            return self.centroid[0] + (vector[1] * self.rotation[0]), self.centroid[1] + (vector[0] * self.rotation[1])

    def rotate(self, key):
        if key == 'a':
            if self.rotation_index < 3:
                self.rotation_index += 1
            else:
                self.rotation_index = 0

        elif key == 'd':
            if self.rotation_index > 0:
                self.rotation_index -= 1
            else:
                self.rotation_index = 3
        return self.points

    def move_down(self):
        print(self.centroid)
        self.centroid = (self.centroid[0], self.centroid[1] + 1)
        print(self.centroid)
        return self.points

