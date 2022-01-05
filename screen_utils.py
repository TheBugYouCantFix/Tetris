import pygame as pg
import sys

from utils import load_image


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

