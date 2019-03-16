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

mapsCollision = pygame.image.load("map/map2Mask.png").convert()
mapsCollision = pygame.transform.scale(mapsCollision,(3000,3000))
pxarray = []
pxarray = pygame.PixelArray(mapsCollision.copy()) #248 177 33

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

W = frameSize[0]
H = frameSize[1]

# Var Fct

menu = 1 #on est pas dans un menus

# Var Map

mapPos = [0,0];

# Var Player

speed = -2;
spriteCount = 20;
sprite = 0;

direction = [0,0,0,0]
finalDir = 0;

#=========================
# Fonctions
#=========================

def isColliding(side):
    #global mapsCollision
    global mapsPos
    global pxarray

    wallDetected = False

    upL = (int(W/2-mapsPos[0]-10),int(H/2-mapsPos[1]-10))
    upR = (int(W/2-mapsPos[0]+70+10), int(H/2-mapsPos[1]-10))
    doL = (int(W/2-mapsPos[0]-10), int(H/2-mapsPos[1]+70+10))
    doR = (int(W/2-mapsPos[0]+70+10), int(H/2-mapsPos[1]+70+10))

    print(pygame.Color(pxarray[doR[0]][doR[1]]))



    return wallDetected

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
            #print(event.key);

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


    if (direction[0]==1 or direction[1]==1 or direction[2]==1 or direction[3]==1):
        sprite = (sprite+1)%spriteCount
        if (direction[0] == 1 and not isColliding(0)):
            finalDir = 0
            mapsPos = mapsPos.move(-speed, 0);
        if (direction[1] == 1 and not isColliding(1)):
            finalDir = 1
            mapsPos = mapsPos.move(0, -speed);
        if (direction[2] == 1 and not isColliding(2)):
            finalDir = 2
            mapsPos = mapsPos.move(speed, 0);
        if (direction[3] == 1 and not isColliding(3)):
            finalDir = 3
            mapsPos = mapsPos.move(0, speed);
    else:
        finalDir = 3
        sprite = 0

    #if (menu == 0):
    frame.blit(fond, (0,0))
    frame.blit(maps, mapsPos)
    if (direction[1] == 1):
        frame.blit(player[int(sprite/(spriteCount/2))][1], (W/2,H/2))
    elif (direction[3] == 1):
        frame.blit(player[int(sprite/(spriteCount/2))][3], (W/2,H/2))
    else:
        frame.blit(player[int(sprite/(spriteCount/2))][finalDir], (W/2,H/2))


    pygame.display.flip()
    pygame.time.delay(10)
