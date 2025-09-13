# endless_runner_nn

![Can't load thumbnail.png](./thumbnail.png)

Simple endless runner game, player has to pass oncoming obstacles. Player only has one action, to jump. Program can be run in 4 modes:

### training
Trains simple Neural network to play the game.

### testing
Runs chosen model in real time.

### evaluation
Evaluates chosen model in multiple runs.

### playing
Allowes user to play the game manually. Use mouse click to jump.

Adjustable game parameters:

**--dens** - obstacle density, how many obstacles are on the screen.

**--gap** - size of the gap in the obstacles.

# Training process

An MlpPolicy from Stable-Baselines3 is used. Models were trained with decreasing obstacle gap, with the model trained on the higher gap used as a starting point for new training. Untrained model struggles to find random success in the beggining for obstacle density < 3. During training the game was limited to stop after the player passes 12 obstacles.

# Results

![Can't load model_test_run_gap_120.gif](./model_test_run_gap_120.gif)

Satisfactory performance was achieved up to the gap sizes of 120 and 110. Model trained on 110 gap size performed better on 120 gap size obstacles than 120 gap size model, even though it performed very poorly on the gap size of 110. The evaluations run the game 100 times, with upper score limit of 100. All scenarios have relativly high standard deviations, sometimes reaching scores from 0 or 1 obstacles up to 100, showing poor consistency.

### 110 gap size model on 120 gap size obstacles

![Can't load eval_graph_model_110_gap_120.png](./eval_graph_model_110_gap_120.png)

### 120 gap size model on 120 gap size obstacles

![Can't load eval_graph_model_120_gap_120.png](./eval_graph_model_120_gap_120.png)

### 110 gap size model on 110 gap size obstacles

![Can't load eval_graph_model_110_gap_110.png](./eval_graph_model_110_gap_110.png)


# Example training
```
python3 main.py --mode train --file dens_3_gap_120/best_model.zip --dens 3 --gap 120
```

# Example testing
```
python3 main.py --mode test --file dens_3_gap_120/best_model.zip --dens 3 --gap 120
```

# Example evaluation
```
python3 main.py --mode eval --file dens_3_gap_120/best_model.zip --dens 3 --gap 120
```

# Example playing
```
python3 main.py --mode play --dens 3 --gap 120
```