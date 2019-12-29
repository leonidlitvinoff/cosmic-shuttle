import pygame
import GameObjects

FPS = 60

path_from_background = 'Data\\Image\\Space_Background.png'
path_from_person = 'Data\\Image\\Person.jpg'

all_sprite = pygame.sprite.Group()

background = GameObjects.GameObject((0, 0), path_from_background)
all_sprite.add(background)


person = GameObjects.GameObject((0, 0), path_from_person, hp=100, speed_move=(300, 600))
all_sprite.add(person)

camera = GameObjects.MovingCamera(traffic_restriction=background.get_size(), speed_move=(2, 3))
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

    all_sprite.update()
    all_sprite.draw(screen)

    clock.tick(FPS)
    camera.update(all_sprite)
    pygame.display.flip()