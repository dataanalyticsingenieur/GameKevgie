import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 600
TILE = 40
ROWS = HEIGHT // TILE
COLS = WIDTH // TILE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Minecraft mit Crafting (Python 3.13.8)")

# ---------------------------
# Farben
# ---------------------------
colors = {
    "sky": (135, 206, 235),
    "grass": (60, 200, 60),
    "dirt": (120, 70, 30),
    "stone": (100, 100, 100),
    "wood": (140, 90, 40),
    "plank": (170, 120, 60),
}

# ---------------------------
# Welt
# ---------------------------
world = [["sky" for _ in range(COLS)] for _ in range(ROWS)]

for y in range(ROWS - 5, ROWS):
    for x in range(COLS):
        if y == ROWS - 5:
            world[y][x] = "grass"
        elif y < ROWS - 2:
            world[y][x] = "dirt"
        else:
            world[y][x] = "stone"

# Ein paar Holzblöcke
for x in range(5, 10):
    world[ROWS - 6][x] = "wood"

# ---------------------------
# Inventar
# ---------------------------
inventory = {
    "dirt": 0,
    "grass": 0,
    "stone": 0,
    "wood": 0,
    "plank": 0,
    "stick": 0,
    "pickaxe": 0
}

selected = "dirt"

# ---------------------------
# Crafting Rezepte
# ---------------------------
recipes = {
    "plank": {"wood": 1},
    "stick": {"plank": 2},
    "pickaxe": {"stone": 3, "stick": 2}
}

font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 36)

def draw_world():
    for y in range(ROWS):
        for x in range(COLS):
            block = world[y][x]
            color = colors.get(block, colors["sky"])
            pygame.draw.rect(screen, color,
                             (x * TILE, y * TILE, TILE, TILE))
            pygame.draw.rect(screen, (0,0,0),
                             (x * TILE, y * TILE, TILE, TILE), 1)

def draw_ui():
    y_offset = 10
    for item, amount in inventory.items():
        text = f"{item}: {amount}"
        img = font.render(text, True, (0,0,0))
        screen.blit(img, (10, y_offset))
        y_offset += 22

    selected_text = big_font.render(f"Selected: {selected}", True, (0,0,0))
    screen.blit(selected_text, (300, 10))

    help_text = font.render("C = Crafting Menü", True, (0,0,0))
    screen.blit(help_text, (300, 50))

def craft(item):
    recipe = recipes[item]

    # prüfen
    for mat, amount in recipe.items():
        if inventory.get(mat, 0) < amount:
            return

    # abziehen
    for mat, amount in recipe.items():
        inventory[mat] -= amount

    # hinzufügen
    if item == "plank":
        inventory["plank"] += 4
    elif item == "stick":
        inventory["stick"] += 4
    elif item == "pickaxe":
        inventory["pickaxe"] += 1

def get_grid_pos(mouse):
    mx, my = mouse
    return mx // TILE, my // TILE

running = True
craft_menu = False

while running:
    screen.fill(colors["sky"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1: selected = "dirt"
            if event.key == pygame.K_2: selected = "grass"
            if event.key == pygame.K_3: selected = "stone"
            if event.key == pygame.K_4: selected = "wood"

            if event.key == pygame.K_c:
                craft_menu = not craft_menu

            # Crafting Buttons
            if craft_menu:
                if event.key == pygame.K_p:
                    craft("plank")
                if event.key == pygame.K_s:
                    craft("stick")
                if event.key == pygame.K_x:
                    craft("pickaxe")

        # Block abbauen
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = get_grid_pos(pygame.mouse.get_pos())
            if 0 <= x < COLS and 0 <= y < ROWS:
                block = world[y][x]
                if block != "sky":
                    inventory[block] += 1
                    world[y][x] = "sky"

        # Block setzen
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x, y = get_grid_pos(pygame.mouse.get_pos())
            if 0 <= x < COLS and 0 <= y < ROWS:
                if world[y][x] == "sky" and inventory.get(selected,0) > 0:
                    world[y][x] = selected
                    inventory[selected] -= 1

    draw_world()
    draw_ui()

    # Crafting Menü anzeigen
    if craft_menu:
        pygame.draw.rect(screen, (200,200,200), (250,150,400,250))
        pygame.draw.rect(screen, (0,0,0), (250,150,400,250), 3)

        screen.blit(big_font.render("CRAFTING", True, (0,0,0)), (370,170))

        screen.blit(font.render("P = 1 Wood → 4 Planks", True, (0,0,0)), (300,220))
        screen.blit(font.render("S = 2 Plank → 4 Stick", True, (0,0,0)), (300,250))
        screen.blit(font.render("X = 3 Stone + 2 Stick → Pickaxe", True, (0,0,0)), (300,280))

    pygame.display.flip()

pygame.quit()
sys.exit()

