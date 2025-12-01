import pygame
import random

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)     # Red
]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [1, 0, 0]]
]

class Tetrimino:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(COLORS)
        self.x = SCREEN_WIDTH // 2 // BLOCK_SIZE * BLOCK_SIZE
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def move(self, dx, dy, grid):
        if not self.collides(dx, dy, grid):
            self.x += dx * BLOCK_SIZE
            self.y += dy * BLOCK_SIZE

    def collides(self, dx, dy, grid):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = (self.x // BLOCK_SIZE) + x + dx
                    new_y = (self.y // BLOCK_SIZE) + y + dy
                    if new_x < 0 or new_x >= len(grid[0]) or new_y >= len(grid) or grid[new_y][new_x]:
                        return True
        return False

def clear_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = len(grid) - len(new_grid)
    new_grid = [[0] * len(grid[0]) for _ in range(lines_cleared)] + new_grid
    return new_grid, lines_cleared

def draw_grid(screen, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def draw_tetrimino(screen, tetrimino):
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetrimino.color, pygame.Rect(tetrimino.x + x * BLOCK_SIZE, tetrimino.y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def auto_move(tetrimino, grid):
    if not tetrimino.collides(0, 1, grid):
        tetrimino.move(0, 1, grid)
    else:
        for y, row in enumerate(tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[(tetrimino.y // BLOCK_SIZE) + y][(tetrimino.x // BLOCK_SIZE) + x] = tetrimino.color
        grid, _ = clear_lines(grid)
        tetrimino.shape = random.choice(SHAPES)
        tetrimino.color = random.choice(COLORS)
        tetrimino.x = SCREEN_WIDTH // 2 // BLOCK_SIZE * BLOCK_SIZE
        tetrimino.y = 0
        if tetrimino.collides(0, 0, grid):
            return False
    return True

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()
    grid = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    tetrimino = Tetrimino(random.choice(SHAPES))
    run = True
    fall_time = 0

    while run:
        fall_speed = 0.5
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            run = auto_move(tetrimino, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_tetrimino(screen, tetrimino)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
