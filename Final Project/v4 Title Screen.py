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

#----------Functions Defined Here-------------
def intro_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Western Shooter", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Use LEFT, RIGHT, and UP arrow keys to move! Use the Spacebar to shoot!", 22,
              WIDTH / 2, HEIGHT / 2)                                                 #Intro text showing the instructions!
    draw_text(screen, "Press any key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()                  #If statements to see if you quit out, or if any key is pressed,
            if event.type == pygame.KEYUP:     #it will begin the game!
                waiting = False


#The function for drawing any sort of text
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK) 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
    
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
            if self.facing_right:
                self.facing_right = False
                self.image = pygame.transform.flip(self.image, True, False)
            
        if keystate[pygame.K_RIGHT]:
            self.speedx = 7 # Speed of the player
            if not self.facing_right:
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
game_over = True
while running:
    if game_over:
        intro_screen() # I added an intro screen for when you start up the game
        # keep running at the right speed
    game_over = False # This gets made False here so that the intro screen does not show again after you enter the game.
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
