import pygame
init = pygame.init()
print(init)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hello World")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))    
    pygame.display.flip()
pygame.quit()
