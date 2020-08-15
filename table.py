from figures import Figure, Shape
from utils import RetryOnException, CollisionError, BoundCollisionError, InvalidInputError


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
        self.score = 0
        self.game_over = False

    @RetryOnException(IndexError, BoundCollisionError)
    def spawn_figure(self, shape=None):

        self.figure = Figure(self._range_rows, self._range_cols, shape)
        points = self.figure.get_points
        self.check_block_colision(points)
        self.points.update(points)
        self.update_frame(self.points, '*')

    def display_frame(self):
        print(f'  {list(range(10))}')
        for index, row in enumerate(self.grid):
            print(f'{index:2d}{row.fields}')

    def update_frame(self, points, value):
        for x, y in points:
            self.grid[y].fields[x].value = value

    def check_block_colision(self, points):
        for point in points:
            if point in self.points:
                print(f'Collision point: {point}')
                raise CollisionError

    def move_or_rotate_figure(self, direction_key):
        oldpoints = self.figure.get_points
        points = self.figure.handle(direction_key)

        self.points = self.points.difference(oldpoints)
        self.check_block_colision(points)
        self.points.update(points)
        self.update_frame(oldpoints, ' ')
        self.update_frame(self.points, '*')

    def check_rows(self):
        for row in self.grid:
            values = [field.value for field in row.fields]
            if ' ' not in values:
                self.grid.remove(row)
                self.grid = [Row(self._range_cols)] + self.grid
                self.score += 1
                print(f'Row Completed! Your Score: {self.score}')

    def check_game_over(self):
        values = [field.value for field in self.grid[0].fields]
        if '*' in values:
            self.game_over = True



# Example shapes of a figure
shapes = list()
shapes.append(Shape(((0, 0), (-1, 0), (-1, -1))))
shapes.append(Shape(((0, 0), (1, 0), (2, 0), (3, 0), (0, -1))))
shapes.append(Shape(((0, 1), (0, 2), (0, 3), (0, 4), (0, 5))))

table = Table(range_rows=5)  # Consider passing range_rows=10 when testing
# table.spawn_figure(random.choice(shapes))  # Init of figure based on random shape
table.spawn_figure(shapes[2])  # Straight bars only to simplify score incrementation testing - it works.

while True:
    table.display_frame()
    direction_key = None
    while direction_key not in {'w', 's', 'a', 'd', 'x'}:
        if table.game_over:
            print('Game Over!')
            break
        direction_key = input('Type w/s to rotate or a/d to move right/left or x to pass:\n')
        if direction_key:
            try:
                table.move_or_rotate_figure(direction_key)
            except InvalidInputError:
                print('\n\nInvalid move! Please type again. \n\n')
            except CollisionError:
                table.spawn_figure(shapes[2])
            finally:
                table.check_rows()
    if table.figure.on_bottom:
        table.spawn_figure(shapes[2])
        # table.spawn_figure(random.choice(shapes))
