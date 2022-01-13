import pygame as pg


class MusicPlayer:
    def __init__(self):
        pg.mixer.init()

    def play_sound(self, file):
        sound = pg.mixer.Sound(file)
        sound.play()

    def play_bg_music(self):
        pg.mixer.music.load('./data/sounds/bg_music.mp3')
        pg.mixer.music.set_volume(0.05)
        pg.mixer.music.play(-1)

    def pause_bg_music(self):
        pg.mixer.music.stop()