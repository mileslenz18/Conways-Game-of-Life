import random
import time
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
            return (100, 200, 100)
        return (15, 15, 15)

    def changeStatus(self):
        self.status = self.newStatus
        self.color = self.getColor()


def eventHandler(animationSpeed):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            mo = pygame.key.get_mods()
            if event.key == pygame.K_c and mo & event.key == pygame.KMOD_LCTRL:
                pygame.quit()

            if event.key == pygame.K_KP_PLUS:
                if animationSpeed > 0:
                    animationSpeed -= 0.02
            elif event.key == pygame.K_KP_MINUS:
                animationSpeed += 0.02
    return animationSpeed


def draw(screen, grid):
    # Draw all the cells
    for row in grid:
        for cell in row:
            cell.draw(screen)


def update(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            status = checkNeighbours(grid, i, j, cell.status)
            cell.newStatus = status

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            cell.changeStatus()

    return grid


def checkNeighbours(grid, i, j, status):
    aliveCells = 0

    if i == 0:
        if j == 0:
            neighbours = [(i, j+1), (i+1, j), (i+1, j+1)]
        elif j == len(grid[0]) - 1:
            neighbours = [(i, j-1), (i+1, j), (i+1, j-1)]
        else:
            neighbours = [(i, j-1), (i, j+1), (i+1, j), (i+1, j+1), (i+1, j-1)]
    elif i == len(grid) - 1:
        if j == 0:
            neighbours = [(i, j+1), (i-1, j), (i-1, j+1)]
        elif j == len(grid[0]) - 1:
            neighbours = [(i, j-1), (i-1, j), (i-1, j-1)]
        else:
            neighbours = [(i, j-1), (i, j+1), (i-1, j), (i-1, j+1), (i-1, j-1)]
    else:
        if j == 0:
            neighbours = [(i+1, j), (i-1, j), (i, j+1), (i+1, j+1), (i-1, j+1)]
        elif j == len(grid[0]) - 1:
            neighbours = [(i+1, j), (i-1, j), (i, j-1), (i+1, j-1), (i-1, j-1)]
        else:
            neighbours = [
                (i+1, j), (i-1, j), (i, j+1), (i, j-1),
                (i+1, j+1), (i-1, j+1), (i+1, j-1), (i-1, j-1)
            ]

    for i, j in neighbours:
        if grid[i][j].status:
            aliveCells += 1

    if status:
        if aliveCells == 2 or aliveCells == 3:
            return 1
        return 0
    else:
        if aliveCells == 3:
            return 1
        return 0


def calculateCellAmount(winX, winY, cellSize):
    rows = int(winY / cellSize)
    cols = int(winX / cellSize)
    return (rows, cols)


def main():
    # Initialize the window
    pygame.init()
    pygame.display.set_caption('Conways Game of Life')
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # Create some important variables
    cellSize = 15
    animationSpeed = 0
    info = pygame.display.Info()
    winX, winY = info.current_w, info.current_h
    rows, cols = calculateCellAmount(winX, winY, cellSize)
    marginY = (winY - rows*cellSize) / 2
    marginX = (winX - cols*cellSize) / 2
    timerStart = time.time()

    # Create the grid and the cells
    grid = []
    i, j = marginX, marginY
    for row in range(rows):
        row = []
        for col in range(cols):
            row.append(Cell(i, j, cellSize))
            i += cellSize
        grid.append(row)
        i = marginX
        j += cellSize

    # Main window loop
    while True:
        animationSpeed = eventHandler(animationSpeed)
        draw(screen, grid)

        if (time.time() - timerStart > animationSpeed):
            grid = update(grid)
            timerStart = time.time()

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
