import pygame as pg

from cell import Cell


class Field:
    WIDTH = 10
    HEIGHT = 20

    def __init__(self, cell_size, offset_x, offset_y):
        self.cell_size = cell_size

        self.offset_x = offset_x
        self.offset_y = offset_y

        self.field = [
            [Cell.EMPTY for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)
        ]

    def get_field(self):
        return self.field

    def set_cell(self, row, col, value):
        if row in range(self.HEIGHT) and col in range(self.WIDTH):
            self.field[row][col] = value

    def get_cell(self, row, col,):
        if row in range(self.HEIGHT) and col in range(self.WIDTH):
            return self.field[row][col]

        return "Invalid coordinates"

    def is_empty(self, row, col) -> bool:
        return bool(self.field[row][col])

    def render(self, screen):
        line_size = 1
        border_color = pg.Color(255, 255, 255)

        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):

                bbox = (x * self.cell_size + self.offset_x,
                        y * self.cell_size + self.offset_y,
                        self.cell_size,
                        self.cell_size)

                cell = self.field[y][x]

                if cell != Cell.EMPTY:
                    pg.draw.rect(screen, cell, bbox)

                pg.draw.rect(screen, border_color, bbox, line_size)

    def clear(self):
        self.field = [
            [Cell.EMPTY for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)
        ]

    def push_rows_down(self):
        for i in range(self.HEIGHT - 1, 0, -1):
            self.field[i] = self.field[i - 1]

        self.field[0] = [Cell.EMPTY for _ in range(self.WIDTH)]

    def check_full_rows(self):
        # TODO: implement this function
        counter = 0
        start = None

        # detecting the amount of filled rows
        for i in range(self.HEIGHT):
            if all(j != Cell.EMPTY for j in self.field[i]):
                if counter == 0:
                    start = i

                counter += 1

            elif counter > 0:
                break

        if counter > 0:
            # emptying the filled rows
            for i in range(start, start + counter):
                self.field[i] = [Cell.EMPTY for _ in range(self.WIDTH)]

            for _ in range(counter):
                self.push_rows_down()


