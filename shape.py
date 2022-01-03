from random import choice

from cell import Cell
from field import Field

from shapes import Square, Line, ThreeOne, OneThree, OneThreeMirrored, TwoTwo, TwoTwoMirrored


class Shape:
    SHAPES = (
        Square, Line, ThreeOne, OneThree, OneThreeMirrored, TwoTwo, TwoTwoMirrored
    )

    for shape in SHAPES:
        shape.START_POS = shape.FIELD
        shape.START_WIDTH, shape.START_HEIGHT = shape.WIDTH, shape.HEIGHT

    def __init__(self, field):
        self.shape = choice(self.SHAPES)()
        self.field = field
        self.collided = False
        self.coordinates = []

        self.row, self.col = 0, (Field.WIDTH - self.shape.WIDTH) // 2

        self.set_shape()

    def set_shape(self):
        for i in range(self.row, self.row + self.shape.HEIGHT):
            for j in range(self.col, self.col + self.shape.WIDTH):
                cell = self.shape.FIELD[i - self.row][j - self.col]

                if cell == Cell.FILLED:
                    cell = self.shape.COLOR

                    self.field.set_cell(i, j, cell)
                    self.coordinates.append((i, j))

    def erase_previous_pos(self):
        self.coordinates = self.coordinates[-4:]  # there are 4 filled cells in every shape

        for row, col in self.coordinates:
            self.field.set_cell(row, col, Cell.EMPTY)

    def move(func):
        def wrap(self, *args, **kwargs):
            self.erase_previous_pos()
            func(self, *args, **kwargs)
            self.set_shape()

        return wrap

    def bottom_collisions(self, row, col):
        # print(row + 1 == self.row + self.shape.HEIGHT or
        #         self.shape.FIELD[row - self.row + 1][col - self.col] == Cell.EMPTY)
        return self.field.get_cell(row, col) != Cell.EMPTY and \
               self.field.get_cell(row + 1, col) != Cell.EMPTY and \
               (row == self.row + self.shape.HEIGHT - 1 or
                self.shape.FIELD[row - self.row + 1][col - self.col] == Cell.EMPTY)

    def side_collisions(self):
        for i in range(self.row, self.row + self.shape.HEIGHT):
            if self.field.get_cell(self.col, i) != Cell.EMPTY:

                # left collision
                if self.field.get_cell(i, self.col - 1) != Cell.EMPTY:
                    print('left')
                    return 'left'

                # right collision
                elif self.field.get_cell(i, self.col + self.shape.WIDTH + 1) != Cell.EMPTY:
                    print('right')
                    return 'right'

    def shape_collisions_detected(self):
        for i in range(self.row, self.row + self.shape.HEIGHT):
            for j in range(self.col, self.col + self.shape.WIDTH):
                if self.bottom_collisions(i, j):
                    return True

        return False

    def fall(self):
        if self.row + self.shape.HEIGHT < self.field.HEIGHT and \
                not self.shape_collisions_detected():
            self.erase_previous_pos()
            self.row += 1
            self.set_shape()
        else:
            self.collided = True

    @move
    def move_right(self):
        if self.col + self.shape.WIDTH < self.field.WIDTH and \
                self.side_collisions() != 'right':
            self.col += 1

    @move
    def move_left(self):
        if self.col - 1 >= 0 and \
                self.side_collisions() != 'left':
            self.col -= 1

    def drop(self):
        for i in range(self.field.HEIGHT):
            self.fall()

        self.collided = True

    def rotate_90deg_clockwise(self):
        shape_type = type(self.shape)
        shape_type.FIELD = list(zip(*shape_type.FIELD[::-1]))
        shape_type.WIDTH, shape_type.HEIGHT = shape_type.HEIGHT, shape_type.WIDTH
        self.erase_previous_pos()
        self.set_shape()

    def normalize_position(self):
        shape_type = type(self.shape)
        shape_type.WIDTH, shape_type.HEIGHT = shape_type.START_WIDTH, shape_type.START_HEIGHT
        shape_type.FIELD = shape_type.START_POS

    def game_over(self):
        for i in range(self.col, self.col + self.shape.WIDTH):
            if self.field.get_cell(0, i) == Cell.EMPTY:
                return False

        return True
