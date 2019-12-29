import pygame
import GameObject

FPS = 60

path_from_person = 'Data\\Image\\Person.jpg'

all_sprite = pygame.sprite.Group()

person = GameObject.VisibleMovingObject((0, 0), path_from_person, hp=100)

all_sprite.add(person)

screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

command_exit = False
while not command_exit:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            command_exit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                person.move_x()
            elif event.key == pygame.K_s:
                person.move_y()
            elif event.key == pygame.K_w:
                person.move_y(1)
            elif event.key == pygame.K_a:
                person.move_x(1)
            elif event.key == pygame.K_SPACE:
                person.hit(10)


    all_sprite.update()
    all_sprite.draw(screen)

    clock.tick(FPS)
    pygame.display.flip()