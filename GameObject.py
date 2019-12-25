import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, position, size, sound_path=None):
        super().__init__()

        self.position = position
        self.size = size
        self.sound = pygame.mixer.music.load(sound_path)

    def play_sond(self):
        if self.sound:
            self.sound.play()

    def get_size(self):
        return self.size

    def get_position(self):
        return self.position
