import pygame
import random

FPS = 60


class EmptyObject(pygame.sprite.Sprite):

    """Пустой обьект"""

    def __init__(self, position, size=(1, 1), path_sound=None, tag='None', name='None'):
        """Иницилизация Обьекта"""
        # Иницилизация родителя
        super().__init__()

        # Иницилизация
        self.rect = pygame.Rect(position, size)
        self.name = name
        self.tag = tag

        # Если есть музыка, сохраняем её
        if path_sound:
            self.sound = pygame.mixer.sound(path_sound)
        else:
            self.sound = None

    def get_info(self):
        """Возращяет название обьекта"""

        return self.name

    def get_tag(self):
        """Возвращяет тег обьекта"""

        return self.tag

    def get_position(self):
        """Возращяет позицию обьекта"""

        return self.rect.x, self.rect.y

    def play_sound(self):
        """Проигрывает звук обьекта"""

        if self.sound:
            self.sound.play()

    def get_size(self):
        """Возращяет размер обьекта (w, h)"""

        return self.rect.size

    def get_rect(self):
        """Возращяет класс (pygame.Rect) с задаными параметрами"""

        return self.rect

    def set_radius(self, radius):
        """Устанавливает радиус обьекту"""

        self.r = radius

    def set_mask(self, mask):
        """Устонваливает маску обьекту, по стандарту из self.image"""

        self.mask = mask

    def shift(self, position):
        """Принудиьтельно сдвинуть обьект, на (x, y) пикселей"""

        self.rect.move_ip(*position)

    def update(self, *arg, **kwargs):
        """Обновление обьекта"""
        # Обновление родительских функций
        super().update(arg)

        # Проигрывание музыки
        self.play_sound()


class VisibleObject(EmptyObject):

    """Видимый обьект"""

    def __init__(self, position, path_image, path_sound=None, animation=None, tag='None', name='None'):
        """Иницилизаця обьекта"""

        # Загрузка изображения
        self.image = pygame.image.load(path_image)

        # Если включена анимация
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
                    self.frames.append(self.image.subsurface(
                        pygame.Rect(frame_location, (w, h))))
            self.image = self.frames[self.cur_frame]
        self.animation = animation

        # Иницилизация родителя
        super().__init__(position, self.image.get_size(), path_sound, tag, name)

    def set_mask(self, mask=None):
        """Установить маску обьету"""

        # Если не передали маску по стандарту получаем её с изображения
        if mask is None:
            self.mask = pygame.mask.from_surface(self.image)
        else:
            super().set_mask(mask)

    def get_surface(self):
        """Возвращяет изображение обьекта"""

        return self.image

    def disabled_alpha(self):
        """Отключения альфаканала"""

        self.image = self.image.convert()

    def play_animation(self):
        """Проигрывание анимации"""

        # Если анимация включена
        if self.animation:
            # Счётчик текушей анимации
            self.counter_anim += 1

            # Если скрость анимации прошла меняем картинку
            if self.counter_anim >= self.speed_anim:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.counter_anim = 0

    def update(self, *arg, **kwargs):
        """Обновления обьетка"""

        # Обновление родительских функций
        super().update()

        # Проигрывание анимации
        self.play_animation()


class VisibleMovingObject(VisibleObject):

    """Видимый обьект способный двигаться"""

    def __init__(self, position, path_image, path_sound=None, speed_move=1,
                 animation=None, tag='None', name='None'):
        """Иницилизация обьекта"""

        # Иницилизация родителя
        super().__init__(position, path_image, path_sound, animation, tag, name)

        # Сохранения движения по осям (x, y) в зависимости от типа
        if type(speed_move) in (int, float):
            speed_move = speed_move / FPS
            self.speed_move = (speed_move, speed_move)
        else:
            self.speed_move = (speed_move[0] / FPS,
                               speed_move[1] / FPS)

        # Счётчик скорости
        self.counter_speed = [0, 0]

    def edit_speed_move(self, new_speed_move):
        """Изменение скорости обьекта"""

        self.speed_move = new_speed_move

    def move_x(self, revers=False):
        """Движение по оси x"""

        # Ведём счёт
        self.counter_speed[0] += self.speed_move[0]

        if self.counter_speed[0] >= 1:

            # берём целое число и движемся по оси x
            roun = int(self.counter_speed[0])
            if revers:
                self.rect.move_ip(-roun, 0)
            else:
                self.rect.move_ip(roun, 0)

            # отнимаем от счётчика пройденый путь
            self.counter_speed[0] -= roun

    def move_y(self, revers=False):
        """Движение по оси y"""

        # Ведём счёт
        self.counter_speed[1] += self.speed_move[1]

        if self.counter_speed[1] >= 1:

            # берём целое число и движемся по оси y
            roun = int(self.counter_speed[1])
            if revers:
                self.rect.move_ip(0, -roun)
            else:
                self.rect.move_ip(0, roun)

            # отнимаем от счётчика пройденый путь
            self.counter_speed[1] -= roun

    def get_speed_move(self):
        """Возращяет скорость передвижения обьекта"""

        return self.speed_move


class GameObject(VisibleMovingObject):

    """Полнеценный игровой обьект со всемы функциями"""

    def __init__(self, position, path_image, path_sound=None, speed_move=0,
                 animation=None, time_life=None, hp=None, tag='None', name='None'):
        """Иницилизация"""

        # Иницилизация родителя
        super().__init__(position, path_image, path_sound,
                         speed_move, animation, tag, name)

        # Добавление новых возможностей
        self.time_life = time_life
        self.hp = hp

    def hit(self, damage):
        """Получение урона"""

        # Если существует hp отнимаем от него дамаг до смерти
        if self.hp:
            self.hp -= damage
            if self.hp <= 0:
                self.kill()
            return True
        else:
            return False

    def update_time_life(self):
        """Обновление время жизни"""

        # Если есть жизнь отнимаём после чего смерть
        if self.time_life is not None:
            if self.time_life == 0:
                self.time_life = None
                self.kill()
            else:
                self.time_life -= 1

    def update(self, *arg, **kwargs):
        """Обновление обьекта"""

        # Обновление родительских функций
        super().update()

        # Обновление время жизни
        self.update_time_life()


class Camera(EmptyObject):
    def __init__(self, current_position=(0, 0), size=(0, 0), path_sound=None,
                 flags=0, depth=0, display=0, tag='None', name='None'):
        self.screen = pygame.display.set_mode(size, flags, depth, display)

        """Иницилизация камеры"""

        # Иницилизация родителей
        super().__init__(current_position, self.screen.get_rect().size,
                         path_sound, tag, name)

    def get_screen(self):
        return self.screen


class MovingCamera(Camera):
    def __init__(self, traffic_restriction=(None, None),
                 current_position=(0, 0), size=(0, 0), path_sound=None,
                 flags=0, depth=0, display=0, speed_move=1, max_speed_increase=2,
                 distance_start_move=5, tag='None', name='None'):
        super().__init__(current_position, size, path_sound, flags, depth, display, tag, name)

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

        x, y = 0, 0

        up_bar = h * self.distance_start_move // 100
        left_bar = w * self.distance_start_move // 100
        down_bar = h * (100 - self.distance_start_move) // 100
        right_bar = w * (100 - self.distance_start_move) // 100

        if mouse_pos[0] < left_bar and self.dx < 0:
            x += round(self.speed_move[0] + self.speed_move[
                0] * self.max_speed_increase * (
                               left_bar - mouse_pos[0]) / left_bar)
        if mouse_pos[0] > right_bar and (
                not self.traf_x or self.dx > -self.traf_x + w):
            x -= round(self.speed_move[0] + self.speed_move[
                0] * self.max_speed_increase * (mouse_pos[0] - right_bar) / (
                               w - right_bar))
        if mouse_pos[1] < up_bar and self.dy < 0:
            y += round(self.speed_move[1] + self.speed_move[
                1] * self.max_speed_increase * (
                               up_bar - mouse_pos[1]) / up_bar)
        if mouse_pos[1] > down_bar and (
                not self.traf_y or self.dy > -self.traf_y + h):
            y -= round(self.speed_move[1] + self.speed_move[
                1] * self.max_speed_increase * (mouse_pos[1] - down_bar) / (
                               h - down_bar))

        for sprite in all_sprite.sprites():
            sprite.shift((x, y))

        self.dx += x
        self.dy += y


class TargetCamera(Camera):
    def __init__(self, target, size=(0, 0), path_sound=None,
                 flags=0, depth=0, display=0, tag='None', name='None'):
        """Иницилизация"""

        # Иницилизация родителя
        super().__init__(target.get_position(), size, path_sound,
                 flags, depth, display, tag, name)

        # Сохранение цели
        self.target = target

    def move(self, all_sprite, shift_cord):
        """Движение камеры"""

        # Принемаем скорость персонажа и двигаем всех относительно персонажа
        speed_move = self.target.get_speed_move()
        for sprite in all_sprite.sprites():
            sprite.shift((speed_move[0] * shift_cord[0],
                          speed_move[1] * shift_cord[1]))

    def update(self, all_sprite, shift_cord, *arg, **kwargs):
        """Обновление обьекта"""

        # Обновление родителя
        super().update(arg)

        # Обновление движения
        self.move(all_sprite, shift_cord)

# --------------------------------------
# Раздел модификаторов к базовым классам
# --------------------------------------
