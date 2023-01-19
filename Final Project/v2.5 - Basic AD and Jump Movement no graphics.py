import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'images')
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
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 80
        self.speedx = 0
        self.speedy = 0
        self.jumping = False
        self.original_y = self.rect.y

    def update(self):
        self.speedx = 0
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -7 # Speed of the player
        if keystate[pygame.K_RIGHT]:
            self.speedx = 7 # Speed of the player
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
    screen.fill(RED)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
    
