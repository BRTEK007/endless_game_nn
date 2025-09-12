# endless_runner_nn

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

# Resulst

TODO: video, picture, evaluations, 110 on 110, 120 on 120, 110 on 120

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