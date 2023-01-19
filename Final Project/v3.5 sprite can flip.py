import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Pygame template - skeleton for a new pygame project
WIDTH = 680  # width of our game window
HEIGHT = 580 # height of our game window
FPS = 30 # frames per second

#------Colors Defined Here-------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#-----------Classes Defined Here------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (60, 58)) # Scale the player model smaller
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 80
        self.speedx = 0
        self.speedy = 0
        self.jumping = False
        self.original_y = self.rect.y
        self.facing_right = True

    def update(self):
        self.speedx = 0
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -7 # Speed of the player
            self.facing_right = False
            self.image = pygame.transform.flip(self.image, True, False)
            
        if keystate[pygame.K_RIGHT]:
            self.speedx = 7 # Speed of the player
            self.facing_right = True
            self.image = pygame.transform.flip(self.image, True, False)
        if keystate[pygame.K_UP]:
            self.jump()
        
        # Boundaries for not leaving the defined area
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # If the player has reached the maximum height of the jump, start moving back down
        if self.rect.y < self.original_y - 100:
            self.speedy = 10 # Downward speed

        # If the player has landed, stop moving
        if self.rect.y >= self.original_y:
            self.speedy = 0
            self.jumping = False
            self.rect.y = self.original_y

    def jump(self):
        if not self.jumping:
            self.speedy = -10 # Initial upward speed
            self.jumping = True








# initialize pygame and create window

pygame.init()
pygame.mixer.init()  # for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))# Creates window using your width and height
pygame.display.set_caption("Shooter") # name of window
clock = pygame.time.Clock()# Keeps track of speed of game


#Game Graphics
player_img = pygame.image.load(path.join(img_dir, "cowboy.png")).convert()
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
ground = pygame.image.load(path.join(img_dir, "dirtslab.png")).convert()

#----Sprites Made-----
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game Loop
running = True
while running:
    # keep running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    
    # Update
    all_sprites.update()
    # Draw / Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    screen.blit(ground, (500, 500))
    screen.blit(ground, (250, 500))
    screen.blit(ground, (100, 500))
    screen.blit(ground, (0, 500))
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()