import pygame
import os
pygame.init()


width = 1200
height = 700

#--------------Some Variables Defined Here-------------
camera_x = 0
camera_walk = 8


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cowboy Shooter')

assets = os.path.join(os.getcwd(), 'Assets')
background = pygame.transform.scale(pygame.image.load(os.path.join(assets, 'background.png')), (width, height)) #change size
dirt = pygame.transform.scale(pygame.image.load(os.path.join(assets, 'sandground.png')), (50, 50)) #change size
ground = pygame.transform.scale(pygame.image.load(os.path.join(assets, 'sandground.png')), (50, 50)) #change size
player_image = pygame.transform.scale(pygame.image.load(os.path.join(assets, 'cowboy.png')), (72, 72))
background_rect = background.get_rect()
enemy_image = pygame.transform.scale(pygame.image.load(os.path.join(assets, 'enemy.png')), (72, 72))

#------------------Functions Defined Here----------------

def intro_screen():
    surface.blit(background, background_rect)
    draw_text(surface, "Western Shooter", 64, width / 2, height / 4)
    draw_text(surface, "Use LEFT, RIGHT, and UP arrow keys to move! Use the Spacebar to shoot!", 22,
              width / 2, height / 2)                                                 #Intro text showing the instructions!
    draw_text(surface, "Press any key to begin", 18, width / 2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        fps = 60
        clock = pygame.time.Clock()
        clock.tick(fps)
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
    
def colliding(rect1, rect2):
    if not (rect1.x + rect1.width <= rect2.x or rect2.x + rect2.width <= rect1.x):
        if not(rect1.y + rect1.height <= rect2.y or rect2.y + rect2.height <= rect1.y):
            return True
    return False

def draw_window(current_map, player, enemies):
    surface.blit(background, (0, 0))
    
    for y in range(len(current_map)):
        for x in range(camera_x, len(current_map[y])):
            if current_map[y][x] == 'X':
                if y != 0 and current_map[y - 1][x] != 'X':
                    surface.blit(dirt, ((x - camera_x) * 50, y* 50))
                else:
                    surface.blit(ground, ((x - camera_x) * 50, y *50))
    for enemy in enemies:
        surface.blit(enemy.image, (enemy.x - (camera_x * 50), enemy.y))                                                                
    
    
                                                                    
                    
    surface.blit(player.image, (player.x, player.y))
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    fps = 60
    
    player = Player(50, 479, 47, 71, player_image, 'R')
    
    enemies = []
    enemies.append(Enemy(500, 379, 47, 71, 3, enemy_image, 'R', 200))
    # Game Loop
    running = True
    game_over = True
    while run:
        if game_over:
            intro_screen() # I added an intro screen for when you start up the game
        
        game_over = False # This gets made False here so that the intro screen does not show again after you enter the game.
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
                
        key_pressed = pygame.key.get_pressed()
        player.handle_movement(key_pressed)
        
        draw_window(tile_map, player, enemies)

#------------------------------------------------
tile_map = [
    '....................................................................',
    '....................................................................',
    '....................................................................',
    '....................................................................',
    '....................................................................',
    '....................................................................',
    '........................................XXXXXXX.....................',
    '.....................................XXXXXXXXXXXX...................',
    '...................................XXXXXXXXXXXXXXXX.................',
    '.........XXXXXXX..................XXXXXXXXXXXXXXXXXXXX..............',
    '................................XXXXXXXXXXXXXXXXXXXXXXXX............',
    'XXXXXXXX.........XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXX...XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]
#------------------------------------------------------------

#-----------------Classes Defined Here---------------

class Character:
    def __init__(self, x, y, width, height, speed, image, looking):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.image = image
        self.looking = looking
    
    def would_collide(self, x, y, current_map):
        character_rect = pygame.Rect(self.x + x, self.y + y, self.width, self.height)
        
        for y in range(len(current_map)):
            for x in range(camera_x, len(current_map[y])):
                if current_map[y][x] == 'X':
                    rect = pygame.Rect((x - camera_x) * 50, y * 50, 50, 50)
                    if colliding(character_rect, rect):
                        return True
        return False

class Player(Character):
    def __init__(self, x, y, width, height, image ,looking):
        super().__init__(x, y, width, height, 5, image, looking)
        self.jumping = False
        self.falling = False
        self.max_jumps = 25
        self.jumps_left = self.max_jumps
    
    def handle_movement(self, key):
        global camera_x
        
        if self.jumping:
            if not(self.would_collide(0, -self.speed, tile_map)) and self.jumps_left != 0:
                self.y -= self.speed
            else:
                self.jumping = False
                self.falling = True
                self.jumps_left = self.max_jumps
            self.jumps_left -= 1
        
        if not(self.would_collide(0, self.speed, tile_map)) and not(self.jumping):
            self.falling = True
            self.y += self.speed
        else:
            self.falling = False
            
        if key[pygame.K_a] and not(self.would_collide(-self.speed, 0, tile_map)):
            if self.looking != 'L':
                self.looking = 'L'
                self.image = pygame.transform.flip(self.image, True, False)
            if self.x - self.speed >= 0:
                self.x -= self.speed
            if (self.x % (camera_walk * 50) == 0 or self.x - self.speed < 0) and camera_x - camera_walk >= 0: #Checks to see if there has been enough blocks to move the camera
                camera_x -= camera_walk
                self.x += camera_walk * 50
            elif (self.x % (camera_walk * 50) == 0 or self.x - self.speed < 0):
                self.x += camera_x * 50
                camera_x = 0
        
        if key[pygame.K_d] and not(self.would_collide(self.speed, 0, tile_map)):
            if self.looking != 'R':
                self.looking = 'R'
                self.image = pygame.transform.flip(self.image, True, False)
            if self.x + self.speed + self.width <= width:   
                self.x += self.speed
            if (self.x % (camera_walk * 50) == 0 or self.x + self.speed + self.width > width) and camera_x + camera_walk + 30 <= len(tile_map[0]):
                camera_x += camera_walk
                self.x -= camera_walk * 50
            elif (self.x % (camera_walk * 50) == 0 or self.x + self.speed + self.width > width):
                self.x -= ((len(tile_map[0]) - 30) - camera_x) * 50
                camera_x = len(tile_map[0]) - 30
        
        if key[pygame.K_w] and not(self.jumping) and not (self.falling):
            self.jumping = True
                   
class Enemy(Character):
    def __init__(self, x, y, width, height, speed, image, looking, r):
        super().__init__(x, y, width, height, speed, image, looking)
        self.initial_x = x
        self.range = r


if __name__ == '__main__':
    main()