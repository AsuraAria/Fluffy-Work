# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 15:50:56 2019

@author: Fluffy Corp

"""

#=========================
# Import
#=========================

import pygame
from pygame.locals import *

#import varglobal

#=========================
# Init Window
#=========================

pygame.init()

frame = pygame.display.set_mode((1280, 720))
frameSize = pygame.display.get_surface().get_size()

#Chargement et du fond
fond = pygame.image.load("map/fond.png").convert()

#Chargement de la map
maps = pygame.image.load("map/map2.png").convert()
maps = pygame.transform.scale(maps,(3000,3000))
mapsPos = maps.get_rect()


fond_menu_principal = pygame.image.load("textures_menus/fond_menu_principal.png").convert()
fond_menu_principal = pygame.transform.scale(fond_menu_principal,(1280, 720))

#Chargement et collage du personnage
player = [[],[]]
for i in range(4):
    player[0].append(pygame.image.load("player/fluffitten"+str(i)+".png").convert_alpha())
    player[0][i] = pygame.transform.scale(player[0][i],(70,70))
for i in range(4):
    player[1].append(pygame.image.load("player/fluffitten"+str(i)+".1.png").convert_alpha())
    player[1][i] = pygame.transform.scale(player[1][i],(70,70))
#frame.blit(perso, (200,300))

# init
pygame.key.set_repeat(1, 30)
liste_key = pygame.key.get_pressed()

#=========================
# Variables
#=========================

# Var Frame

W = 1280
H = 720

# Var Fct

menu = 2 #on est dans un menus

# Var Map

mapPos = [0,0];

# Var Player

speed = -2;
spriteCount = 20;
sprite = 0;

direction = [0,0,0,0]
finalDir = 0;
#=========================
# While
#=========================

#frame.blit(maps, mapPos)
        
#pygame.display.flip()

#BOUCLE INFINIE
continuer = 1
while continuer:
    for event in pygame.event.get():
        if event.type==QUIT:
            loop=0
            pygame.quit()
        if event.type == KEYDOWN:
            k = event.key
            print(event.key);
            
            # zqsd : 97 119 100 115
            
            if (k == 97):
                direction[0] = 1;
            elif (k == 119):
                direction[1] = 1;
            elif (k == 100):
                direction[2] = 1;
            elif (k == 115):
                direction[3] = 1;
                
        if event.type == KEYUP:
            k = event.key
            
            if (k == 97):
                direction[0] = 0;
            elif (k == 119):
                direction[1] = 0;
            elif (k == 100):
                direction[2] = 0;
            elif (k == 115):
                direction[3] = 0;
    
    
    if (direction[0] == 1):
        finalDir = 0
        mapsPos = mapsPos.move(-speed, 0);
        sprite = (sprite+1)%spriteCount
    elif (direction[1] == 1):
        finalDir = 1
        mapsPos = mapsPos.move(0, -speed);
        sprite = (sprite+1)%spriteCount
    elif (direction[2] == 1):
        finalDir = 2
        mapsPos = mapsPos.move(speed, 0);
        sprite = (sprite+1)%spriteCount
    elif (direction[3] == 1):
        finalDir = 3
        mapsPos = mapsPos.move(0, speed);
        sprite = (sprite+1)%spriteCount
    else:
        finalDir = 3
        sprite = 0
    
    if (menu == 0):
        frame.blit(fond, (0,0))
        frame.blit(maps, mapsPos)
        frame.blit(player[int(sprite/(spriteCount/2))][finalDir], (W/2,H/2))
    
    if menu ==1:#afficher le menu principal
        frame.blit(fond, (0,0))
        frame.blit(fond_menu_principal,(0,0))
        
        bouton_play = pygame.image.load("textures_menus/bouton_play.png").convert()
        bouton_quit = pygame.image.load("textures_menus/bouton_quit.png").convert()
        frame.blit(bouton_play,(60,600))
        frame.blit(bouton_quit,(900,600))
        
        if event.type == MOUSEBUTTONDOWN :
            if (60<event.pos[0])&(event.pos[0]<260)&(600<event.pos[1])&(event.pos[1]<660):
                print("play")
            if (900<event.pos[0])&(event.pos[0]<1160)&(600<event.pos[1])&(event.pos[1]<660):
                print("quit")
                
    if menu ==2:#afficher le menu difficulte
        frame.blit(fond, (0,0))
        frame.blit(fond_menu_principal,(0,0))
        
        bouton_easy = pygame.image.load("textures_menus/bouton_easy.png").convert()
        bouton_hard = pygame.image.load("textures_menus/bouton_hard.png").convert()
        frame.blit(bouton_easy,(60,600))
        frame.blit(bouton_hard,(900,600))
        
        if event.type == MOUSEBUTTONDOWN :
            if (60<event.pos[0])&(event.pos[0]<260)&(600<event.pos[1])&(event.pos[1]<660):
                print("easy")
            if (900<event.pos[0])&(event.pos[0]<1160)&(600<event.pos[1])&(event.pos[1]<660):
                print("hard")    
    
    pygame.display.flip()
    pygame.time.delay(10)
                