import pygame

FPS = 60


class EmptyObject(pygame.sprite.Sprite):
    def __init__(self, position, size=(1, 1), path_sound=None):
        super().__init__()

        self.rect = pygame.Rect(position, size)
        if path_sound:
            self.sound = pygame.mixer.sound(path_sound)
        self.sound = None

    def get_position(self):
        return self.rect.x, self.rect.y

    def play_sound(self):
        if self.sound:
            self.sound.play()

    def get_size(self):
        return self.rect.size

    def get_rect(self):
        return self.rect

    def shift(self, position):
        self.rect.move_ip(*position)

    def update(self):
        self.play_sound()


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
    def __init__(self, position, path_image, collidepoint_type=None, path_sound=None, animation=None):
        self.image = pygame.image.load(path_image)

        super().__init__(position, self.image.get_size(), collidepoint_type, path_sound)

        if self.mask:
            self.image.set_masks(self.mask)

        if animation:
            self.frames = []
            self.cur_frame = animation[2] if len(animation) == 3 else 1

            self.speed_anim = FPS // animation[3] if len(animation) == 4 else 0
            self.counter_anim = 0

            self.col = animation[0]
            self.row = animation[1]

            self.rect.size = self.image.get_width() // self.col, self.image.get_height() // self.row

            for j in range(self.row):
                for i in range(self.col):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(self.image.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))
            self.image = self.frames[self.cur_frame]

        self.animation = animation

    def update(self, surface):
        super().update()

        if self.animation:
            self.counter_anim += 1

            if self.counter_anim >= self.speed_anim:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.counter_anim = 0

        surface.blit(self.image, self.get_position())


class VisibleMovingObject(VisibleObject):
    def __init__(self, position, path_image, collidepoint_type=None, path_sound=None, speed_move=1, animation=None):
        super().__init__(position, path_image, collidepoint_type, path_sound, animation)

        if type(speed_move) == int:
            speed_move = FPS // speed_move
            self.speed_move = (speed_move, speed_move)
        else:
            self.speed_move = (FPS // speed_move[0], FPS // speed_move[1])

    def move_x(self, strs=None):
        if strs:
            self.rect.move_ip(-self.speed_move[0], 0)
        else:
            self.rect.move_ip(self.speed_move[0], 0)

    def move_y(self, strs=None):
        if strs:
            self.rect.move_ip(0, -self.speed_move[1])
        else:
            self.rect.move_ip(0, self.speed_move[1])