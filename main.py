import os
import pygame
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time .Clock()
HEIGHT = 800
WIDTH = 1200
DISPLAY_COLOR =(0,0,0)
BG=pygame.transform.scale(pygame.image.load("background.png"),(WIDTH,HEIGHT))
BG_X1=0
BG_X2=BG.get_width()
BG_MOVE = 3

PLAYER_COLOR=(0,0,0)
FONT = pygame.font.SysFont("Verdana",40)
main_display = pygame.display.set_mode((WIDTH, HEIGHT))


IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player = pygame.image.load("player.png").convert_alpha()
PLAYER_SIZE = (player.get_width(),player.get_height())
player_rect = pygame.Rect(WIDTH//5, HEIGHT//2, *PLAYER_SIZE)
player_move=[0,0]

def create_enemy():
    enemy = pygame.image.load("enemy.png").convert_alpha()
    ENEMY_SIZE = (enemy.get_width(),enemy.get_height())
    enemy_rect = pygame.Rect(WIDTH,random.randint(HEIGHT//6,5*HEIGHT//6),*ENEMY_SIZE)
    enemy_move=[random.randint(-8,-4),0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus = pygame.image.load("bonus.png").convert_alpha()
    BONUS_SIZE = (bonus.get_width(),bonus.get_height()) 
    bonus_rect = pygame.Rect(random.randint(WIDTH//5, 4*WIDTH//5),-bonus.get_height(),*BONUS_SIZE)
    bonus_move=[0,random.randint(1,3)]
    return [bonus, bonus_rect, bonus_move]

def draw_del(elements):
    is_collide = False
    for element in elements:
        element[1]=element[1].move(element[2])
        main_display.blit(element[0],element[1])
        if player_rect.colliderect(element[1]): 
            is_collide=True
            elements.pop(elements.index(element))
        if element[1].left<-element[0].get_width() or element[1].bottom > HEIGHT + element[0].get_height() :
            elements.pop(elements.index(element))
    return [elements, is_collide]

CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, 2000)
pygame.time.set_timer(CHANGE_IMAGE, 200)
enemies=[]
bonuses=[]

score = 0
image_index=0

playing = True

while playing:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing=False
        if event.type == CREATE_ENEMY and len(enemies)<10:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS and len(bonuses)<4:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player=pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index+=1
            if image_index>=len(PLAYER_IMAGES):image_index=0

    BG_X1-=BG_MOVE
    BG_X2-=BG_MOVE

    if BG_X1 <-BG.get_width():
        BG_X1=BG.get_width()
    if BG_X2 <-BG.get_width():
        BG_X2=BG.get_width()

    main_display.blit(BG,(BG_X1,0))
    main_display.blit(BG,(BG_X2,0))
    
    keys=pygame.key.get_pressed()
    
    player_move=[0,0]
    if keys[K_DOWN] and player_rect.bottom < 6*HEIGHT//7:
        player_move=[0,4]
    if keys[K_UP] and player_rect.bottom > HEIGHT//7+PLAYER_SIZE[1]:
        player_move=[0,-4]
    if keys[K_RIGHT] and player_rect.right < 6*WIDTH//7:
        player_move=[4,0]
    if keys[K_LEFT] and player_rect.right > WIDTH//7+PLAYER_SIZE[0]:
        player_move=[-4,0]    
    player_rect=player_rect.move(player_move)

    k=draw_del(enemies)
    enemies=k[0]
    if k[1]: 
        playing=False
    k=draw_del(bonuses)
    bonuses=k[0]
    if k[1]: 
        score+=1

    main_display.blit(player,player_rect)
    main_display.blit(FONT.render(str(score),True, PLAYER_COLOR), (WIDTH-50,30))

    pygame.display.flip()