import pygame
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 640
LEVEL_BOUNDS_WIDTH = 48

COLOR_BOUNDS = (67, 98, 125)
COLOR_BG = (10, 138, 252)
COLOR_OBSTACLE = (252, 22, 10)
COLOR_PLAYER = (236, 252, 10)
OBSTACLES_ON_SCREEN = 4

class Obstacle:
    GAP_SIZE = 200
    MIN_PADDING = 64
    WIDTH = 64
    SPEED = 256
    def __init__(self, x_pos, gap_y_level):
        self.x_pos = x_pos
        self.gap_y_level = gap_y_level
        self.already_passed = False

    def update(self, dt):
        self.x_pos -= Obstacle.SPEED * dt

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_OBSTACLE, 
        (self.x_pos, self.gap_y_level+Obstacle.GAP_SIZE//2, Obstacle.WIDTH, WINDOW_HEIGHT))

        pygame.draw.rect(screen, COLOR_OBSTACLE, 
        (self.x_pos, LEVEL_BOUNDS_WIDTH, Obstacle.WIDTH, self.gap_y_level-LEVEL_BOUNDS_WIDTH-Obstacle.GAP_SIZE//2))

    def is_off_screen(self):
        return self.x_pos + Obstacle.WIDTH < 0

    def collides_with_player(self, player_x, player_y):
        closest_x = player_x

        if player_x < self.x_pos:
            closest_x = self.x_pos
        elif player_x > self.x_pos + Obstacle.WIDTH:
            closest_x = self.x_pos + Obstacle.WIDTH

        dx = player_x-closest_x

        dy = min(abs(player_y - self.gap_y_level - Obstacle.GAP_SIZE//2), abs(player_y-self.gap_y_level + Obstacle.GAP_SIZE//2))

        if player_y < self.gap_y_level - Obstacle.GAP_SIZE//2 or player_y > self.gap_y_level + Obstacle.GAP_SIZE//2:
            dy = 0

        return dx*dx + dy*dy <= Player.RADIUS*Player.RADIUS

    def count_as_passed(self, player_x, player_y):
        if self.already_passed:
            return False
        elif self.x_pos < player_x:
            self.already_passed = True
            return True

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

        if self.y_vel > WINDOW_HEIGHT*2:
            self.y_vel = WINDOW_HEIGHT*2
        elif self.y_vel < -WINDOW_HEIGHT*2:
            self.y_vel = -WINDOW_HEIGHT*2
        
        if self.y_pos > WINDOW_HEIGHT-LEVEL_BOUNDS_WIDTH - Player.RADIUS:
            self.y_pos = WINDOW_HEIGHT-LEVEL_BOUNDS_WIDTH - Player.RADIUS
            self.y_vel *= - 0.6
        elif self.y_pos < LEVEL_BOUNDS_WIDTH + Player.RADIUS:
            self.y_pos = LEVEL_BOUNDS_WIDTH + Player.RADIUS
            self.y_vel = 0

    def jump(self):
        self.y_vel = -Player.JUMP_VEL

    def draw(self, screen):
        pygame.draw.circle(screen, COLOR_PLAYER, (Player.X_POS, self.y_pos), Player.RADIUS)

    def restart(self):
        self.y_pos = WINDOW_HEIGHT-LEVEL_BOUNDS_WIDTH-Player.RADIUS-1
        self.y_vel = 0

class Game:
    def __init__(self, render = False):
        self.player = Player()
        self.obstacles = []

        obstacle_offset_range = (WINDOW_HEIGHT - LEVEL_BOUNDS_WIDTH*2 - Obstacle.GAP_SIZE - Obstacle.MIN_PADDING*2)//2
        self.obstacle_range = (WINDOW_HEIGHT//2-obstacle_offset_range, WINDOW_HEIGHT//2+obstacle_offset_range)


        for i in range(0, OBSTACLES_ON_SCREEN):
            self.spawn_obstacle(WINDOW_WIDTH//2 + i * WINDOW_WIDTH//OBSTACLES_ON_SCREEN)
        
        self.score = 0

        self._is_playing = True

    def restart(self):
        self.score = 0
        self.player.restart()
        self.obstacles = []
        
        for i in range(0, OBSTACLES_ON_SCREEN):
            self.spawn_obstacle(WINDOW_WIDTH//2 + i * WINDOW_WIDTH//OBSTACLES_ON_SCREEN)

        self._is_playing = True

    def spawn_obstacle(self, x_pos):
        self.obstacles.append(Obstacle(x_pos, random.randint(self.obstacle_range[0], self.obstacle_range[1])))

    def update(self, dt):
        if self._is_playing == False:
            return

        for ob in self.obstacles:
            ob.update(dt)
            if ob.collides_with_player(self.player.X_POS, self.player.y_pos):
                self._is_playing = False
            if ob.count_as_passed(self.player.X_POS, self.player.y_pos):
                self.score += 1

        self.obstacles = [ob for ob in self.obstacles if not ob.is_off_screen()]

        self.player.update(dt)

        if len(self.obstacles) < OBSTACLES_ON_SCREEN:
            self.spawn_obstacle(WINDOW_WIDTH)

        if self.score >= 16:
            self._is_playing = False#TODO

    def mouse_click(self):
        self.player.jump()

    def draw(self, screen, font):
        screen.fill(COLOR_BG)

        for ob in self.obstacles:
            ob.draw(screen)

        LEVEL_BOUNDS_WIDTH
        pygame.draw.rect(screen, COLOR_BOUNDS, (0, 0, WINDOW_WIDTH, LEVEL_BOUNDS_WIDTH))
        pygame.draw.rect(screen, COLOR_BOUNDS, (0, WINDOW_HEIGHT-LEVEL_BOUNDS_WIDTH, WINDOW_WIDTH, LEVEL_BOUNDS_WIDTH))

        self.player.draw(screen)

        text_surface = font.render(f"score: {self.score}", True, (255, 255, 255))
        screen.blit(text_surface, (5, 5))

    def is_playing(self):
        return self._is_playing

    def game_state(self):
        """
        (
            player position y                   <-1, 1>,
            player velocity y                   <-1, 1>,
            next obstacle height                <-1, 1>,
            next obstacle x pos                 <-1, 1>
        )
        """
        return [
            1 -self.player.y_pos / (WINDOW_HEIGHT//2),
            self.player.y_vel / (WINDOW_HEIGHT*2),
            1 -self.obstacles[0].gap_y_level / (WINDOW_HEIGHT//2),
            1 - self.obstacles[0].x_pos / (WINDOW_WIDTH//2)]