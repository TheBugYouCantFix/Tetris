from cell import Cell
from utils import colors

from random import choice

# "*" = filled; "_" = empty


class Square:
    """
    **
    **
    """

    COLOR = colors.get('light yellow')
    WIDTH, HEIGHT = 2, 2

    FIELD = [
        [Cell.FILLED, Cell.FILLED],
        [Cell.FILLED, Cell.FILLED]
    ]


class Line:
    # ****

    COLOR = colors.get('cyan')
    WIDTH, HEIGHT = 4, 1

    FIELD = [
        [Cell.FILLED, Cell.FILLED,
         Cell.FILLED, Cell.FILLED]
    ]


class ThreeOne:
    """
    * * *
    _ * _
    """

    COLOR = colors.get('purple')
    WIDTH, HEIGHT = 3, 2

    FIELD = [
        [Cell.FILLED, Cell.FILLED, Cell.FILLED],
        [Cell.EMPTY, Cell.FILLED, Cell.EMPTY]
    ]


class OneThree:
    """
    _ _ *
    * * *
    """

    COLOR = colors.get('orange')
    WIDTH, HEIGHT = 3, 2

    FIELD = [
        [Cell.EMPTY, Cell.EMPTY, Cell.FILLED],
        [Cell.FILLED, Cell.FILLED, Cell.FILLED]
    ]

class OneThreeMirrored:
    """
    * _ _
    * * *
    """

    COLOR = colors.get('light green')
    WIDTH, HEIGHT = 3, 2

    FIELD = [
        [Cell.FILLED, Cell.EMPTY, Cell.EMPTY],
        [Cell.FILLED, Cell.FILLED, Cell.FILLED]
    ]


class TwoTwo:
    """
    _ * *
    * * _
    """

    COLOR = colors.get('green')
    WIDTH, HEIGHT = 3, 2

    FIELD = [
        [Cell.EMPTY, Cell.FILLED, Cell.FILLED],
        [Cell.FILLED, Cell.FILLED, Cell.EMPTY]
    ]


class TwoTwoMirrored:
    """
    * * _
    _ * *
    """

    COLOR = colors.get('red')
    WIDTH, HEIGHT = 3, 2

    FIELD = [
        [Cell.FILLED, Cell.FILLED, Cell.EMPTY],
        [Cell.EMPTY, Cell.FILLED, Cell.FILLED]
    ]


SHAPES = (
        Square, Line, ThreeOne, OneThree, OneThreeMirrored, TwoTwo, TwoTwoMirrored
    )


def random_shape_type():
    return choice(SHAPES)