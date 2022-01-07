import pygame as pg

from shapes import random_shape_type

from field import Field
from utils import colors, play_sound
from shape import Shape

from screen_utils import \
    game_over_screen, show_parameter, show_shape


def main():
    pg.init()

    cell_size = 30
    offset = 100
    size = Field.WIDTH * cell_size + 2 * offset, \
           Field.HEIGHT * cell_size + offset

    offset_x, offset_y = offset // 5, cell_size

    screen = pg.display.set_mode(size)
    pg.display.set_caption('Tetris')

    field = Field(screen, cell_size, offset_x, offset_y)

    timer = pg.time.Clock()
    FPS = 60

    ticks = 0
    speed = 30

    background_image = pg.image.load('./data/assets/bg.jpg')

    running = True

    shape_type = random_shape_type()
    next_shape_type = random_shape_type()

    shape = Shape(shape_type, field, next_shape_type)

    play_sound('./data/sounds/start.mp3')

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                key = event.key

                if key == pg.K_d or key == pg.K_RIGHT:
                    shape.move_right()
                if key == pg.K_a or key == pg.K_LEFT:
                    shape.move_left()
                if key == pg.K_s or key == pg.K_DOWN:
                    shape.fall()
                if key == pg.K_w or key == pg.K_UP:
                    shape.rotate_90deg_clockwise()
                if key == pg.K_SPACE:
                    shape.drop()

        screen.fill(colors.get('black'))
        # screen.blit(background_image, (0, 0))
        field.render()

        x, y = cell_size * field.WIDTH + offset_x + 20, offset_y + 50
        show_shape(screen, next_shape_type, x, y, cell_size)

        y = offset_y + 200
        show_parameter(screen, "Points", field.points, x, y)

        y = offset_y + 230
        show_parameter(screen, "Lines", field.lines, x, y)

        if shape.collided:

            if not shape.dropped:
                play_sound('data/sounds/hit.mp3')

            field.check_full_rows(shape)

            if shape.game_over():
                play_sound('data/sounds/game_over.wav')
                screen.fill(colors.get('black'))
                game_over_screen(size, screen, timer, FPS, field)

            shape.normalize_position()

            # creating new shape and generating type of a next shape
            shape_type = shape.next_type
            next_shape_type = random_shape_type()

            shape = Shape(shape_type, field, next_shape_type)

        if ticks >= speed:
            shape.fall()
            ticks = 0

        timer.tick(FPS)
        ticks += 1

        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
