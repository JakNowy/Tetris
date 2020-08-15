from figures import Figure


class Field:

    def __init__(self):
        self.X = None
        self.Y = None
        self.value = ' '

    def __str__(self):
        return self.value


class Row(list):

    def __init__(self, range_X):
        self.fields = [Field() for _ in range(range_X)]
        super(Row, self).__init__()

    def __str__(self):
        return ''.join([field.value for field in self.fields])

    def __repr__(self):
        return self.fields


class Table:

    def __init__(self, range_X=20, range_Y=20):
        self.range_X = range_X
        self.range_Y = range_Y
        self.grid = [Row(range_X) for _ in range(range_Y)]
        self.figure = None

    def spawn_figure(self):
        self.figure = Figure(self.range_X)
        self.grid[self.figure.Y].fields[self.figure.X] = '*'

    def display_frame(self):
        for index, row in enumerate(self.grid):
            print(f'{index}|{row}|')


table = Table()
table.spawn_figure()
table.display_frame()
