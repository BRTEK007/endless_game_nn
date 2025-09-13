from game import *

import time
import argparse
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnNoModelImprovement

import matplotlib.pyplot as plt
import pandas as pd
import cv2

class JetpackEnv(gym.Env):
    def __init__(self, render = False, obstacle_density = 2, obstacle_gap_size = 200, score_to_pass = 12):
        super().__init__()
        self.observation_space = spaces.Box(low=-1.0, high=1.0, shape=(4,), dtype=np.float32)
        self.action_space = spaces.Discrete(2)
        self.game = Game(obstacle_density = obstacle_density,
         obstacle_gap_size = obstacle_gap_size, score_to_pass = score_to_pass)
        self._last_score = 0

        self.obstacle_density = obstacle_density
        self.obstacle_gap_size = obstacle_gap_size
        self.score_to_pass = score_to_pass

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

        if done and not self.game.is_won():
            reward -= 1.0 # crashing penalty
        else:
            reward += 0.01 # surviving reward
    
        truncated = False
        return obs, reward, done, truncated, {}

    def get_score(self):
        return self.game.score

    def get_screen(self):
        return self.screen

    def _get_obs(self):
        return np.array(self.game.game_state(), dtype=np.float32)

    def render(self, mode="human"):
        self.game.draw(self.screen, self.font)
        pygame.display.flip()

    def close(self):
        pass


def play(obstacle_density, obstacle_gap_size):
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font = pygame.font.Font(None, 36)

    game = Game(obstacle_density = obstacle_density, obstacle_gap_size = obstacle_gap_size, score_to_pass = 100)
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

def train(initial_model_file, obstacle_density, obstacle_gap_size):

    env = JetpackEnv(render=False, obstacle_density = obstacle_density, obstacle_gap_size = obstacle_gap_size, score_to_pass = 12)
    eval_env = JetpackEnv(render=False, obstacle_density = obstacle_density, obstacle_gap_size = obstacle_gap_size, score_to_pass = 12)

    stop_callback = StopTrainingOnNoModelImprovement(
        max_no_improvement_evals=10,    
        min_evals=5,                    # how many evals to wait before checking      
        verbose=1
    )

    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=f"./models/dens_{obstacle_density}_gap_{obstacle_gap_size}",
        log_path="./logs/",
        eval_freq=5000,          # evaluate every 5000 steps
        deterministic=True,
        render=False,
        callback_after_eval=stop_callback
    )

    if initial_model_file is None:
        model = PPO("MlpPolicy", env, verbose=1)
    else:
        model = PPO.load(f"./models/{initial_model_file}", env=env)
    model.learn(total_timesteps=100_00, callback=eval_callback)
  
def test(initial_model_file, obstacle_density, obstacle_gap_size,  record = False):
    env = JetpackEnv(render=True, obstacle_density = obstacle_density, obstacle_gap_size = obstacle_gap_size, score_to_pass = 100)
    model = PPO.load(f"./models/{initial_model_file}", env=env)

    if record:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter(f"model_test_run_gap_{obstacle_gap_size}.mp4", fourcc, 30, (WINDOW_WIDTH, WINDOW_HEIGHT))

    obs, _ = env.reset()
    done, truncated = False, False
    while True:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, truncated, _ = env.step(action)
        env.render()

        if record:
            frame = pygame.surfarray.array3d(env.get_screen())
            frame = np.transpose(frame, (1, 0, 2))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            video.write(frame)    

        time.sleep(1/30)
        if done or truncated:
            obs, _ = env.reset()
            if record: # When recording stop playing to save a single run only
                break

    if record:
        video.release()

def evaluate(model_file, obstacle_density, obstacle_gap_size):
    RUNS = 100
    MAX_SCORE = 100
   
    env = JetpackEnv(render=False, obstacle_density = obstacle_density,
    obstacle_gap_size = obstacle_gap_size, score_to_pass = MAX_SCORE)
    model = PPO.load(f"./models/{model_file}", env=env)

    scores = []

    print()
    print(f"Evaluation for {RUNS} runs, with max score limit {MAX_SCORE}")
    print()

    obs, _ = env.reset()
    done, truncated = False, False
    while len(scores) < RUNS:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, truncated, _ = env.step(action)
        if done or truncated or env.get_score() >= MAX_SCORE:
            scores.append(env.get_score())
            print(f"score: {env.get_score()}")
            obs, _ = env.reset()
            done, truncated = False, False

    print()
    df = pd.DataFrame(scores, columns=["score"])
    print(df.describe())

    plt.figure(figsize=(6,4))
    plt.hist(df["score"], bins=50, edgecolor="black")
    plt.xlabel("Score")
    plt.ylabel("Number of runs")
    plt.title("Score Frequency")
    plt.tight_layout()
    plt.savefig(f"eval_graph_gap_{obstacle_gap_size}.png", dpi=150)
    plt.close()


parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["train", "play", "test", "eval"], required=True,
                    help="Run mode: train or play or test.")
parser.add_argument("--file",
                    help="The model to start training with or to evaluate, leave empty for new model. Path should be relative to models directory.")

parser.add_argument("--dens", type=int, required=True,
                    help="How many obstacles on the screen.")

parser.add_argument("--gap", type=int, required=True,
                    help="Obstacle gap size")

parser.add_argument("--record", action="store_true",
                    help="Enable rendering during training")

args = parser.parse_args()

if args.mode == "play":
    play(args.dens, args.gap)
elif args.mode == "train":
    train(args.file, args.dens, args.gap)
elif args.mode == "test":
    if args.file == None:
        print("--file argument needed")
        exit(1)
    test(args.file, args.dens, args.gap, record = args.record)
elif args.mode == "eval":
    if args.file == None:
        print("--file argument needed")
        exit(1)
    evaluate(args.file, args.dens, args.gap)