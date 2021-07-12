import sys
import json
import pygame


class Cell:
    def __init__(self, x, y, size, colorAlive, colorDead):
        self.status = 0
        self.newStatus = None
        self.x = x
        self.y = y
        self.size = size
        self.colorAlive = colorAlive
        self.colorDead = colorDead
        self.color = self.getColor()

    def draw(self, screen, gridActivated):
        # Draw the actual cell
        pygame.draw.rect(
            screen, self.color, (self.x, self.y, self.size, self.size))

        # Draw part of the grid outline
        if gridActivated:
            pygame.draw.line(
                screen, (100, 100, 100), (self.x, self.y),
                (self.x + self.size - 1, self.y))
            pygame.draw.line(
                screen, (100, 100, 100), (self.x, self.y),
                (self.x, self.y + self.size - 1))

    def getColor(self):
        if self.status:
            return self.colorAlive
        return self.colorDead

    def changeStatus(self):
        self.status = self.newStatus
        self.color = self.getColor()


class Main:
    def __init__(self):
        # Initialize the window
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Conway's Game of Life")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # Get the settings from the config.json file
        with open('config.json') as jsonFile:
            self.config = json.load(jsonFile)

        # Declare important variables for the simulation
        self.clock = pygame.time.Clock()
        self.gridActivated = bool(self.config['display-grid'])
        self.running = True
        self.startSimulation = False

        # Create the grid
        self.createGrid()

        # Call the main game loop
        self.mainloop()

    def createGrid(self):
        # Calculate rows, and cols amount depending on the cell size
        cellSize = int(self.config['cell-size'])
        info = pygame.display.Info()
        winX, winY = info.current_w, info.current_h
        rows, cols = int(winY / cellSize), int(winX / cellSize)

        # Calculate the margin to center the grid
        marginY = (winY - rows*cellSize) / 2
        marginX = (winX - cols*cellSize) / 2

        # Get the colors from the .json file
        colorAlive = tuple(
            map(int, self.config['cell-color-alive'].split(', ')))
        colorDead = tuple(map(int, self.config['cell-color-dead'].split(', ')))

        # Create the cell instances and save the in the grid
        self.grid = []
        i, j = marginX, marginY
        for row in range(rows):
            row = []
            for _ in range(cols):
                row.append(Cell(i, j, cellSize, colorAlive, colorDead))
                i += cellSize
            self.grid.append(row)
            i = marginX
            j += cellSize

    def checkNeighbours(self, grid, i, j, status):
        # Get a list of all the neighbours
        if i == 0:
            if j == 0:
                neighbours = [(i, j+1), (i+1, j), (i+1, j+1)]
            elif j == len(grid[0]) - 1:
                neighbours = [(i, j-1), (i+1, j), (i+1, j-1)]
            else:
                neighbours = [
                    (i, j-1), (i, j+1), (i+1, j), (i+1, j+1), (i+1, j-1)]
        elif i == len(grid) - 1:
            if j == 0:
                neighbours = [(i, j+1), (i-1, j), (i-1, j+1)]
            elif j == len(grid[0]) - 1:
                neighbours = [(i, j-1), (i-1, j), (i-1, j-1)]
            else:
                neighbours = [
                    (i, j-1), (i, j+1), (i-1, j), (i-1, j+1), (i-1, j-1)]
        else:
            if j == 0:
                neighbours = [
                    (i+1, j), (i-1, j), (i, j+1), (i+1, j+1), (i-1, j+1)]
            elif j == len(grid[0]) - 1:
                neighbours = [
                    (i+1, j), (i-1, j), (i, j-1), (i+1, j-1), (i-1, j-1)]
            else:
                neighbours = [
                    (i+1, j), (i-1, j), (i, j+1), (i, j-1),
                    (i+1, j+1), (i-1, j+1), (i+1, j-1), (i-1, j-1)]

        # Count the neighbours with an alive status
        aliveCells = 0
        for i, j in neighbours:
            if grid[i][j].status:
                aliveCells += 1

        # Return 1 or 0 depending on the amount of alive cells
        if status:
            if aliveCells == 2 or aliveCells == 3:
                return 1
            return 0
        else:
            if aliveCells == 3:
                return 1
            return 0

    def drawCells(self, drawMode):
        pos = pygame.mouse.get_pos()
        for row in self.grid:
            for cell in row:
                if (cell.x <= pos[0] and cell.x + cell.size >= pos[0]
                        and cell.y <= pos[1]
                        and cell.y + cell.size >= pos[1]):
                    if drawMode:
                        cell.newStatus = 1
                    else:
                        cell.newStatus = 0
                    cell.changeStatus()

    def eventHandler(self):
        # Check all detected events
        for event in pygame.event.get():

            # If the 'x' button is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If any key is pressed
            if event.type == pygame.KEYDOWN:
                mo = pygame.key.get_mods()

                # Close the game if CTRL + C is pressed
                if (event.key == pygame.K_c and
                        mo & event.key == pygame.KMOD_LCTRL):
                    pygame.quit()
                    sys.exit()

                # Start simulation if CTRL + S is pressed
                if (event.key == pygame.K_s and
                        mo & event.key == pygame.KMOD_LCTRL):
                    self.startSimulation = True

                # Reset everything if CTRL + R is pressed
                if (event.key == pygame.K_r and
                        mo & event.key == pygame.KMOD_LCTRL):
                    self.running = False

            # Do not check anythin below here if simulation is running
            if self.startSimulation:
                return

            # Check if the left mouse is pressed to draw
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                    or event.type == pygame.MOUSEMOTION and event.buttons[0]):
                self.drawCells(1)

            # Check if the right mouse is pressed to erase
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3
                    or event.type == pygame.MOUSEMOTION and event.buttons[2]):
                self.drawCells(0)

    def update(self):
        # Check all the cells and save their new status
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                status = self.checkNeighbours(self.grid, i, j, cell.status)
                cell.newStatus = status

        # Apply the new status to all the cells
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                cell.changeStatus()

        # Reset the simulation if all cells are dead
        cellAlive = False
        for row in self.grid:
            for cell in row:
                if cell.status:
                    cellAlive = True
                    break
            if cellAlive:
                break
        if not cellAlive:
            self.running = False

    def draw(self):
        # Draw the background
        bgColor = tuple(map(int, self.config['bg-color'].split(', ')))
        self.screen.fill(bgColor)

        # Draw each cell in the grid
        for row in self.grid:
            for cell in row:
                cell.draw(self.screen, self.gridActivated)

        # Draw bottom line of the grid outline
        if self.gridActivated:
            cellSize = self.grid[0][0].size
            xEnd = self.grid[-1][-1].x + cellSize
            yEnd = self.grid[-1][-1].y + cellSize

            xStart, yStart = self.grid[-1][0].x, self.grid[-1][0].y + cellSize
            pygame.draw.line(
                self.screen, (100, 100, 100), (xStart, yStart - 1),
                (xEnd - 1, yEnd - 1)
            )

            xStart, yStart = self.grid[0][-1].x + cellSize, self.grid[0][-1].y
            pygame.draw.line(
                self.screen, (100, 100, 100), (xStart - 1, yStart),
                (xEnd - 1, yEnd - 1)
            )

    def mainloop(self):
        while self.running:
            # Check for events
            self.eventHandler()

            # Call the update & draw methods
            if self.startSimulation:
                self.update()
            self.draw()

            # Update the screen
            pygame.display.flip()
            self.clock.tick(20)

        # Reset the variables
        self.createGrid()
        self.running = True
        self.startSimulation = False
        self.mainloop()


if __name__ == '__main__':
    Main()
