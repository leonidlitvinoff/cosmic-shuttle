import pygame
import GameObjects
import pygameMenu
import os
from random import randrange

ABOUT = ['Leonid  Litvinov',
         'Stepan  Fedorov']
COLOR_BACKGROUND = (255, 104, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
DIFFICULTY = ['EASY']
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (0, 0)

clock = None
main_menu = None
surface = None


def change_difficulty(value, difficulty):
    selected, index = value
    print('Selected difficulty: "{0}" ({1}) at index {2}'.format(selected,
                                                                 difficulty,
                                                                 index))
    DIFFICULTY[0] = difficulty


def random_color():
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def play_function(difficulty, font, test=False):
    assert isinstance(difficulty, (tuple, list))
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)

    # Define globals
    global main_menu
    global clock
    bg_color = random_color()
    main_menu.disable()
    main_menu.reset(1)

    # Путь до изображений к игре
    path_from_background = 'Data\\Image\\Map1.png'
    path_from_person = 'Data\\Image\\person.png'
    path_from_zombie = 'Data\\Image\\Zombie.png'

    counter_kill = 1000

    # Иницилизация групп
    # Сюда входят все обьекты кроме игрока и камеры
    all_sprite = pygame.sprite.Group()
    # Сюда входят только видимые обьекты
    visible_objects = pygame.sprite.Group()
    # Сюда входят только выстрелы
    bullet = pygame.sprite.Group()
    # Сюда входят только враги
    enemy = pygame.sprite.Group()

    counter = pygame.font.Font(None, 48)

    # Добавления Фона
    background = GameObjects.GameObject((0, 0), path_from_background)
    background.set_mask()
    background.disabled_alpha()
    all_sprite.add(background)
    visible_objects.add(background)

    # Добавления игрока
    person = GameObjects.Person((900, 900), path_from_person, hp=10000, speed_move=(600, 600))
    visible_objects.add(person)

    # Создание камеры
    camera = GameObjects.TargetCamera(all_sprite, person,
                                      traffic_restriction=background.get_size(),
                                      flags=(pygame.FULLSCREEN))
    screen = camera.get_screen()

    clock = pygame.time.Clock()

    # Основной цикл игры
    command_exit = False
    while not command_exit:
        screen.fill((0, 0, 0))

        # Обрабатываем нажаните клавишь
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                command_exit = True

        x, y = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            x += 1
        if keys[pygame.K_a]:
            x -= 1
        if keys[pygame.K_w]:
            y -= 1
        if keys[pygame.K_s]:
            y += 1
        if keys[pygame.K_SPACE]:
            bull = person.shoot()
            visible_objects.add(bull)
            bullet.add(bull)
            all_sprite.add(bull)
        camera.sled((x, y))


        # Обнавление всех обьектов
        person.update()
        all_sprite.update()
        visible_objects.draw(screen)
        xol = counter.render(f"Всего убито: {counter_kill}", True, [0, 0, 0])
        screen.blit(xol, (0, 0))
        if (True and len(enemy) < 100) or (False and not randrange(1)):
            zombie = GameObjects.Enemy((randrange(-150, WINDOW_SIZE[0] * 1.5), -150),
                                       path_from_zombie, speed_move=round(100 + counter_kill ** 0.70),
                                       target=person, damage=round(1 + counter_kill ** 0.125), rotate=(1, lambda: person.get_rect().center), hp=round(1 + counter_kill ** 0.25))
            all_sprite.add(zombie)
            visible_objects.add(zombie)
            enemy.add(zombie)

        person.edit_speed_move(round(600 + (counter_kill ** 0.5)))

        a = pygame.sprite.spritecollide(person, enemy, False,
                                          collided=pygame.sprite.collide_mask)
        if a:
            for enem in a:
                person.hit(enem.get_damage())

        a = pygame.sprite.groupcollide(bullet, enemy, False, False)
        if a:
            for x, y in a.items():
                for enemys in y:
                    if pygame.sprite.collide_mask(x, enemys):
                        enemys.hit(x.get_damage())
                        x.kill()
                        if not enemys.get_hp():
                            counter_kill += 1


        clock.tick(FPS)
        pygame.display.flip()


def main_background():
    global surface
    surface.fill(COLOR_BACKGROUND)


def main(test=False):
    global clock
    global main_menu
    global surface
    global WINDOW_SIZE
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    surface = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
    WINDOW_SIZE = surface.get_size()
    pygame.display.set_caption('Example - Game Selector')
    clock = pygame.time.Clock()
    play_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.7),
                                menu_width=int(WINDOW_SIZE[0] * 0.7),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Play menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )

    play_submenu = pygameMenu.Menu(surface,
                                   bgfun=main_background,
                                   color_selected=COLOR_WHITE,
                                   font=pygameMenu.font.FONT_BEBAS,
                                   font_color=COLOR_BLACK,
                                   font_size=30,
                                   menu_alpha=100,
                                   menu_color=MENU_BACKGROUND_COLOR,
                                   menu_height=int(WINDOW_SIZE[1] * 0.5),
                                   menu_width=int(WINDOW_SIZE[0] * 0.7),
                                   option_shadow=False,
                                   title='Submenu',
                                   window_height=WINDOW_SIZE[1],
                                   window_width=WINDOW_SIZE[0]
                                   )
    play_submenu.add_option('Back', pygameMenu.events.BACK)
    play_menu.add_option('Start',
                         play_function,
                         DIFFICULTY,
                         pygame.font.Font(pygameMenu.font.FONT_FRANCHISE, 30))
    play_menu.add_selector('Select difficulty',
                           [('1 - Easy', 'EASY'),
                            ('2 - Medium', 'MEDIUM'),
                            ('3 - Hard', 'HARD')],
                           onchange=change_difficulty,
                           selector_id='select_difficulty')
    play_menu.add_option('Return to main menu', pygameMenu.events.BACK)
    about_menu = pygameMenu.TextMenu(surface,
                                     bgfun=main_background,
                                     color_selected=COLOR_WHITE,
                                     font=pygameMenu.font.FONT_BEBAS,
                                     font_color=COLOR_BLACK,
                                     font_size_title=30,
                                     font_title=pygameMenu.font.FONT_8BIT,
                                     menu_color=MENU_BACKGROUND_COLOR,
                                     menu_color_title=COLOR_WHITE,
                                     menu_height=int(WINDOW_SIZE[1] * 0.6),
                                     menu_width=int(WINDOW_SIZE[0] * 0.6),
                                     onclose=pygameMenu.events.DISABLE_CLOSE,
                                     option_shadow=False,
                                     text_color=COLOR_BLACK,
                                     text_fontsize=50,
                                     title='About',
                                     window_height=WINDOW_SIZE[1],
                                     window_width=WINDOW_SIZE[0]
                                     )
    for m in ABOUT:
        about_menu.add_line(m)
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_option('Return to menu', pygameMenu.events.BACK)
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.6),
                                menu_width=int(WINDOW_SIZE[0] * 0.6),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Main menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    main_menu.add_option('Play', play_menu)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)
    main_menu.set_fps(FPS)
    while True:
        clock.tick(FPS)
        main_background()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        main_menu.mainloop(events, disable_loop=test)
        pygame.display.flip()
        if test:
            break


main()
