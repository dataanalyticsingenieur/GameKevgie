import pygame
import sys
import random
import math

# Initialisierung
pygame.init()

# Konstanten
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
BALL_RADIUS = 15
BALL_SPEED = 5
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Bildschirm einrichten
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Billiard")

# Kugeln erstellen
balls = [
    {"pos": [200, 200], "vel": [random.choice([-BALL_SPEED, BALL_SPEED]), random.choice([-BALL_SPEED, BALL_SPEED])], "color": RED},
    {"pos": [400, 200], "vel": [random.choice([-BALL_SPEED, BALL_SPEED]), random.choice([-BALL_SPEED, BALL_SPEED])], "color": BLUE},
]

# Funktion zur Kollisionserkennung
def check_collision(ball1, ball2):
    dx = ball1["pos"][0] - ball2["pos"][0]
    dy = ball1["pos"][1] - ball2["pos"][1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance < 2 * BALL_RADIUS

# Funktion zur Behandlung von Kollisionen
def handle_collision(ball1, ball2):
    dx = ball1["pos"][0] - ball2["pos"][0]
    dy = ball1["pos"][1] - ball2["pos"][1]
    distance = math.sqrt(dx**2 + dy**2)

    if distance == 0:
        return

    # Normalisieren
    nx = dx / distance
    ny = dy / distance

    # Relativer Geschwindigkeitsvektor
    dvx = ball1["vel"][0] - ball2["vel"][0]
    dvy = ball1["vel"][1] - ball2["vel"][1]

    # Impuls entlang der Normalen
    impulse = dvx * nx + dvy * ny

    # Geschwindigkeiten anpassen
    ball1["vel"][0] -= impulse * nx
    ball1["vel"][1] -= impulse * ny
    ball2["vel"][0] += impulse * nx
    ball2["vel"][1] += impulse * ny

# Hauptspielschleife
clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Bildschirm aktualisieren
    screen.fill(GREEN)

    # Kugeln bewegen
    for ball in balls:
        ball["pos"][0] += ball["vel"][0]
        ball["pos"][1] += ball["vel"][1]

        # Kollision mit den Wänden
        if ball["pos"][0] - BALL_RADIUS < 0 or ball["pos"][0] + BALL_RADIUS > SCREEN_WIDTH:
            ball["vel"][0] *= -1
        if ball["pos"][1] - BALL_RADIUS < 0 or ball["pos"][1] + BALL_RADIUS > SCREEN_HEIGHT:
            ball["vel"][1] *= -1

    # Kollision zwischen Kugeln
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if check_collision(balls[i], balls[j]):
                handle_collision(balls[i], balls[j])

    # Kugeln zeichnen
    for ball in balls:
        pygame.draw.circle(screen, ball["color"], (int(ball["pos"][0]), int(ball["pos"][1])), BALL_RADIUS)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()