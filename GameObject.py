import pygame

FPS = 60


class EmptyPoint(pygame.sprite.Sprite):
    def __init__(self, position, path_sound=None):
        super().__init__()

        self.size = pygame.Rect(position, (1, 1))
        if path_sound:
            self.sound = pygame.mixer.sound(path_sound)
        self.sound = None

    def get_position(self):
        return self.size.x, self.size.y

    def play_sound(self):
        if self.sound:
            self.sound.play()

    def update(self):
        self.play_sound()


class EmptyObject(EmptyPoint):
    def __init__(self, position, size, path_sound=None):
        super().__init__(position, path_sound)

        self.size.size = size

    def get_size(self):
        return self.size.size

    def get_rect(self):
        return self.size

