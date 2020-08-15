from copy import deepcopy
from figures import Figure
from utils import RetryOnException, CollisionError


class Field:

    def __init__(self):
        self.value = ' '

    def __repr__(self):
        return self.value


class Row:

    def __init__(self, range_cols):
        self.fields = [Field() for _ in range(range_cols)]


class Table:

    def __init__(self, range_cols=20, range_rows=20):
        self._range_cols = range_cols
        self._range_rows = range_rows
        self.grid = [Row(range_cols) for _ in range(range_rows)]

        self.points = set()
        self.figure = None

    @RetryOnException(IndexError)
    def spawn_figure(self):
        self.figure = Figure(self._range_rows, self._range_cols)
        self.check_colision(self.figure.points)
        self.points.update(self.figure.points)
        self.update_frame(self.points, '*')
        return self.figure

    def display_frame(self):
        print(f'  {list(range(10))}')
        for index, row in enumerate(self.grid):
            print(f'{index:2d}{row.fields}')

    def update_frame(self, points, value):
        for x, y in points:
            self.grid[y].fields[x].value = value

    def check_colision(self, points):
        for point in points:
            if point in self.points:
                print(f'Collision point: {point}')
                raise CollisionError

    def move_or_rotate_figure(self, direction_key):
        old_points = deepcopy(self.figure.points)
        if direction_key in {'w', 's'}:
            points = self.figure.rotate(direction_key)
        elif direction_key in {'a', 'd'}:
            points = self.figure.move(direction_key)
        else:
            points = self.figure.move_down()

        self.points = self.points.difference(old_points)
        self.check_colision(points)
        self.points.update(points)
        self.update_frame(old_points, ' ')
        self.update_frame(self.points, '*')


table = Table()
table.spawn_figure()
while True:
    table.display_frame()
    direction_key = None
    while direction_key not in {'w', 's', 'a', 'd', 'x'}:
        direction_key = input('Type w/s to rotate or a/d to move right/left or x to pass:\n')
    try:
        table.move_or_rotate_figure(direction_key)
    except CollisionError:
        print('colission')
