# Conways-Game-of-Life (my version)
___
### Introduction & Requirements
This file is my implementation of Conway's game of life. It is programmed in python with the pygame module. To run the main.py file you need to have Python installed and the latest version of the pygame module.

### Change the simulation to your needs
In the _config.json_ file, you can choose some basic settings to your needs. Here is a quick explanation for each entry:
- cell-size (integer): Changes the cell-size. Warning: The number shouldn't be too big (will raise an error) or too low (causing lag)!
- cell-color-alive (rgb-values): The color of a cell when it is alive.
- cell-color-dead (rgb-values): The color of a cell when it is dead.
- bg-color (rgb-values): The color of the background behind the grid. (Depending on the grid size, it is possible that you won't be able to see this)

### Shortcuts & how to use the file
When the file is initially started, you will be in draw mode. You can the state of a cell by clicking on it with the right or left mouse button.
- CTRL + C: will exit the program at all times
- CTRL + S: will start the simulation when in draw mode
- CTRL + R: will reset the simulation when simulation is running