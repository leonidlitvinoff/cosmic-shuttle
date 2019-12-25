import pygame

FPS = 60


class GameObject(pygame.sprite.Sprite):

    """Абстрактный класс. Предстовляет из себя простой игровой обьект"""

    def __init__(self, position, sound_path=None):
        super().__init__()

        self.position = position
        self.sound = pygame.mixer.music.load(sound_path)

    def play_sond(self):
        if self.sound:
            self.sound.play()

    def get_position(self):
        return self.position

    def update(self):
        pass