from copy import deepcopy

from cell import Cell
from field import Field
from shapes import SHAPES


class Shape:

    for shape in SHAPES:
        shape.START_POS = shape.FIELD
        shape.START_WIDTH, shape.START_HEIGHT = shape.WIDTH, shape.HEIGHT

    def __init__(self, shape_type, field, next_type):
        self.shape = shape_type()
        self.field = field

        self.next_type = next_type

        self.collided = False
        self.coordinates = []

        self.row, self.col = 0, (Field.WIDTH - self.shape.WIDTH) // 2

        self.field.points += 4  # 4 is the amount of cells in every shape

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

    def right_collision(self):
        for i in range(self.row, self.row + self.shape.HEIGHT):
            for j in range(self.col + 1, self.col + self.shape.WIDTH + 1):
                if self.shape.FIELD[i - self.row][j - self.col - 1] == Cell.FILLED and \
                        (j == self.col + self.shape.WIDTH or
                         self.shape.FIELD[i - self.row][j - self.col] == Cell.EMPTY) and \
                        self.field.get_cell(i, j) != Cell.EMPTY:
                    return True

        return False

    def left_collision(self):
        for i in range(self.row, self.row + self.shape.HEIGHT):
            for j in range(self.col - 1, self.col + self.shape.WIDTH - 1):
                if self.shape.FIELD[i - self.row][j - self.col + 1] == Cell.FILLED and \
                        (j == self.col - 1 or
                         self.shape.FIELD[i - self.row][j - self.col] == Cell.EMPTY) and \
                        self.field.get_cell(i, j) != Cell.EMPTY:
                    return True

        return False

    def bottom_collisions(self, row, col):
        return self.field.get_cell(row, col) != Cell.EMPTY and \
               self.field.get_cell(row + 1, col) != Cell.EMPTY and \
               self.shape.FIELD[row - self.row][col - self.col] == Cell.FILLED and \
               (row == self.row + self.shape.HEIGHT - 1 or
                self.shape.FIELD[row - self.row + 1][col - self.col] == Cell.EMPTY)

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

    def move_right(self):
        if not self.right_collision() and not self.collided:
            self.erase_previous_pos()
            if self.col + self.shape.WIDTH < self.field.WIDTH:
                self.col += 1
                self.set_shape()

    def move_left(self):
        if not self.left_collision() and not self.collided:
            self.erase_previous_pos()
            if self.col - 1 >= 0:
                self.col -= 1
                self.set_shape()

    def drop(self):
        for i in range(self.field.HEIGHT):
            self.fall()

        self.collided = True

    @staticmethod
    def rotated_arr(arr):
        # rotates array 90 degrees clockwise
        return list(zip(*arr[::-1]))

    def rotate_90deg_clockwise(self):
        shape_type = type(self.shape)
        old_position = deepcopy(shape_type.FIELD)

        if shape_type.HEIGHT > shape_type.WIDTH and \
                self.col + self.shape.WIDTH > self.field.WIDTH - (shape_type.HEIGHT - shape_type.WIDTH):
            return

        shape_type.FIELD = self.rotated_arr(shape_type.FIELD)
        shape_type.WIDTH, shape_type.HEIGHT = shape_type.HEIGHT, shape_type.WIDTH

        self.erase_previous_pos()

        leave_loop = False

        # checking if there are no collisions with other shapes after rotation
        for i in range(self.row, self.row + self.shape.HEIGHT):
            for j in range(self.col, self.col + self.shape.WIDTH):
                if self.field.get_cell(i, j) != Cell.EMPTY and \
                        self.shape.FIELD[i - self.row][j - self.col] == Cell.FILLED:
                    shape_type.FIELD = old_position
                    shape_type.WIDTH, shape_type.HEIGHT = shape_type.HEIGHT, shape_type.WIDTH
                    leave_loop = True
                    break

            if leave_loop:
                break

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
