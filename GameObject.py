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

        if self.mask:
            self.image.set_masks(self.mask)

    def draw_on_surface(self, surface, position=None):
        if position:
            surface.blit(self.image, position)
        else:
            surface.blit(self.image, self.rect)


class VisibleMovingObject(VisibleObject):
    def __init__(self, position, path_image, collidepoint_type=None, path_sound=None, speed_move=1):
        super().__init__(position, path_image, collidepoint_type, path_sound)

        if type(speed_move) == int:
            speed_move = FPS // speed_move
            self.speed_move = (speed_move, speed_move)
        else:
            self.speed_move = (FPS // speed_move[0], FPS // speed_move[1])

    def move_x(self):
        self.rect.move(self.speed_move[0], 0)

    def move_y(self):
        self.rect.move(0, self.speed_move[1])

    def update(self, surface):
        super().update()

        surface.blit(self.image)


class AnimatedVisibleObject(VisibleObject):
    def __init__(self, position, path_image, columns, rows, collidepoint_type=None, path_sound=None, cur_frame=0, speed_anim=1):
        super().__init__(position, path_image, collidepoint_type, path_sound)

        self.frames = []
        self.cur_frame = cur_frame

        self.speed_anim = FPS // speed_anim
        self.counter_anim = 0

        self.col = columns
        self.row = rows

        self.cut_sheet(self.image, columns, rows)
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, columns, rows):
        self.rect.size = sheet.get_width() // columns, sheet.get_height() // rows
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        super().update()

        self.counter_anim += 1

        if self.counter_anim >= self.speed_anim:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.counter_anim = 0

