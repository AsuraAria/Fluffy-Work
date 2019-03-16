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
maps = pygame.transform.scale(maps,(3000,3000));
mapsPos = maps.get_rect()

#Chargement et collage du personnage
player = pygame.image.load("player/fluffitten.png").convert_alpha()
player = pygame.transform.scale(player,(70,70));
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

menu = 0 #on n'est pas dans un menus

# Var Map

mapPos = [0,0];

# Var Player

speed = -1;

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
            if (k == 119):
                direction[1] = 1;
            if (k == 100):
                direction[2] = 1;
            if (k == 115):
                direction[3] = 1;
                
        if event.type == KEYUP:
            k = event.key
            
            if (k == 97):
                direction[0] = 0;
            if (k == 119):
                direction[1] = 0;
            if (k == 100):
                direction[2] = 0;
            if (k == 115):
                direction[3] = 0;
    
    
    if (direction[0] == 1):
        mapsPos = mapsPos.move(-speed, 0);
    elif (direction[1] == 1):
        mapsPos = mapsPos.move(0, -speed);
    elif (direction[2] == 1):
        mapsPos = mapsPos.move(speed, 0);
    elif (direction[3] == 1):
        mapsPos = mapsPos.move(0, speed);
    
    #if (menu == 0):
    frame.blit(fond, (0,0))
    frame.blit(maps, mapsPos)
    frame.blit(player, (W/2,H/2))
        
    pygame.display.flip()
                