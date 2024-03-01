import pygame
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time .Clock()
HEIGHT = 800
WIDTH = 1200
DISPLAY_COLOR =(0,0,0)
PLAYER_COLOR=(255,255,255)
ENEMY_COLOR = (0,0,255)
BONUS_COLOR = (255,0,0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

PLAYER_SIZE = (20,20)

player = pygame.Surface(PLAYER_SIZE)
player.fill(PLAYER_COLOR)
player_rect = player.get_rect()
player_move=[0,0]

def create_enemy():
    ENEMY_SIZE = (30,30) 
    enemy = pygame.Surface(ENEMY_SIZE)
    enemy.fill(ENEMY_COLOR)
    enemy_rect = pygame.Rect(WIDTH,random.randint(0, HEIGHT),*ENEMY_SIZE)
    enemy_move=[random.randint(-6,-1),0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    BONUS_SIZE = (30,30) 
    bonus = pygame.Surface(BONUS_SIZE)
    bonus.fill(BONUS_COLOR)
    bonus_rect = pygame.Rect(random.randint(WIDTH//5, 4*WIDTH//5),0,*BONUS_SIZE)
    bonus_move=[0,random.randint(1,3)]
    return [bonus, bonus_rect, bonus_move]

def draw_del(elements):
    for element in elements:
        element[1]=element[1].move(element[2])
        main_display.blit(element[0],element[1])
        if element[1].left<0 or element[1].bottom>HEIGHT:
            elements.pop(elements.index(element))
    return elements

CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, 2000)
enemies=[]
bonuses=[]

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

    main_display.fill(DISPLAY_COLOR)
    
    keys=pygame.key.get_pressed()
    
    player_move=[0,0]
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_move=[0,1]
    if keys[K_UP] and player_rect.bottom > PLAYER_SIZE[1]:
        player_move=[0,-1]
    if keys[K_RIGHT] and player_rect.right  < WIDTH:
        player_move=[1,0]
    if keys[K_LEFT] and player_rect.right > PLAYER_SIZE[0]:
        player_move=[-1,0]    
    player_rect=player_rect.move(player_move)

    enemies=draw_del(enemies)
    bonuses=draw_del(bonuses)

    main_display.blit(player,player_rect)

    pygame.display.flip()