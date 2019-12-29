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


class Camera(EmptyObject):
    def __init__(self, current_position=(0, 0), size=(0, 0), path_sound=None, flags=0):
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        super().__init__(current_position, self.screen.get_rect().size, path_sound)

    def get_screen(self):
        return self.screen


class MovingCamera(Camera):
    def __init__(self, traffic_restriction=(None, None), current_position=(0, 0), size=(0, 0), path_sound=None, flags=0, speed_move=1, max_speed_increase=2, distance_start_move=5):
        super().__init__(current_position, size, path_sound, flags)

        if type(speed_move) == int:
            self.speed_move = (speed_move, speed_move)
        elif len(speed_move) == 2:
            self.speed_move = speed_move

        self.max_speed_increase = max_speed_increase
        self.distance_start_move = distance_start_move

        self.dx, self.dy = current_position

        self.traf_x, self.traf_y = traffic_restriction

    def update(self, all_sprite, *arg, **kwargs):
        super().update(arg, kwargs)

        mouse_pos = pygame.mouse.get_pos()
        w, h = self.get_size()
        all_sprite = all_sprite

        x, y = 0, 0

        up_bar = h * self.distance_start_move // 100
        left_bar = w * self.distance_start_move // 100
        down_bar = h * (100 - self.distance_start_move) // 100
        right_bar = w * (100 - self.distance_start_move) // 100

        if mouse_pos[0] < left_bar and self.dx < 0:
            x += round(self.speed_move[0] + self.speed_move[0] * self.max_speed_increase * (left_bar - mouse_pos[0]) / left_bar)
        if mouse_pos[0] > right_bar and (not self.traf_x or self.dx > -self.traf_x + w):
            x -= round(self.speed_move[0] + self.speed_move[0] * self.max_speed_increase * (mouse_pos[0] - right_bar) / (w - right_bar))
        if mouse_pos[1] < up_bar and self.dy < 0:
            y += round(self.speed_move[1] + self.speed_move[1] * self.max_speed_increase * (up_bar - mouse_pos[1]) / up_bar)
        if mouse_pos[1] > down_bar and (not self.traf_y or self.dy > -self.traf_y + h):
            y -= round(self.speed_move[1] + self.speed_move[1] * self.max_speed_increase * (mouse_pos[1] - down_bar) / (h - down_bar))

        for sprite in all_sprite.sprites():
            sprite.shift((x, y))

        self.dx += x
        self.dy += y


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