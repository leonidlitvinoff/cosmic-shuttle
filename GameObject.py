import pygame
from fractions import Fraction

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

    def update(self, *arg, **kwargs):
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

        if animation:
            self.frames = []
            self.cur_frame = animation[2] if len(animation) == 3 else 1

            self.speed_anim = FPS // animation[3] if len(animation) == 4 else 0
            self.counter_anim = 0

            self.col = animation[0]
            self.row = animation[1]

            w, h = self.image.get_width() // self.col, self.image.get_height() // self.row

            for j in range(self.row):
                for i in range(self.col):
                    frame_location = (w * i, h * j)
                    self.frames.append(self.image.subsurface(pygame.Rect(frame_location, (w, h))))
            self.image = self.frames[self.cur_frame]
        self.animation = animation

        super().__init__(position, self.image.get_size(), collidepoint_type, path_sound)

        if self.mask:
            self.image.set_masks(self.mask)

    def update(self, *arg, **kwargs):
        super().update()

        if self.animation:
            self.counter_anim += 1

            if self.counter_anim >= self.speed_anim:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.counter_anim = 0


class VisibleMovingObject(VisibleObject):
    def __init__(self, position, path_image, collidepoint_type=None, path_sound=None, speed_move=1, animation=None):
        super().__init__(position, path_image, collidepoint_type, path_sound, animation)

        if type(speed_move) == int:
            speed_move = Fraction(speed_move, FPS)
            speed_move = speed_move.numerator, speed_move.denominator
            self.speed_move = (*speed_move, *speed_move)
        else:
            a = Fraction(speed_move[0], FPS)
            a = a.numerator, a.denominator

            b = Fraction(speed_move[1], FPS)
            b = b.numerator, b.denominator

            self.speed_move = (*a, *b)

        self.counter_speed = [0, 0]

    def move_x(self, strs=None):
        self.counter_speed[0] += 1
        if self.counter_speed[0] == self.speed_move[1]:
            if strs:
                self.rect.move_ip(-self.speed_move[0], 0)
            else:
                self.rect.move_ip(self.speed_move[0], 0)
            self.counter_speed[0] = 0

    def move_y(self, strs=None):
        self.counter_speed[1] += 1
        if self.counter_speed[1] == self.speed_move[3]:
            if strs:
                self.rect.move_ip(0, -self.speed_move[2])
            else:
                self.rect.move_ip(0, self.speed_move[2])
            self.counter_speed[1] = 0


class GameObject(VisibleMovingObject):
    def __init__(self, position, path_image, collidepoint_type=None, path_sound=None, speed_move=0, animation=None, time_life=None, hp=None):
        super().__init__(position, path_image, collidepoint_type, path_sound, speed_move, animation)

        self.time_life = time_life
        self.hp = hp

    def hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def update(self, *arg, **kwargs):
        super().update()

        if self.time_life is not None:
            if self.time_life == 0:
                self.kill()
            else:
                self.time_life -= 1