import pygame as pg
import pygame_widgets as pw

import sys
import ctypes

from utils import colors
from cell import Cell

from pygame_widgets.button import Button


def set_up_taskbar_image():
    # This function lets you display the app icon in the taskbar(which isn't being displayed by default)
    app_id = u'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


path = './data/assets/icon.png'


def set_icon():
    icon = pg.image.load(path)
    pg.display.set_icon(icon)


background_image = pg.image.load('./data/assets/bg.jpg')


def show_background_image(screen):
    screen.blit(background_image, (0, 0))


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


def start_screen(screen, clock, fps):
    show_background_image(screen)

    title_font = pg.font.Font(None, 150)
    string = title_font.render("Tetris", 1, pg.Color('red'))
    rect = string.get_rect()
    rect.top = 100
    rect.x = 100
    screen.blit(string, rect)

    text_list = ['W, A, S, D / arrow keys - movement', 'Space - drop a shape']

    font = pg.font.Font(None, 35)
    text_coord = 300

    for line in text_list:
        string_rendered = font.render(line, 1, pg.Color('white'))
        rect = string_rendered.get_rect()
        text_coord += 10
        rect.top = text_coord
        rect.x = 50
        text_coord += rect.height
        screen.blit(string_rendered, rect)

    button = Button(
        screen, 130, 500, 200, 150, text='Start',
        fontSize=50, margin=20,
        inactiveColour=colors.get('orange'), radius=20,
    )

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                terminate()

        if button.clicked:
            return

        pw.update(events)
        button.draw()
        pg.display.flip()
        clock.tick(fps)


def game_over_screen(screen, clock, fps, field, score, best_score, mp):
    show_background_image(screen)

    game_over_font = pg.font.Font(None, 70)
    string = game_over_font.render("Game over", 1, pg.Color('red'))
    rect = string.get_rect()
    rect.top = 180
    rect.x = 100
    screen.blit(string, rect)

    text_list = [f"Score: {score}", f"Best score: {best_score}"]

    font = pg.font.Font(None, 50)
    text_coord = 250

    for line in text_list:
        string_rendered = font.render(line, 1, pg.Color('white'))
        rect = string_rendered.get_rect()
        text_coord += 10
        rect.top = text_coord
        rect.x = 120
        text_coord += rect.height
        screen.blit(string_rendered, rect)

    button = Button(
        screen, 130, 500, 200, 150, text='Retry',
        fontSize=50, margin=20,
        inactiveColour=colors.get('red'), radius=20,
    )

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                terminate()

        if button.clicked:
            field.clear()
            mp.play_bg_music()
            return

        pw.update(events)
        button.draw()
        pg.display.flip()
        clock.tick(fps)
