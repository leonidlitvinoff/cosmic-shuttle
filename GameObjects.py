import pygame
import random
import math

FPS = 60


class EmptyObject(pygame.sprite.Sprite):
    """Пустой обьект"""

    def __init__(self, position, size=(1, 1), path_sound=None, tag='None',
                 name='None'):
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

    def __init__(self, position, path_image, path_sound=None, animation=None,
                 tag='None', name='None'):
        """Иницилизаця обьекта"""

        # Загрузка изображения
        if type(path_image) == str:
            self.image = pygame.image.load(path_image)
        else:
            self.image = path_image

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
        super().__init__(position, self.image.get_size(), path_sound, tag,
                         name)

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
                 animation=None, tag='None', name='None', always_moving=False):
        """Иницилизация обьекта"""

        # Иницилизация родителя
        super().__init__(position, path_image, path_sound, animation, tag,
                         name)

        # Сохранения движения по осям (x, y) в зависимости от типа
        if type(speed_move) in (int, float):
            speed_move = speed_move / FPS
            self.speed_move = (speed_move, speed_move)
        else:
            self.speed_move = (speed_move[0] / FPS,
                               speed_move[1] / FPS)

        # Счётчик скорости
        self.counter_speed = [0, 0]
        # Движение сохранение темп движения
        if always_moving:
            self.always_moving = always_moving
        else:
            self.always_moving = False

    def edit_speed_move(self, new_speed_move):
        """Изменение скорости обьекта"""

        self.speed_move = new_speed_move

    def move(self, shift):
        """Движение по осям"""

        x, y = 0, 0
        if shift[0]:
            # Ведём счёт
            self.counter_speed[0] += self.speed_move[0]

            if self.counter_speed[0] >= 1:
                # берём целое число и движемся по оси x
                x = int(self.counter_speed[0])

                # отнимаем от счётчика пройденый путь
                self.counter_speed[0] -= x

        if shift[1]:
            # Ведём счёт
            self.counter_speed[1] += self.speed_move[1]

            if self.counter_speed[1] >= 1:
                # берём целое число и движемся по оси y
                y = int(self.counter_speed[1])

                # отнимаем от счётчика пройденый путь
                self.counter_speed[1] -= y

        self.rect.move_ip((x * shift[0], y * shift[1]))

    def get_speed_move(self):
        """Возращяет скорость передвижения обьекта"""

        return self.speed_move

    def update(self, *arg, **kwargs):
        """Иницилизация"""

        # иницилизация родителя
        super().update(arg, kwargs)

        if self.always_moving:
            self.move(self.always_moving)


class GameObject(VisibleMovingObject):
    """Полнеценный игровой обьект со всемы функциями"""

    def __init__(self, position, path_image, path_sound=None, speed_move=0,
                 animation=None, time_life=None, hp=None, tag='None',
                 name='None', always_moving=False):
        """Иницилизация"""

        # Иницилизация родителя
        super().__init__(position, path_image, path_sound,
                         speed_move, animation, tag, name, always_moving)

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

    def get_hp(self):
        """Возвращяет hp обьекта"""

        return self.hp

    def get_time_life(self):
        """Возвращяет оставшееся время жизни обьекта"""

        return self.time_life

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


class RotatingGameObject(GameObject):
    def __init__(self, position, path_image, path_sound=None, speed_move=0,
                 animation=None, time_life=None, hp=None, tag='None',
                 name='None', always_moving=False, rotate=(1, pygame.mouse.get_pos)):
        super().__init__(position, path_image, path_sound, speed_move,
                         animation, time_life, hp, tag, name, always_moving)

        # Сохранения вращения
        self.rotate_speed = rotate[0]
        self.rotate_func = rotate[1]
        self.angle = 0
        self.old_image = self.image
        self.image = pygame.transform.rotate(self.old_image, self.angle)
        self.vector = (0, 0)

    def rotate(self):
        m_x, m_y = self.rotate_func()
        x, y = self.rect.center
        a, b = m_y - y, m_x - x
        c = (a ** 2 + b ** 2) ** 0.5
        self.vector = (b / c, a / c)
        self.angle = -math.degrees(math.atan2(m_y - y, m_x - x))
        self.image = pygame.transform.rotate(self.old_image, self.angle)

    def update(self, *arg, **kwargs):
        """Обновление обьекта"""

        super().update(arg, kwargs)

        self.rotate()


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
    def __init__(self, all_sprite, current_position=(0, 0),
                 traffic_restriction=(None, None), size=(0, 0),
                 path_sound=None,
                 flags=0, depth=0, display=0, tag='None',
                 name='None'):
        """Иницилизация камеры"""

        # Иницилизация родителей
        super().__init__((0, 0), size, path_sound, flags, depth,
                         display, tag, name)

        # Иницилизация новых плюшек
        self.traffic_restriction = traffic_restriction

        # Сохраняем ссылку на спрайты
        self.all_sprite = all_sprite
        self.shift_x, self.shift_y = 0, 0

        self.move((-current_position[0], -current_position[1]))

    def shift(self, shift_position):
        """Принудительный сдвиг камеры"""

        # Сдиг всех до точи отсчёта
        for sprite in self.all_sprite.sprites():
            sprite.shift((shift_position[0], shift_position[1]))

    def move(self, speed_move):
        """Движение по осям"""

        size_screen = self.screen.get_rect().size
        result = [False, False]
        shift_cor = [0, 0]

        if ((not self.traffic_restriction[0]) or
                (0 >= self.shift_x + speed_move[0] >= size_screen[0] - self.traffic_restriction[0])):
            result[0] = True
            shift_cor[0] = speed_move[0]
            self.shift_x += speed_move[0]

        if ((not self.traffic_restriction[1]) or
                (0 >= self.shift_y + speed_move[1] >= size_screen[1] - self.traffic_restriction[1])):
            result[1] = True
            shift_cor[1] = speed_move[1]
            self.shift_y += speed_move[1]

        if shift_cor[0] or shift_cor[1]:
            for sprite in self.all_sprite.sprites():
                sprite.shift(shift_cor)

        return result


class TargetCamera(MovingCamera):
    def __init__(self, all_sprite, target, traffic_restriction=(None, None),
                 size=(0, 0), path_sound=None, flags=0, depth=0, display=0,
                 tag='None', name='None'):
        """Иницилизация"""

        # Сохранение цели
        self.target = target

        # Иницилизация родителя
        super().__init__(all_sprite, target.get_position(),
                         traffic_restriction, size, path_sound, flags, depth,
                         display, tag, name)

        # Нормализация камеры и сдвижение игрока в центр камеры
        self.target.shift(tuple(map(lambda x: -x, self.target.get_position())))
        tar_w, tar_h = self.target.get_size()
        w, h = self.get_size()
        self.const = (w // 2 - tar_w // 2), (h // 2 - tar_h // 2)
        self.move((-(w // 2 - tar_w // 2), -(h // 2 - tar_h // 2)))
        self.target.shift(self.const)

    def sled(self, shift):
        """Движение камеры"""

        # Если цель не в центре сдвигаем цель
        if self.target.get_position()[0]:
            if (shift[0] == -1 and self.target.get_position()[0] > self.const[0]) or (shift[0] == 1 and self.target.get_position()[0] < self.const[0]):
                self.target.move((shift[0], 0))
                shift = (0, shift[1])
        if self.target.get_position()[1]:
            if (shift[1] == -1 and self.target.get_position()[1] > self.const[1]) or (shift[1] == 1 and self.target.get_position()[1] < self.const[1]):
                self.target.move((0, shift[1]))
                shift = (shift[0], 0)

        # Если цель в центре и она двигается то всё хорошо
        speed_move = self.target.get_speed_move()
        x, y = self.move((-(speed_move[0] * shift[0]),
                             -(speed_move[1] * shift[1])))

        # Если нет двигаем цель
        if not x:
            self.target.move((shift[0], 0))
        if not y:
            self.target.move((0, shift[1]))


class CameraMovingMouse(Camera):
    def __init__(self, traffic_restriction=(None, None),
                 current_position=(0, 0), size=(0, 0), path_sound=None,
                 flags=0, depth=0, display=0, speed_move=1,
                 max_speed_increase=2,
                 distance_start_move=5, tag='None', name='None'):
        super().__init__(current_position, size, path_sound, flags, depth,
                         display, tag, name)

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

# --------------------------------------
# Раздел модификаторов к базовым классам
# --------------------------------------


class Enemy(RotatingGameObject):

    """Класс вражеского обьекта"""

    def __init__(self, position, path_image, path_sound=None, speed_move=0,
                 animation=None, time_life=None, hp=None, tag='None',
                 name='None', always_moving=False, rotate=(1, pygame.mouse.get_pos), target=None, damage=0):
        """Иницилизация"""

        # Иницилизация родителя
        super().__init__(position, path_image, path_sound, speed_move,
                         animation, time_life, hp, tag, name, always_moving,
                         rotate)

        self.target = target
        self.damage = damage

    def get_damage(self):
        """Возращяет урон который может нанести обьект"""

        return self.damage

    def update(self, *arg, **kwargs):
        """Обновление обьекта"""

        # Обновление родителя
        super().update(arg, kwargs)

        # Двигается по осям до персонажа
        tar_x, tar_y = self.target.get_position()
        x, y = self.get_position()
        shift = [0, 0]
        if tar_x > x:
            shift[0] = 1
        elif tar_x < x:
            shift[0] = -1
        if tar_y > y:
            shift[1] = 1
        elif tar_y < y:
            shift[1] = -1
        self.move(shift)


class Person(RotatingGameObject):
    def shoot(self):
        x, y = 0, 0
        if self.angle > 0:
            y = -1
        elif self.angle < 0:
            y = 1
        if 0 < self.angle < 90 or 0 > self.angle > -90:
            x = 1
        elif 90 < self.angle < 180 or -90 > self.angle > -180:
            x = -1
        a = VisibleMovingObject(self.get_position(), path_image=pygame.transform.rotozoom(pygame.image.load('Data\\Image\\bullet.png'), self.angle, 0.1), speed_move=(10000 * abs(self.vector[0]), 10000 * abs(self.vector[1])), always_moving=(x, y))
        a.damage = 1
        return a
