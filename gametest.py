import pygame
import sys

pygame.init()

# Konstanten
WIN_WIDTH = 800
WIN_HEIGHT = 600
BALL_SIZE = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
FPS = 60

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bildschirm einrichten
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Pong Spiel")

# Ballposition und -geschwindigkeit
ball_x = WIN_WIDTH // 2
ball_y = WIN_HEIGHT // 2
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y

# Schlägerpositionen
paddle1_y = WIN_HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle2_y = WIN_HEIGHT // 2 - PADDLE_HEIGHT // 2

# Funktion zum Zeichnen des Balls
def draw_ball(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, BALL_SIZE, BALL_SIZE))

# Funktion zum Zeichnen der Schläger
def draw_paddles(paddle1_y, paddle2_y):
    pygame.draw.rect(screen, WHITE, (10, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIN_WIDTH - 20, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Spielschleife
def game_loop():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, paddle1_y, paddle2_y
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= PADDLE_SPEED
        if keys[pygame.K_s] and paddle1_y < WIN_HEIGHT - PADDLE_HEIGHT:
            paddle1_y += PADDLE_SPEED
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and paddle2_y < WIN_HEIGHT - PADDLE_HEIGHT:
            paddle2_y += PADDLE_SPEED

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_y <= 0 or ball_y >= WIN_HEIGHT - BALL_SIZE:
            ball_speed_y *= -1

        if ball_x <= 20 and paddle1_y < ball_y < paddle1_y + PADDLE_HEIGHT:
            ball_speed_x *= -1
        elif ball_x >= WIN_WIDTH - 30 and paddle2_y < ball_y < paddle2_y + PADDLE_HEIGHT:
            ball_speed_x *= -1
        elif ball_x < 0 or ball_x > WIN_WIDTH:
            ball_x = WIN_WIDTH // 2
            ball_y = WIN_HEIGHT // 2
            ball_speed_x *= -1

        screen.fill(BLACK)
        draw_ball(ball_x, ball_y)
        draw_paddles(paddle1_y, paddle2_y)
        pygame.display.update()
        clock.tick(FPS)

game_loop()