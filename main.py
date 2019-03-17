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
from math import *

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
maps = []
mapsPos = []
mapsCollision = []
pxarray = []

for i in range(2):
    maps.append(pygame.image.load("map/map"+str(i)+".png").convert())
    if (i==0):
        maps[i] = pygame.transform.scale(maps[i],(3000,3000))
    else:
        maps[i] = pygame.transform.scale(maps[i],(1650,1050))
    
    mapsPos.append(maps[i].get_rect())
    mapsPos[i] = mapsPos[i].move(-290,-1560)
    
    mapsCollision.append(pygame.image.load("map/map"+str(i)+"Mask.png").convert())
    if (i==0):
        mapsCollision[i] = pygame.transform.scale(mapsCollision[i],(3000,3000))
    else:
        mapsCollision[i] = pygame.transform.scale(mapsCollision[i],(1650,1050))
    
    pxarray.append(pygame.PixelArray(mapsCollision[i].copy()))

#Chargement et collage du personnage
player = [[],[]]
for i in range(4):
    player[0].append(pygame.image.load("player/fluffitten"+str(i)+".png").convert_alpha())
    player[0][i] = pygame.transform.scale(player[0][i],(70,70))
for i in range(4):
    player[1].append(pygame.image.load("player/fluffitten"+str(i)+".1.png").convert_alpha())
    player[1][i] = pygame.transform.scale(player[1][i],(70,70))
#frame.blit(perso, (200,300))

botsPos = [[0,792.0, 1180, "?!#*&@"],[1,1794.0, 432.0, "?!#*&@"],[2,2586.0, 250.0,"door"],[3,740.0, 450.0,"sign"],[4,790.0, 90.0,"door"]]
botsDiag = [["Fluffy : Hi, my name is Fluffy and I was hired",
             "in the archeologic team here. I am here to",
             "help with the new language you discovered.",
             "Chief : Ok, you have to go meet Ragnard, our",
             "expert in antic languages. Go north, he is",
             "waiting for you at the camp !"],
    
            ["Expert : Hi ! You are the new one ? Good. You",
             "will need this : It is a DICODEX !",
             "It will automatically save any word you will",
             "learn during your exploration. There are",
             "already some words in it, you should check",
             "them before you go.",
             "Go East to the temple, I'll come to see you",
             "later. Good luck !",
             ""],[],["Allez sur la pierre à côté de la porte","",""]]
            
bots = []
for i in range(5):
    bots.append(pygame.image.load("bots/bot"+str(i)+".png").convert_alpha())
    if (i==3):
        bots[i] = pygame.transform.scale(bots[i],(140,140))
    else:
        bots[i] = pygame.transform.scale(bots[i],(70,70))

keyTuto = [0,0,0,0]
dicodecFound = False
tuto = []
for i in range(3):
    tuto.append(pygame.image.load("textures/tuto"+str(i)+".png").convert_alpha())
    tuto[i] = pygame.transform.scale(tuto[i],(420,120))

box = pygame.image.load("textures/box.png").convert_alpha()
box = pygame.transform.scale(box,(1200,250))
isInteracting = False;

# init
pygame.key.set_repeat(1, 30)
liste_key = pygame.key.get_pressed()

#=========================
# Variables
#=========================

White = (255,255,255)
Black = (0,0,0)

# Var Frame

W = frameSize[0]
H = frameSize[1]

# Var Fct

menu = 0 #on est pas dans un menus
nearBot = -1

whichDiag = 0
resetSpace = True;

#=======

# Var Map

currentMap = 0;

# Var Player

speed = -2;
spriteCount = 20;
sprite = 0;

direction = [0,0,0,0]
finalDir = 0;

# Font

# Statue et Ecritaux : gabriola
gabriolaFont = pygame.font.SysFont("gabriola", 54)
# Character : constantia
constantiaFont = pygame.font.SysFont("constantia", 54)

# Scene 1
#=========================
# Fonctions
#=========================

def isColliding(side):
    #global mapsCollision
    global currentMap
    global mapsPos
    global pxarray

    wallDetected = False

    upL = (int(W/2-mapsPos[currentMap][0]),int(H/2-mapsPos[currentMap][1]+40))
    upR = (int(W/2-mapsPos[currentMap][0]+70), int(H/2-mapsPos[currentMap][1]+40))
    doL = (int(W/2-mapsPos[currentMap][0]), int(H/2-mapsPos[currentMap][1]+70))
    doR = (int(W/2-mapsPos[currentMap][0]+70), int(H/2-mapsPos[currentMap][1]+70))

    #print(pygame.Color(pxarray[doR[0]][doR[1]]))

    if (side == 0):
        if (pygame.Color(pxarray[currentMap][doL[0]-5][doL[1]]) == (0, 248, 177, 33) or pygame.Color(pxarray[currentMap][upL[0]-5][upL[1]]) == (0, 248, 177, 33)):
            return True
    if (side == 1):
        if (pygame.Color(pxarray[currentMap][upL[0]][upL[1]-5]) == (0, 248, 177, 33) or pygame.Color(pxarray[currentMap][upR[0]][upR[1]-5]) == (0, 248, 177, 33)):
            return True;
    if (side == 2):
        if (pygame.Color(pxarray[currentMap][upR[0]+5][upR[1]]) == (0, 248, 177, 33) or pygame.Color(pxarray[currentMap][doR[0]+5][doR[1]]) == (0, 248, 177, 33)):
            return True;
    if (side == 3):
        if (pygame.Color(pxarray[currentMap][doL[0]][doL[1]+5]) == (0, 248, 177, 33) or pygame.Color(pxarray[currentMap][doR[0]][doR[1]+5]) == (0, 248, 177, 33)):
            return True;

    return wallDetected

def isBot():
    global mapsPos
    global pxarray
    global bots
    global botsPos
    global W
    global H

    botDetected = False

    for i in range(len(bots)):
        if (sqrt((-mapsPos[currentMap][0]+W/2-botsPos[i][1])**2+(-mapsPos[currentMap][1]+H/2-botsPos[i][2])**2) <= 150):
            return botsPos[i][0]
    
    return -1
    #if (side == 0):

def evaluateDoor():
    global nearBot
    global currentMap
    global mapsPos
    global isInteracting
    
    isInteracting = False
    
    if (nearBot == 2):
        currentMap = 1
        mapsPos[currentMap][0] = -144
        mapsPos[currentMap][1] = -445
    if (nearBot == 4):
        currentMap = 2
        

#=========================
# While
#=========================

#frame.blit(maps, mapPos)

#pygame.display.flip()

#BOUCLE INFINIE
continuer = 1
while continuer:
    #print(mapsPos[currentMap])
    
    for event in pygame.event.get():
        if event.type==QUIT:
            loop=0
            pygame.quit()
        if event.type == KEYDOWN:
            k = event.key
            #print(event.key);
            
            if (k == 13):
                speed = -20
            if (k == 8):
                speed = -2
            
            # zqsd : 97 119 100 115
            if (k == 97):
                direction[0] = 1;
            elif (k == 119):
                direction[1] = 1;
            elif (k == 100):
                direction[2] = 1;
            elif (k == 115):
                direction[3] = 1;
            if (k == 101 and nearBot != -1 and resetSpace):
                if (isInteracting):
                    whichDiag += 3
                resetSpace = False
                isInteracting = True

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
            if (k == 101):
                resetSpace = True;

    #print(resetSpace)
    if (menu == 0):
        
        if (not isInteracting):
            if (direction[0]==1 or direction[1]==1 or direction[2]==1 or direction[3]==1):
                sprite = (sprite+1)%spriteCount
                if (direction[0] == 1 and -mapsPos[currentMap][0]+W/2>=0 and not isColliding(0)):
                    finalDir = 0
                    mapsPos[currentMap] = mapsPos[currentMap].move(-speed, 0);
                    keyTuto[0] = 1
                if (direction[1] == 1 and -mapsPos[currentMap][1]+H/2>=0 and not isColliding(1)):
                    finalDir = 1
                    mapsPos[currentMap] = mapsPos[currentMap].move(0, -speed);
                    keyTuto[1] = 1
                if (direction[2] == 1 and -mapsPos[currentMap][0]+W/2+70<=2990 and not isColliding(2)):
                    finalDir = 2
                    mapsPos[currentMap] = mapsPos[currentMap].move(speed, 0);
                    keyTuto[2] = 1
                if (direction[3] == 1 and -mapsPos[currentMap][1]+H/2+70<=2990 and not isColliding(3)):
                    finalDir = 3
                    mapsPos[currentMap] = mapsPos[currentMap].move(0, speed);
                    keyTuto[3] = 1
            else:
                sprite = 0
        
        #if (menu == 0):
        frame.blit(fond, (0,0))
        frame.blit(maps[currentMap], mapsPos[currentMap])
        print((-mapsPos[currentMap][0]+W/2,-mapsPos[currentMap][1]+H/2))
        
        #Bots
        if (currentMap == 0):
            for i in range(3):
                frame.blit(bots[i],(botsPos[i][1]+mapsPos[currentMap][0],botsPos[i][2]+mapsPos[currentMap][1]))
        elif (currentMap == 1):
            for i in range(3,5):
                frame.blit(bots[i],(botsPos[i][1]+mapsPos[currentMap][0],botsPos[i][2]+mapsPos[currentMap][1]))
            
        if (direction[1] == 1 and not isInteracting):
            frame.blit(player[int(sprite/(spriteCount/2))][1], (W/2,H/2))
        elif (direction[3] == 1 and not isInteracting):
            frame.blit(player[int(sprite/(spriteCount/2))][3], (W/2,H/2))
        else:
            frame.blit(player[int(sprite/(spriteCount/2))][finalDir], (W/2,H/2))
            
        nearBot = isBot()
        
        if (keyTuto != [1,1,1,1]):
            frame.blit(tuto[0],(W/2+100,H/2-100))
        if (dicodecFound):
            frame.blit(tuto[2],(W-310,H-75))
            
        if (nearBot != -1 and not isInteracting):
            keyTuto = [1,1,1,1]
            frame.blit(tuto[1],(W/2+100,H/2-100))
        
        
        if (isInteracting):
            #print(nearBot)
            if (botsPos[nearBot][3] != "door"):
                frame.blit(box,(40,H-250-20))
                if (whichDiag <= len(botsDiag[nearBot])-1):
                    text1 = constantiaFont.render(botsDiag[nearBot][whichDiag],1,White)
                    text2 = constantiaFont.render(botsDiag[nearBot][whichDiag+1],1,White)
                    text3 = constantiaFont.render(botsDiag[nearBot][whichDiag+2],1,White)
                    frame.blit(text1,(110,H-250+20))
                    frame.blit(text2,(110,H-250+80))
                    frame.blit(text3,(110,H-250+140))
                else:
                    isInteracting = False;
                    whichDiag = 0
                    if (nearBot == 1):
                       dicodecFound = True
                sprite = 0
            else:
                evaluateDoor()
        
    # UPDATE
    
    pygame.display.flip()
    pygame.time.delay(10)
