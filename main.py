import pygame,sys

from pygame.locals import *
from random import randint

class Crosshair(pygame.sprite.Sprite):
    def __init__(self,img_path):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.shoot_sound = pygame.mixer.Sound('sound/shoot.wav')
        self.shoot_sound.set_volume(0.1)

    def shoot(self):
        self.shoot_sound.play()    
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.center = mouse_pos

class Target(pygame.sprite.Sprite):
    def __init__(self,img_path,pos_x,pox_y):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(center = (pos_x, pox_y))

class Button():
    def __init__(self,text,width,height,pos):
        #Core Attributes
        self.pressed = False

        #Top Rectangle
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_rect.center = pos
        self.top_color = (0,0,0)

        #Text
        self.text_surf = gui_font.render(text,True,(255,255,255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    def draw(self):
        pygame.draw.rect(screen,self.top_color,self.top_rect,border_radius = 20)
        screen.blit(self.text_surf,self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (127,127,127)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                return True
        else:
            self.top_color = (0,0,0)

    def update(self):
        self.check_click()

class GameState():
    def __init__(self):
        self.state = "menu"

    def game(self):
        global hit
        target_x = randint(200,screen_width-200)
        target_y = randint(200,screen_height-200)
        collide = pygame.sprite.spritecollide(crosshair,target_grp,False)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                crosshair.shoot()
                for target in collide:
                    target.kill()
                    new_target = Target('images/target.png',target_x,target_y)
                    target_grp.add(new_target)  
                    hit += 1            

        screen.blit(backgound_surf,background_rect)
        display_text(f'Hit:{hit}',screen_width/2,100,64,(255,255,255))
        display_text(f'Press ESC to exit',screen_width/2,screen_height-100,64,(255,255,255))
        target_grp.draw(screen)
        crosshair_grp.draw(screen)
        crosshair_grp.update()
        pygame.display.flip()

    def menu(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if b1.check_click():
                    self.state = 'game'
                if b2.check_click():
                    pygame.quit()
                    sys.exit()

        screen.blit(backgound_surf,background_rect)
        display_text(f'Target Shooter',screen_width/2,200,128,(255,255,255))
        b1.update()
        b2.update()
        b1.draw()
        b2.draw()
        crosshair_grp.draw(screen)       
        crosshair_grp.update()
        pygame.display.flip()

    def stateManager(self):
        if self.state == 'menu':
            self.menu()
        if self.state == 'game':
            self.game()

def display_text(text,pos_x,pos_y,size,color):
    font = pygame.font.Font('font/kelik.otf', size)
    font_surf = font.render(text,True,color)
    font_rect = font_surf.get_rect(center = (pos_x,pos_y))
    screen.blit(font_surf,font_rect)

# General
pygame.init()
clock = pygame.time.Clock()
obj_info = pygame.display.Info()
gameState = GameState()
pygame.mouse.set_visible(False)
hit = 0

# Game Screen
screen_width = obj_info.current_w
screen_height = obj_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))

# Background
backgound_surf = pygame.image.load('images/background.png').convert_alpha()
background_rect = backgound_surf.get_rect(center= (screen_width/2,screen_height/2))

# Font
gui_font = pygame.font.Font('font/kelik.otf',64)

# Crosshair
crosshair = Crosshair('images/crosshair.png')
crosshair_grp = pygame.sprite.Group()
crosshair_grp.add(crosshair)

# Target
target = Target('images/target.png',randint(200,screen_width-200),randint(200,screen_height-200))
target_grp = pygame.sprite.Group()
target_grp.add(target)

# Button
b1 = Button('Play',300,100,(screen_width/2,screen_height/2))
b2 = Button('Exit',300,100,(screen_width/2,screen_height/2+200))

# Game Loop
while True:
    gameState.stateManager()
    clock.tick(60)