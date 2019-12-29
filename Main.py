import pygame
import GameObject

FPS = 60

path_from_background = 'Data\\Image\\Space_Background.png'
path_from_person = 'Data\\Image\\Person.jpg'

all_sprite = pygame.sprite.Group()

background = GameObject.GameObject((0, 0), path_from_background)
all_sprite.add(background)


person = GameObject.GameObject((0, 0), path_from_person, hp=100, speed_move=(60, 120))
all_sprite.add(person)

size_screen = w_screen, h_screen = (800, 600)
screen = pygame.display.set_mode(size_screen)

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

    mouse_pos = pygame.mouse.get_pos()

    if mouse_pos[0] < w_screen // 20 and background.get_position()[0] < 0:
        for sprite in all_sprite.sprites():
            if sprite.get_position()[0] < w_screen:
                sprite.shift((10, 0))
    if mouse_pos[0] > w_screen * 95 // 100 and background.get_position()[0] > -background.get_size()[0] + w_screen:
        for sprite in all_sprite.sprites():
            if sprite.get_position()[0] < w_screen:
                sprite.shift((-10, 0))
    if mouse_pos[1] < h_screen // 20 and background.get_position()[1] < 0:
        for sprite in all_sprite.sprites():
            if sprite.get_position()[1] < w_screen:
                sprite.shift((0, 10))
    if mouse_pos[1] > h_screen * 95 // 100 and background.get_position()[1] > -background.get_size()[1] + h_screen:
        for sprite in all_sprite.sprites():
            if sprite.get_position()[1] < w_screen:
                sprite.shift((0, -10))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        person.move_x()
    if keys[pygame.K_a]:
        person.move_x(1)
    if keys[pygame.K_w]:
        person.move_y(1)
    if keys[pygame.K_s]:
        person.move_y()

    all_sprite.update()
    all_sprite.draw(screen)

    clock.tick(FPS)
    pygame.display.flip()