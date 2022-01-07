import pygame as pg
import sys

from utils import load_image
from utils import colors
from cell import Cell


def show_shape(screen, shape_type, x, y, cell_size):
    offset = 20

    color = shape_type.COLOR
    border_color = colors.get('white')

    for i in range(shape_type.START_HEIGHT):
        for j in range(shape_type.START_WIDTH):

            bbox = (
                x + cell_size * j + offset,
                y + cell_size * i + offset,
                cell_size, cell_size
            )

            if shape_type.START_POS[i][j] == Cell.FILLED:
                pg.draw.rect(screen, color, bbox)

            pg.draw.rect(screen, border_color, bbox, 1)

    pg.draw.rect(
        screen, border_color, (
            x, y,
            cell_size * shape_type.START_WIDTH + 2 * offset,
            cell_size * shape_type.START_HEIGHT + 2 * offset
        ), 3
    )


def show_parameter(screen, name, parameter, x, y):
    text = f"{name}: {parameter}"
    font = pg.font.Font(None, 30)

    text_rendered = font.render(text, 1, pg.Color('white'))

    offset = 10

    rect = text_rendered.get_rect()
    rect.x = x - offset
    rect.y = y - offset

    rect.width += offset
    rect.height += offset

    # pg.draw.rect(screen, colors.get('white'), rect, 1)

    screen.blit(text_rendered, rect)


def terminate():
    pg.quit()
    sys.exit()


def game_over_screen(screen_size, screen, clock, fps, field):
    text = ["Game over"]

    font = pg.font.Font(None, 50)
    text_coord = 250

    for line in text:
        string_rendered = font.render(line, 1, pg.Color('white'))
        rect = string_rendered.get_rect()
        text_coord += 10
        rect.top = text_coord
        rect.x = 10
        text_coord += rect.height
        screen.blit(string_rendered, rect)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                field.clear()
                return

        pg.display.flip()
        clock.tick(fps)
