import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path


pygame.mixer.pre_init(44100, -16, 2, 512 )
mixer.init()
pygame.init()

# Bildschirmgröße
screen_width = 700
screen_height = 700

# Clock für FPS
clock = pygame.time.Clock()
fps = 60


# Bildschirm erstellen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')


font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)




# Tilegröße
tile_size = 35
game_over = 0
main_menu = True
level = 1
max_levels = 2
score = 0

white = (255, 255, 255)
blue = (0, 0, 255)


# Bilder laden
sun_img = pygame.image.load('img1/sun.png')
bg_img = pygame.image.load('img1/sky.png')
restart_img = pygame.image.load('img1/restart_btn.png')
start_img = pygame.image.load('img1/start_btn.png')
exit_img = pygame.image.load('img1/exit_btn.png') 

#load sounds
pygame.mixer.music.load('img1/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000 )
coin_fx = pygame.mixer.Sound('img1/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img1/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img1/game_over.wav')
game_over_fx.set_volume(0.5)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))




def reset_level(level):
    player.reset(100, screen_height - 110)
    blob_group.empty()
    platform_group.empty()
    lava_group.empty()
    exit_group.empty()

    world_data = []  

    if path.exists(f'img1/level{level}_data'):
        with open(f'img1/level{level}_data', 'rb') as pickle_in:
            world_data = pickle.load(pickle_in)

    return World(world_data)






# BUTTON-KLASSE
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action


# PLAYER-KLASSE
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 2
        col_thresh = 20

        if game_over == 0:
            key = pygame.key.get_pressed()
            # Springen
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            # Bewegung
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
            # Animation wechseln
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction >= 0:
                self.image = self.images_right[self.index]
            else:
                self.image = self.images_left[self.index]

            # Schwerkraft
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            self.in_air = True

            # Kollisionen
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    
                    elif self.vel_y > 0:
                        dy = tile[1].top - self.rect.bottom
                       
                        self.vel_y = 0
                        self.in_air = False

            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                game_over_fx.play()
            
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1


            for platform in platform_group:

    # X-Kollision
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # Y-Kollision
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

        # Fallen → auf Plattform landen
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = 0
                        self.in_air = False

        # Springen → Kopf stößt an
                    elif self.vel_y < 0:
                        self.rect.top = platform.rect.bottom
                        dy = 0
                        self.vel_y = 0    

                    if platform.move_x != 0:   
                        self.rect.x += platform.move_direction


         
                       



            # Position aktualisieren
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        #Spieler immer anzeigen + Rect
        screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.direction = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'img1/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (30, 60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img1/ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


# WELT-KLASSE
class World():
    def __init__(self, data):
        self.tile_list = []

        dirt_img = pygame.image.load('img1/dirt.png')
        grass_img = pygame.image.load('img1/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size)
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(col_count * tile_size,  row_count * tile_size, 1, 0 )
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size,  row_count * tile_size, 0, 1)
                    platform_group.add(platform)      
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2)+ 5)
                    lava_group.add(lava)

                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)

                if tile == 8:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))    
                    exit_group.add(exit)



                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
           


# ENEMY-KLASSE
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img1/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img1/platform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
               





# LAVA-KLASSE
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img1/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img1/coin.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        






class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img1/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int (tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        


player = Player(100, screen_height - 110)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()

score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

if path.exists(f'img1/level{level}_data'):
    pickle_in = open(f'img1/level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
    world = World(world_data)

# Buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)
# GAME LOOP
run = True
while run:
    clock.tick(fps)

    # Hintergrund
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (50, 50))

    if main_menu:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:

        world.draw()

# Gegner bewegen
        if game_over == 0:   
            blob_group.update()
            platform_group.update()

        # Kollision Coins
        if pygame.sprite.spritecollide(player, coin_group, True):
            score += 1
            coin_fx.play()
        draw_text('X ' + str (score),font_score, white, tile_size - 5, 35 )
            

       
        world.draw()
        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)
     

        # Spieler updaten
        
        game_over = player.update(game_over)

        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0

        if game_over == 1:    
            level += 1 
            if level <= max_levels:
                world_data = []
                world = reset_level(level)
                game_over = 0

            else:
                draw_text('YOU WIN! ', font, blue,  (screen_width // 2 ) - 140, screen_height // 2)
                if restart_button.draw():
                     level = 1
                     world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0


    # Event-Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()



pygame.quit()