import pygame
import sys

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 480, 720

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Endless runner")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()