import pygame

FPS = 60


class EmptyPoint(pygame.sprite.Sprite):
    def __init__(self, position, path_sound=None):
        super().__init__()

        self.rect = pygame.Rect(position, (1, 1))
        if path_sound:
            self.sound = pygame.mixer.sound(path_sound)
        self.sound = None

    def get_position(self):
        return self.rect.x, self.rect.y

    def play_sound(self):
        if self.sound:
            self.sound.play()

    def update(self):
        self.play_sound()


class EmptyObject(EmptyPoint):
    def __init__(self, position, size, path_sound=None):
        super().__init__(position, path_sound)

        self.rect.size = size

    def get_size(self):
        return self.rect.size

    def get_rect(self):
        return self.rect


class TransparentObject(EmptyObject):
    def __init__(self, position, size, collidepoint_type=None, path_sound=None):
        super().__init__(position, size, path_sound)

        self.mask = None
        self.radius = None

        if collidepoint_type:
            if type(collidepoint_type) == str:
                self.mask = pygame.mask.from_surface(pygame.image.load(collidepoint_type))
            elif type(collidepoint_type) == int:
                self.radius = collidepoint_type
            elif len(collidepoint_type) == 2 and type(collidepoint_type[0]) == str and type(collidepoint_type[1]) == int:
                self.mask = pygame.mask.from_surface(pygame.image.load(collidepoint_type[0]), threshold=collidepoint_type[1])


class VisibleObject(TransparentObject):
    def __init__(self, position, path_image, collidepoint_type=None, path_sound=None):
        self.image = pygame.image.load(path_image)

        super().__init__(position, self.image.get_size(), collidepoint_type, path_sound)

        self.image.set_masks(self.mask)

    def draw_on_surface(self, surface, position=None):
        if position:
            surface.blit(self.image, position)
        else:
            surface.blit(self.image, self.rect)


class VisibleMovingObject(VisibleObject):
    def __init__(self, position, path_image, collidepoint_type=None, path_sound=None, speed_move=1):
        self.image = pygame.image.load(path_image)

        super().__init__(position, self.image.get_size(), collidepoint_type, path_sound)

        self.image.set_masks(self.mask)

        if type(speed_move) == int:
            self.speed_move = (speed_move, speed_move)
        else:
            self.speed_move = tuple(speed_move)
