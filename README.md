# Conways Game of Life

## Introduction & Requirements

This is my implementation of Conway's game of life using Python and the Pygame module. To run the _main.py_ file, you obviously need to have Python as well as Pygame installed. Otherwise, you won't be able to run the game. Perhaps I will add an _.exe_ file in the future, so everyone can try it out.

## Change the simulation to your needs

In the _config.json_ file, you can choose some basic settings to modify the game. Here is a quick explanation for each entry:
- cell-size (integer): Changes the cell-size.

__Warning:__ This number shouldn't be bigger than your screen size (because this will raise an error) or too low (due to possible lags).
- cell-color-alive (rgb-values): The color of a cell when it is alive.
- cell-color-dead (rgb-values): The color of a cell when it is dead.
- bg-color (rgb-values): The color of the background behind the grid.

(Depending on the grid size, it is possible that you won't be able to see this color)

## Shortcuts & Usage

When you initially start the file you will be in __draw mode__. This means you can draw your own starting grid layout and then start the game. The following shortcuts can be used to navigate through the game:
- Left mouse button: Change the cell state to 'alive' (only in draw mode).
- Right mouse button: Change the cell state to 'dead' (only in draw mode).
- CTRL + C: Exit the program at all times.
- CTRL + S: Start the simulation when in draw mode.
- CTRL + R: Reset the simulation when simulation is running.