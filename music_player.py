import pygame as pg


class MusicPlayer:
    def __init__(self):
        pg.mixer.init()
        self.sound_dict = {}

    def play_sound(self, file):
        if file in self.sound_dict:
            sound = self.sound_dict[file]
        else:
            sound = pg.mixer.Sound(file)

        sound.play()

    @staticmethod
    def play_bg_music():
        pg.mixer.music.load('./data/sounds/bg_music.mp3')
        pg.mixer.music.set_volume(0.05)
        pg.mixer.music.play(-1)

    @staticmethod
    def pause_bg_music():
        pg.mixer.music.stop()