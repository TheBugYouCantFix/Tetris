from random import choice

from cell import Cell
from utils import colors
from field import Field


# "*" = filled; "_" = empty


class Square:
    """
    **
    **
    """

    COLOR = colors.get('light yellow')
    WIDTH, HEIGHT = 2, 2

    FIELD = (
        (Cell.FILLED, Cell.FILLED),
        (Cell.FILLED, Cell.FILLED)
    )


class Line:
    # ****

    COLOR = colors.get('cyan')
    WIDTH, HEIGHT = 4, 1

    FIELD = [
        (Cell.FILLED, Cell.FILLED,
         Cell.FILLED, Cell.FILLED)
    ]


class ThreeOne:
    """
    ***
    _*_
    """

    COLOR = colors.get('purple')
    WIDTH, HEIGHT = 3, 2

    FIELD = (
        (Cell.FILLED, Cell.FILLED, Cell.FILLED),
        (Cell.EMPTY, Cell.FILLED, Cell.EMPTY)
    )


class OneOneTwo:
    """
    *_
    *_
    **
    """

    COLOR = colors.get('orange')
    WIDTH, HEIGHT = 2, 3

    FIELD = (
        (Cell.FILLED, Cell.EMPTY),
        (Cell.FILLED, Cell.EMPTY),
        (Cell.FILLED, Cell.FILLED)
    )


class OneTwoOne:
    """
    *_
    **
     _*
    """

    COLOR = colors.get('light green')
    WIDTH, HEIGHT = 2, 3

    FIELD = (
        (Cell.FILLED, Cell.EMPTY),
        (Cell.FILLED, Cell.FILLED),
        (Cell.EMPTY, Cell.FILLED)
    )


class Shape:
    SHAPES = (Square, Line, OneTwoOne, OneOneTwo, ThreeOne)

    def __init__(self, field):
        self.shape = choice(self.SHAPES)()
        self.field = field
        self.blocked = False

        self.row, self.col = 0, Field.WIDTH // self.shape.WIDTH

        self.set_shape()

    def set_shape(self, value=None):
        for i in range(self.row, self.row + self.shape.HEIGHT):
            for j in range(self.col, self.col + self.shape.WIDTH):
                if value is None:
                    cell = self.shape.FIELD[i - self.row][j - self.col]

                    # if cell == Cell.FILLED:
                    #     cell = self.shape.COLOR

                    self.field.set_cell(i, j, cell)
                else:
                    self.field.set_cell(i, j, value)

    def get_shape(self):
        return self.shape

    def move(func):
        def wrap(self, *args, **kwargs):
            self.set_shape(Cell.EMPTY)
            func(self, *args, **kwargs)
            self.set_shape()

        return wrap

    @move
    def fall(self):
        if self.row + self.shape.HEIGHT < self.field.HEIGHT:
            self.row += 1

    @move
    def move_right(self):
        if self.col + self.shape.WIDTH < self.field.WIDTH:
            self.col += 1

    @move
    def move_left(self):
        if self.col - 1 >= 0:
            self.col -= 1

    def drop(self):
        for i in range(self.field.HEIGHT):
            self.fall()

    def turn_90deg_clockwise(self):
        pass