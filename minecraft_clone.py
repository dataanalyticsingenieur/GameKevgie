import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions (increased to fit the larger world)
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Minecraft Clone")

# Colors
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BACKGROUND_COLOR = GRAY  # Setzen Sie die Hintergrundfarbe auf Grau.

# Block size
BLOCK_SIZE = 40

# Player dimensions (smaller to resemble a human shape)
PLAYER_WIDTH = BLOCK_SIZE // 2
PLAYER_HEIGHT = int(BLOCK_SIZE * 1.5)

# Create a larger world (grid of blocks)
world = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
]

# Player position
player_x, player_y = 5, 5  # Startposition des Spielers in der Welt

# Player color
PLAYER_COLOR = (255, 0, 0)  # Rot

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Bewegung des Spielers
            if event.key == pygame.K_UP and player_y > 0:
                player_y -= 1
            elif event.key == pygame.K_DOWN and player_y < len(world) - 1:
                player_y += 1
            elif event.key == pygame.K_LEFT and player_x > 0:
                player_x -= 1
            elif event.key == pygame.K_RIGHT and player_x < len(world[0]) - 1:
                player_x += 1

    # Clear screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the world
    for row_index, row in enumerate(world):
        for col_index, block in enumerate(row):
            x = col_index * BLOCK_SIZE
            y = row_index * BLOCK_SIZE
            if block == 1:
                pygame.draw.rect(screen, GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))
            elif block == 2:
                pygame.draw.rect(screen, BROWN, (x, y, BLOCK_SIZE, BLOCK_SIZE))
            elif block == 0:
                pygame.draw.rect(screen, GRAY, (x, y, BLOCK_SIZE, BLOCK_SIZE))

    # Draw the player
    pygame.draw.rect(
        screen,
        PLAYER_COLOR,
        (
            player_x * BLOCK_SIZE + (BLOCK_SIZE - PLAYER_WIDTH) // 2,  # Center horizontally
            player_y * BLOCK_SIZE + (BLOCK_SIZE - PLAYER_HEIGHT) // 2,  # Center vertically
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
        ),
    )

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
