import sys
import random
import pygame


class Cell:
    def __init__(self, x, y, size):
        self.status = random.choice([0]*20 + [1]*20)
        self.newStatus = None
        self.x = x
        self.y = y
        self.size = size
        self.color = self.getColor()

    def draw(self, screen):
        pygame.draw.rect(
            screen, self.color, (self.x, self.y, self.size, self.size))

    def getColor(self):
        if self.status:
            return (100, 100, 220)
        return (15, 15, 15)

    def changeStatus(self):
        self.status = self.newStatus
        self.color = self.getColor()


class Main:
    def __init__(self):
        # Initialize the window
        pygame.init()
        pygame.display.set_caption("Conway's Game of Life")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # ! Whats that?
        self.clock = pygame.time.Clock()

        # Create the grid
        self.createGrid()

        # Call the main game loop
        self.mainloop()

    def createGrid(self):
        # Calculate rows, and cols amount depending on the cell size
        cellSize = 15
        info = pygame.display.Info()
        winX, winY = info.current_w, info.current_h
        rows, cols = int(winY / cellSize), int(winX / cellSize)

        # Calculate the margin to center the grid
        marginY = (winY - rows*cellSize) / 2
        marginX = (winX - cols*cellSize) / 2

        # Create the cell instances and save the in the grid
        self.grid = []
        i, j = marginX, marginY
        for row in range(rows):
            row = []
            for _ in range(cols):
                row.append(Cell(i, j, cellSize))
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

    def update(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                status = self.checkNeighbours(self.grid, i, j, cell.status)
                cell.newStatus = status

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                cell.changeStatus()

    def draw(self):
        # Draw each cell in the grid
        for row in self.grid:
            for cell in row:
                cell.draw(self.screen)

    def mainloop(self):
        while True:
            # Check for events
            self.eventHandler()

            # Call the update & draw methods
            self.update()
            self.draw()

            # Update the screen
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    Main()
