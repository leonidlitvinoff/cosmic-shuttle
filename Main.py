import pygame
import GameObject

FPS = 60

path_from_person = 'Data\\Image\\Person.jpg'
person = GameObject.VisibleMovingObject((0, 0), path_from_person)

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
                print(person.get_position())
            elif event.key == pygame.K_s:
                person.move_y()
                print(person.get_position())


    person.update(screen)

    clock.tick(FPS)
    pygame.display.flip()