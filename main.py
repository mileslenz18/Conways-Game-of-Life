import sys
import pygame


class Cell:
    def __init__(self, x, y, size):
        self.status = 0
        self.newStatus = None
        self.x = x
        self.y = y
        self.size = size
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
            return (80, 200, 80)
        return (15, 15, 15)

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

        # Declare important variables for the simulation
        self.clock = pygame.time.Clock()
        self.gridActivated = True
        self.running = True
        self.startSimulation = False
        self.appState = "introduction"

        # Create the grid
        self.createGrid()

        # Call the main game loop
        self.mainloop()

    def createGrid(self):
        # Calculate rows, and cols amount depending on the cell size
        cellSize = 43
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

            # Skip the introduction when button is pressed
            if (self.appState == "introduction" and
                    event.type == pygame.MOUSEBUTTONDOWN and
                    event.button == 1):
                pos = pygame.mouse.get_pos()
                if (self.introBtnX <= pos[0] and self.introBtnX +
                        self.introBtnSize[0] >= pos[0] and
                        self.introBtnY <= pos[1] and
                        self.introBtnY + self.introBtnSize[1] >= pos[1]):
                    self.appState = "simulation"
                    return

            # Do not check anythin below here if simulation is running
            # or the intro is displayed
            if self.startSimulation or self.appState == "introduction":
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

    def drawIntroduction(self):
        center = pygame.display.Info().current_w / 2

        # Draw the background color
        self.screen.fill((20, 20, 20))

        # Create different fonts
        h1 = pygame.font.SysFont('Lato', 50)
        h2 = pygame.font.SysFont('Lato', 32)

        # Create the actual text
        title = h1.render("Conway's Game of Life", False, (220, 220, 220))
        text1Str = "Press the left mouse button to draw."
        text2Str = "Press the right mouse button to erase."
        text1 = h2.render(text1Str, False, (220, 220, 220))
        text2 = h2.render(text2Str, False, (220, 220, 220))

        # Render the texts
        self.screen.blit(title, (center - title.get_width()/2, 220))
        self.screen.blit(text1, (center - title.get_width()/2, 420))
        self.screen.blit(text2, (center - title.get_width()/2, 500))

        # Draw a button to continue
        self.introBtnX, self.introBtnY = center - 100, 600
        self.introBtnSize = (200, 80)
        pygame.draw.rect(
            self.screen, (200, 0, 0),
            (self.introBtnX, self.introBtnY,
             self.introBtnSize[0], self.introBtnSize[1])
        )

    def mainloop(self):
        while self.running:
            # Check for events
            self.eventHandler()

            # Call the update & draw methods
            if self.appState == "simulation":
                if self.startSimulation:
                    self.update()
                self.draw()
            else:
                self.drawIntroduction()

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
