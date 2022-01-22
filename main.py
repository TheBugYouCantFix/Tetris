import pygame as pg

from shapes import random_shape_type

from field import Field
from utils import colors
from shape import Shape

from db_manager import DbManager
from music_player import MusicPlayer

from config import \
    CELL_SIZE, OFFSET, FPS, points_step, SPEED_DELTA

from screen_utils import \
    start_screen, game_over_screen, show_parameter, show_shape, \
    set_icon, set_up_taskbar_image, show_background_image


def main():
    pg.init()

    mp = MusicPlayer()

    size = Field.WIDTH * CELL_SIZE + 2 * OFFSET, \
           Field.HEIGHT * CELL_SIZE + OFFSET  # 500x700

    offset_x, offset_y = OFFSET // 5, CELL_SIZE

    screen = pg.display.set_mode(size)
    pg.display.set_caption('Tetris')

    field = Field(screen, CELL_SIZE, offset_x, offset_y, mp)

    ticks = 0
    speed = 30

    points_for_next_speed_increase = points_step

    clock = pg.time.Clock()

    db = DbManager()

    set_icon()

    running = True

    shape_type = random_shape_type()
    next_shape_type = random_shape_type()

    shape = Shape(shape_type, field, next_shape_type, mp)

    start_screen(screen, clock, FPS)

    mp.play_bg_music()
    mp.play_sound('./data/sounds/start.mp3')

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
        show_background_image(screen)
        field.render()

        x, y = CELL_SIZE * field.WIDTH + offset_x + 20, offset_y + 50
        show_shape(screen, next_shape_type, x, y, CELL_SIZE)

        y = offset_y + 200
        show_parameter(screen, "Points", field.points, x, y)

        y = offset_y + 230
        show_parameter(screen, "Lines", field.lines, x, y)

        if shape.collided:

            if not shape.dropped:
                mp.play_sound('data/sounds/hit.mp3')

            field.check_full_rows(shape, field.points, points_for_next_speed_increase)

            if shape.game_over():
                mp.pause_bg_music()
                mp.play_sound('data/sounds/game_over.wav')
                screen.fill(colors.get('black'))

                score = field.points
                db.add_score(score)

                best_score = db.get_max_score()

                game_over_screen(screen, clock, FPS, field, score, best_score, mp)
                field.nullify_params()

            shape.normalize_position()

            # creating new shape and generating type of a next shape
            shape_type = shape.next_type
            next_shape_type = random_shape_type()

            shape = Shape(shape_type, field, next_shape_type, mp)

        if field.points >= points_for_next_speed_increase:
            speed -= SPEED_DELTA  # we extract the delta as the less the value of speed var is the faster shape falls
            points_for_next_speed_increase += points_step

            mp.play_sound('./data/sounds/speed_increase.mp3')

        if ticks >= speed:
            shape.fall()
            ticks = 0

        clock.tick(FPS)
        ticks += 1

        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    set_up_taskbar_image()
    main()
