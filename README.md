# snakeAPI
An API for a basic snake environment that can be used to test reinforcement learning algorithms.
Unlike traditional inputs to RL algorithms which are huge and clunky this provides a clean API with low computational power required to test and train your RL algos.

## Dependencies
needs python version with tkinter (python3-tk) and turtle
``` pip3 install turtle ```
``` sudo apt-get install python3-tk ```

## Usage
```python 
from snake import *
game = Game() # starts a new game
game.startScreen(render=True) # starts the screen. Put render = True to see the output. False for speedy computations
done = False

while done != -1:
  action = random.choice(['0', '1', '2', '3']) # represent up down left right respectively
  done, reward = game.nextFrame(action, render=True)
  snakeInfo = game.snakeInfo() # returns the current state of the snake as a [headX, headY, foodX, foodY, [position_of_all_tail_elements]]
game.clearScreen() # deletes all objects from screen
