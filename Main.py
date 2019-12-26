import pygame
import GameObject

FPS = 60

screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

command_exit = False
while not command_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            command_exit = True

    clock.tick(FPS)
    pygame.display.flip()