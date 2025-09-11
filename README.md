# endless_runner_nn

Simple endless runner game, player has to pass oncoming obstacles. Player only has one action, to jump. Program can be run in 3 modes:

### training
Trains simple Neural network to play the game.

### evaluation
Evaluates chosen model in real time.

### playing
Allowes user to play the game manually. Use mouse click to jump.

Adjustable game parameters:

**--dens** - obstacle density, how many obstacles are on the screen.

**--gap** - size of the gap in the obstacles.

# Training process

An MlpPolicy from Stable-Baselines3 is used. Model was trained with decreasing obstacle gap, starting from 300 and going as low as 120. The previous model was always used as a starting point. Untrained model struggles to find random success in the beggining for obstacle density < 3. During training the game was limited to stop after the player passes 12 obstacles.

# Example training
```
python3 main.py --mode train --file dens_3_gap_120/best_model.zip --dens 3 --gap 120
```

# Example evaluation
```
python3 main.py --mode eval --file dens_3_gap_120/best_model.zip --dens 3 --gap 120
```

# Example playing
```
python3 main.py --mode play --dens 3 --gap 120
```