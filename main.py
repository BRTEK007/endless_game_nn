import pygame
import random

pygame.init()

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 480
LEVEL_BOUNDS_WIDTH = 48

COLOR_BOUNDS = (67, 98, 125)
COLOR_BG = (10, 138, 252)
COLOR_OBSTACLE = (252, 22, 10)
COLOR_PLAYER = (236, 252, 10)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

class Obstacle:
    GAP_SIZE = 128
    WIDTH = 64
    SPEED = 256
    def __init__(self, x_pos, bottom_row_height):
        self.x_pos = x_pos
        self.bottom_row_height = bottom_row_height

    def update(self, dt):
        self.x_pos -= Obstacle.SPEED * dt

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_OBSTACLE, 
        (self.x_pos, self.bottom_row_height, Obstacle.WIDTH, WINDOW_HEIGHT-self.bottom_row_height-LEVEL_BOUNDS_WIDTH))

        pygame.draw.rect(screen, COLOR_OBSTACLE, 
        (self.x_pos, LEVEL_BOUNDS_WIDTH, Obstacle.WIDTH, self.bottom_row_height-LEVEL_BOUNDS_WIDTH-Obstacle.GAP_SIZE))

    def is_off_screen(self):
        return self.x_pos + Obstacle.WIDTH < 0

class Player:
    RADIUS = 20
    X_POS = 100
    def __init__(self):
        self.radius = Player.RADIUS
        self.y_pos = WINDOW_HEIGHT-LEVEL_BOUNDS_WIDTH-Player.RADIUS-1

    def update(self, dt):
        pass

    def draw(self, screen):
        pygame.draw.circle(screen, COLOR_PLAYER, (Player.X_POS, self.y_pos), Player.RADIUS)


class Game:
    def __init__(self):
        self.player = Player()
        self.obstacles = []

        self.obstacles.append(Obstacle(WINDOW_WIDTH, random.randint(WINDOW_HEIGHT//2-64, WINDOW_HEIGHT//2+64)))
        self.obstacles.append(Obstacle(WINDOW_WIDTH*1.5, random.randint(WINDOW_HEIGHT//2-64, WINDOW_HEIGHT//2+64)))
        self.obstacles.append(Obstacle(WINDOW_WIDTH*2, random.randint(WINDOW_HEIGHT//2-64, WINDOW_HEIGHT//2+64)))

        self.obstacle_speed = 2.5

    def update(self, dt):
        for ob in self.obstacles:
            ob.update(dt)

        self.obstacles = [ob for ob in self.obstacles if not ob.is_off_screen()]

    def draw(self, screen):
        screen.fill(COLOR_BG)

        for ob in self.obstacles:
            ob.draw(screen)

        LEVEL_BOUNDS_WIDTH
        pygame.draw.rect(screen, COLOR_BOUNDS, (0, 0, WINDOW_WIDTH, LEVEL_BOUNDS_WIDTH))
        pygame.draw.rect(screen, COLOR_BOUNDS, (0, WINDOW_HEIGHT-LEVEL_BOUNDS_WIDTH, WINDOW_WIDTH, LEVEL_BOUNDS_WIDTH))

        self.player.draw(screen)


game = Game()
clock = pygame.time.Clock()  
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.update(dt)
    game.draw(screen)
    pygame.display.flip()

pygame.quit()
