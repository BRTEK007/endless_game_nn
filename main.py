import pygame
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 640
LEVEL_BOUNDS_WIDTH = 48

COLOR_BOUNDS = (67, 98, 125)
COLOR_BG = (10, 138, 252)
COLOR_OBSTACLE = (252, 22, 10)
COLOR_PLAYER = (236, 252, 10)


class Obstacle:
    GAP_SIZE = 180
    MIN_PADDING = 64
    WIDTH = 64
    SPEED = 256
    def __init__(self, x_pos, gap_y_level):
        self.x_pos = x_pos
        self.gap_y_level = gap_y_level

    def update(self, dt):
        self.x_pos -= Obstacle.SPEED * dt

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_OBSTACLE, 
        (self.x_pos, self.gap_y_level+Obstacle.GAP_SIZE//2, Obstacle.WIDTH, WINDOW_HEIGHT))

        pygame.draw.rect(screen, COLOR_OBSTACLE, 
        (self.x_pos, LEVEL_BOUNDS_WIDTH, Obstacle.WIDTH, self.gap_y_level-LEVEL_BOUNDS_WIDTH-Obstacle.GAP_SIZE//2))

    def is_off_screen(self):
        return self.x_pos + Obstacle.WIDTH < 0

class Player:
    RADIUS = 20
    X_POS = 100
    GRAVITY  = WINDOW_HEIGHT*2
    JUMP_VEL = GRAVITY//3
    def __init__(self):
        self.radius = Player.RADIUS
        self.y_pos = WINDOW_HEIGHT-LEVEL_BOUNDS_WIDTH-Player.RADIUS-1
        self.y_vel = 0

    def update(self, dt):
        self.y_vel += Player.GRAVITY * dt
        self.y_pos += self.y_vel*dt
        
        if self.y_pos > WINDOW_HEIGHT-LEVEL_BOUNDS_WIDTH - Player.RADIUS:
            self.y_pos = WINDOW_HEIGHT-LEVEL_BOUNDS_WIDTH - Player.RADIUS

    def jump(self):
        self.y_vel = -Player.JUMP_VEL

    def draw(self, screen):
        pygame.draw.circle(screen, COLOR_PLAYER, (Player.X_POS, self.y_pos), Player.RADIUS)


class Game:
    def __init__(self):
        self.player = Player()
        self.obstacles = []

        obstacle_offset_range = (WINDOW_HEIGHT - LEVEL_BOUNDS_WIDTH*2 - Obstacle.GAP_SIZE - Obstacle.MIN_PADDING*2)//2
        self.obstacle_range = (WINDOW_HEIGHT//2-obstacle_offset_range, WINDOW_HEIGHT//2+obstacle_offset_range)

        self.spawn_obstacle(WINDOW_WIDTH)
        self.spawn_obstacle(WINDOW_WIDTH*1.5)
        self.font = pygame.font.Font(None, 36)
        self.score = 0

    def restart(self):
        pass

    def spawn_obstacle(self, x_pos):
        self.obstacles.append(Obstacle(x_pos, random.randint(self.obstacle_range[0], self.obstacle_range[1])))

    def update(self, dt):
        for ob in self.obstacles:
            ob.update(dt)

        self.obstacles = [ob for ob in self.obstacles if not ob.is_off_screen()]

        self.player.update(dt)

        if len(self.obstacles) < 2:
            self.spawn_obstacle(WINDOW_WIDTH)

    def mouse_click(self):
        self.player.jump()

    def draw(self, screen):
        screen.fill(COLOR_BG)

        for ob in self.obstacles:
            ob.draw(screen)

        LEVEL_BOUNDS_WIDTH
        pygame.draw.rect(screen, COLOR_BOUNDS, (0, 0, WINDOW_WIDTH, LEVEL_BOUNDS_WIDTH))
        pygame.draw.rect(screen, COLOR_BOUNDS, (0, WINDOW_HEIGHT-LEVEL_BOUNDS_WIDTH, WINDOW_WIDTH, LEVEL_BOUNDS_WIDTH))

        self.player.draw(screen)

        text_surface = self.font.render(f"score: {1}", True, (255, 255, 255))
        screen.blit(text_surface, (5, 5))


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


game = Game()
clock = pygame.time.Clock()  
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                game.mouse_click()

    game.update(dt)
    game.draw(screen)
    pygame.display.flip()

pygame.quit()
