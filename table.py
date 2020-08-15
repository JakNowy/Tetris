from copy import deepcopy
from figures import Figure
from utils import RetryOnException, CollisionError


class Field:

    def __init__(self):
        self.value = ' '

    def __repr__(self):
        return self.value


class Row(list):

    def __init__(self, range_cols):
        self.fields = [Field() for _ in range(range_cols)]
        super(Row, self).__init__()


class Table:

    def __init__(self, range_cols=20, range_rows=20):
        self._range_cols = range_cols
        self._range_rows = range_rows
        self.grid = [Row(range_cols) for _ in range(range_rows)]

        self.points = set()
        self.figure = None

    @RetryOnException(IndexError)
    def spawn_figure(self):
        self.figure = Figure(self._range_cols)
        self.check_colision(self.figure.points)
        self.points.update(self.figure.points)
        self.update_frame(self.points, '*')
        return self.figure

    def move_down(self):
        self.figure_old = deepcopy(self.figure)
        new_points = self.figure.move_down()
        self.check_colision(new_points)
        self.update_frame(self.figure_old.points, ' ')
        self.update_frame(new_points, '*')

    def check_colision(self, points):
        for point in points:
            if point in self.points:
                raise CollisionError

    def display_frame(self):
        print(f'  {list(range(10))}')
        for index, row in enumerate(self.grid):
            print(f'{index:2d}{row.fields}')

    def update_frame(self, points, value):
        for x, y in points:
            self.grid[y].fields[x].value = value

    def rotate_figure(self):
        self.update_frame(self.figure.points, ' ')
        direction_key = input('Rotate:\n')
        points = self.figure.rotate(direction_key)

        self.update_frame(points, '*')


table = Table()
table.spawn_figure()
while True:
    table.rotate_figure()
    try:
        table.move_down()
    except CollisionError:
        pass
    table.display_frame()
