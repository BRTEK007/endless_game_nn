from game import *

import time
import argparse
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback

class JetpackEnv(gym.Env):
    def __init__(self, render = False):
        super().__init__()
        self.observation_space = spaces.Box(low=-1.0, high=1.0, shape=(4,), dtype=np.float32)
        self.action_space = spaces.Discrete(2)
        self.game = Game()
        self._last_score = 0

        if render:
            pygame.init()
            pygame.font.init()

            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.font = pygame.font.Font(None, 36)

    def reset(self, *, seed=None, options=None):
        self.game.restart()
        self._last_score = 0
        return self._get_obs(), {}

    def step(self, action):
        FPS = 30
        if action == 1:
            self.game.mouse_click()
        self.game.update(1.0 / FPS) # simulate a frame
        obs = self._get_obs()

        reward = 0.0

        if self.game.score > self._last_score:
            reward += 1.0 # passed an obstacle reward
            self._last_score = self.game.score

        done = not self.game.is_playing()  # set to True if crashed

        if done:
            reward -= 1.0 # crashing penalty
        else:
            reward += 0.01 # surviving reward
    
        truncated = False
        return obs, reward, done, truncated, {}

    def _get_obs(self):
        return np.array(self.game.game_state(), dtype=np.float32)

    def render(self, mode="human"):
        self.game.draw(self.screen, self.font)
        pygame.display.flip()

    def close(self):
        pass

def play():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font = pygame.font.Font(None, 36)

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

        if game.is_playing() == False:
            game.restart()

        game.update(dt)
        game.draw(screen, font)
        pygame.display.flip()

    pygame.quit()

def train():
    env = JetpackEnv(render=False)
    eval_env = JetpackEnv(render=False)

    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path="./models/",
        log_path="./logs/",
        eval_freq=5000,          # evaluate every 5000 steps
        deterministic=True,
        render=False,
    )

    # model = PPO("MlpPolicy", env, verbose=1)
    model = PPO.load("./models/base_model", env=env)
    model.learn(total_timesteps=100_000, callback=eval_callback)
  
def evaluate():
    env = JetpackEnv(render=True)   # enable rendering
    model = PPO.load("./models/best_model", env=env)

    obs, _ = env.reset()
    done, truncated = False, False
    while True:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, truncated, _ = env.step(action)
        env.render()
        time.sleep(1/30)
        if done or truncated:
            obs, _ = env.reset()

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["train", "play", "eval"], required=True,
                    help="Run mode: train or play or eval")
args = parser.parse_args()

if args.mode == "play":
    play()
elif args.mode == "train":
    train()
elif args.mode == "eval":
    evaluate()

# obs, _ = env.reset()
# for _ in range(1000):
#     pygame.time.wait(100)
#     env.render()
#     action, _ = model.predict(obs, deterministic=True)
#     obs, reward, terminated, truncated, _ = env.step(action)
#     if terminated or truncated:
#         obs, _ = env.reset()