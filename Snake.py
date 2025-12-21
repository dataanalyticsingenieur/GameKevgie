import pygame
import random

pygame.init()

# Constants
WIN_SIZE = 800
SQUARE_COUNT = 20
SQUARE_SIZE = WIN_SIZE // SQUARE_COUNT
DELAY = 100
START_LENGTH = 5

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Snake")

# Initialize snake
head_column = SQUARE_COUNT // 2
head_row = SQUARE_COUNT // 2
snake_length = START_LENGTH
body_parts = []

# Initialize apple
apple_row = random.randint(0, SQUARE_COUNT - 1)
apple_column = random.randint(0, SQUARE_COUNT - 1)

# Movement variables
step_x = 0
step_y = 0

def draw_square(column, row, color):
    x = column * SQUARE_SIZE
    y = row * SQUARE_SIZE
    pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

run = True
while run:
    pygame.time.delay(DELAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and step_x != -1:
        step_x = 1
        step_y = 0
    elif keys[pygame.K_LEFT] and step_x != 1:
        step_x = -1
        step_y = 0
    elif keys[pygame.K_UP] and step_y != 1:
        step_x = 0
        step_y = -1
    elif keys[pygame.K_DOWN] and step_y != -1:
        step_x = 0
        step_y = 1

    if step_x != 0 or step_y != 0:
        body_parts.append((head_column, head_row))
        head_column += step_x
        head_row += step_y
    if len(body_parts) > snake_length:
        body_parts.pop(0)

    if head_column < 0 or head_column >= SQUARE_COUNT or head_row < 0 or head_row >= SQUARE_COUNT or (head_column, head_row) in body_parts:
        head_column = SQUARE_COUNT // 2
        head_row = SQUARE_COUNT // 2
        snake_length = START_LENGTH
        body_parts = []
        step_x = 0
        step_y = 0

    if head_column == apple_column and head_row == apple_row:
        snake_length += 1
        apple_row = random.randint(0, SQUARE_COUNT - 1)
        apple_column = random.randint(0, SQUARE_COUNT - 1)

    screen.fill(BLACK)

    apple_x = apple_column * SQUARE_SIZE
    apple_y = apple_row * SQUARE_SIZE
    pygame.draw.rect(screen, RED, (apple_x, apple_y, SQUARE_SIZE, SQUARE_SIZE))

    for part in body_parts:
        draw_square(part[0], part[1], GREEN)

    draw_square(head_column, head_row, GREEN)

    for i in range(SQUARE_COUNT):
        line_pos = SQUARE_SIZE * i
        pygame.draw.line(screen, WHITE, (line_pos, 0), (line_pos, WIN_SIZE), 2)
        pygame.draw.line(screen, WHITE, (0, line_pos), (WIN_SIZE, line_pos), 2)

    pygame.display.update()

pygame.quit()
