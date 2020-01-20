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
WINDOW_SIZE = (1600, 900)

clock = None
main_menu = None
surface = None

def change_difficulty(value, difficulty):
    selected, index = value
    print('Selected difficulty: "{0}" ({1}) at index {2}'.format(selected, difficulty, index))
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
    path_from_background = 'Data\\Image\\Background.png'
    path_from_person = 'Data\\Image\\Person.png'
    path_from_planet = 'Data\\Image\\Planet2.png'

    all_sprite = pygame.sprite.Group()

    background = GameObjects.GameObject((0, 0), path_from_background, collidepoint_type=path_from_background)
    all_sprite.add(background)

    planet = GameObjects.Planet((0, 0), path_from_planet, point_degradation=100)
    all_sprite.add(planet)

    person = GameObjects.GameObject((100, 100), path_from_person, hp=100, speed_move=(300, 600), collidepoint_type=path_from_person)
    all_sprite.add(person)

    camera = GameObjects.MovingCamera(traffic_restriction=background.get_size(), speed_move=(2, 3), max_speed_increase=10, distance_start_move=10)
    screen = camera.get_screen()

    clock = pygame.time.Clock()

    command_exit = False
    while not command_exit:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                command_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    person.hit(10)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            person.move_x()
        if keys[pygame.K_a]:
            person.move_x(1)
        if keys[pygame.K_w]:
            person.move_y(1)
        if keys[pygame.K_s]:
            person.move_y()

        ab = pygame.sprite.collide_mask(background, person)
        if ab:
            print(ab)

        all_sprite.update()
        all_sprite.draw(screen)

        clock.tick(FPS)
        camera.update(all_sprite)
        pygame.display.flip()


def main_background():
    global surface
    surface.fill(COLOR_BACKGROUND)


def main(test=False):
    global clock
    global main_menu
    global surface
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    surface = pygame.display.set_mode(WINDOW_SIZE)
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