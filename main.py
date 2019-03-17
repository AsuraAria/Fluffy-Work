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

pygame.display.set_caption("Fluffy French Adventure")

icon = pygame.image.load("player/icon.png").convert_alpha()
pygame.display.set_icon(icon)

#Chargement et du fond
fond = pygame.image.load("map/fond.png").convert()

#Chargement du menu
menu0 = pygame.image.load("textures/menu0.png").convert()
menu1 = pygame.image.load("textures/menu1.png").convert()

#Chargement de la map
maps = []
mapsPos = []
mapsCollision = []
pxarray = []

for i in range(5):
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

botsPos = [[0,792.0, 1180, "?!#*&@"],[1,1794.0, 180.0, "?!#*&@"],[2,2586.0, 250.0,"door"],
            [3,750.0, 450.0,"sign"],[4,790.0, 90.0,"door"],
            [5,600.0, 550.0, "statue"],[6,790.0, 90.0,"door"],
            [7,900.0, 600.0,"sign"],[8,790.0, 90.0,"door"],
            [9,600.0, 600.0,"sign"]]
    
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
             ""],[],
             
             ["Allez sur la pierre à côté de la porte","",""],[],
             
             ["Statue : To over pass me, you have to say the",
              "opposite of : 'sous'","",
              "Fluffy : (choose the anwser with WASD key)",
              "W - Sous    A - Sur   S - A coté","D - Porte"],[],
              
              ["NE PAS ALLER SUR L'EAU","",""],[],
              
              ["/!\\ Ruines en construction /!\\","Revenez plus tard",""]]
            
bots = []
for i in range(10):
    bots.append(pygame.image.load("bots/bot"+str(i)+".png").convert_alpha())
    if (i==3 or i==7 or i==9):
        bots[i] = pygame.transform.scale(bots[i],(140,140))
    elif (i==5):
        bots[i] = pygame.transform.scale(bots[i],(140,280))
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

heart = pygame.image.load("textures/heart.png").convert_alpha()

counter = 0
intro = []
for i in range(1,80):
    intro.append(pygame.image.load("Sheer_Madness/troll"+str(i)+".png").convert())
    intro[i-1] = pygame.transform.scale(intro[i-1],(1280,720))

# init
pygame.key.set_repeat(1, 30)
liste_key = pygame.key.get_pressed()

pygame.mixer.music.load("musique/bruitages/vent ou mer.wav")
son_trappe = pygame.mixer.Sound("musique/bruitages/plaque pression fenetre.wav")
son_dial = pygame.mixer.Sound("musique/bruitages/clickparole.wav")
son_porte = pygame.mixer.Sound("musique/bruitages/porte.wav")
son_dico = pygame.mixer.Sound("musique/bruitages/clickparole1.wav")
son_victory = pygame.mixer.Sound("musique/bruitages/victoire.wav")

# DICO

fond_dico = pygame.image.load("textures/fond_dicodec.png").convert_alpha()

dico = [["Pierre","Noun : Rock"],["Sur","Noun : Above"],["Sous","Noun : Under"],["A coté","Noun : Next to"]]
positiondict = 0
n = 0;
#=========================
# Variables
#=========================

HP = 3

difficulty = -1

White = (255,255,255)
Black = (0,0,0)

# Var Frame

W = frameSize[0]
H = frameSize[1]

# Var Fct

menu = 0 #on est pas dans un menus
nearBot = -1

whichDiag = 0
resetA = True;
resetE = True;
resetH = True;
resetB = True;
resetMouse = True;

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
gabriolaFontB = pygame.font.SysFont("gabriola", 60, 1)
gabriolaFont = pygame.font.SysFont("gabriola", 75, 0)
# Character : constantia
constantiaFont = pygame.font.SysFont("constantia", 54)

resetVictorySound = True;

#Statue

answering = False
choice = -1
resetChoice = True

# Scene 1
switch1 = False;

# Scene 2
switch2 = False;

#=========================
# Fonctions
#=========================

def isColliding(side):
    #global mapsCollision
    global currentMap
    global mapsPos
    global pxarray
    global resetVictorySound
    global switch1
    global HP
    global menu

    wallDetected = False

    upL = (int(W/2-mapsPos[currentMap][0]),int(H/2-mapsPos[currentMap][1]+40))
    upR = (int(W/2-mapsPos[currentMap][0]+70), int(H/2-mapsPos[currentMap][1]+40))
    doL = (int(W/2-mapsPos[currentMap][0]), int(H/2-mapsPos[currentMap][1]+70))
    doR = (int(W/2-mapsPos[currentMap][0]+70), int(H/2-mapsPos[currentMap][1]+70))
    
    center = (int(W/2-mapsPos[currentMap][0]+40),int(H/2-mapsPos[currentMap][1]+40))

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

    if (pygame.Color(pxarray[currentMap][center[0]][center[1]]) == (0, 255, 0, 0)):
        son_trappe.play()
        switch1 = True;
        if (resetVictorySound):
            resetVictorySound = False
            son_victory.play()
    if (pygame.Color(pxarray[currentMap][center[0]][center[1]]) == (0, 250, 0, 0)):
        son_trappe.play()
    if (pygame.Color(pxarray[currentMap][center[0]][center[1]]) == (0, 0, 255, 0)):
        menu = 0;
        currentMap = 0;

    return wallDetected

def isBot():
    global curentMap
    global mapsPos
    global pxarray
    global bots
    global botsPos
    global W
    global H

    if (currentMap == 0):
        for i in range(3):
            if (sqrt((-mapsPos[currentMap][0]+W/2-botsPos[i][1])**2+(-mapsPos[currentMap][1]+H/2-botsPos[i][2])**2) <= 150):
                return botsPos[i][0]
    elif (currentMap == 1):
        for i in range(3,5):
            if (sqrt((-mapsPos[currentMap][0]+W/2-botsPos[i][1])**2+(-mapsPos[currentMap][1]+H/2-botsPos[i][2])**2) <= 150):
                return botsPos[i][0]
    elif (currentMap == 2):
        for i in range(5,7):
            if (sqrt((-mapsPos[currentMap][0]+W/2-botsPos[i][1])**2+(-mapsPos[currentMap][1]+H/2-botsPos[i][2])**2) <= 150):
                return botsPos[i][0]
    elif (currentMap == 3):
        for i in range(7,9):
            if (sqrt((-mapsPos[currentMap][0]+W/2-botsPos[i][1])**2+(-mapsPos[currentMap][1]+H/2-botsPos[i][2])**2) <= 150):
                return botsPos[i][0]
    elif (currentMap == 4):
        for i in range(9,10):
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
        son_porte.play()
    if (nearBot == 4 and switch1):
        son_porte.play()
        currentMap = 2
        mapsPos[currentMap][0] = -144
        mapsPos[currentMap][1] = -445
        resetVictorySound = True
        dico.append(["Aller","Verb : To go"])
        dico.append(["Porte","Noun : Door"])
    if (nearBot == 6 and switch2):
        son_porte.play()
        currentMap = 3
        resetVictorySound = True
        mapsPos[currentMap][0] = -144
        mapsPos[currentMap][1] = -445
        dico.append(["Eau","Noun : Water"])
    if (nearBot == 8):
        son_porte.play()
        currentMap = 4
        son_victory.play()
        resetVictorySound = True
        mapsPos[currentMap][0] = -144
        mapsPos[currentMap][1] = -445
        dico.append(["Ne pas","Negation : Do not"])

def evaluateAnwser():
    global currentMap
    global answering
    global nearBot
    global HP
    global isInteracting
    global whichDiag
    global menu
    global switch2
    
    if (nearBot == 5):
        if (choice != -1):
            if (choice == 1):
                answering = False
                switch2 = True
                isInteracting = False;
                whichDiag = 0
                son_victory.play()
                resetVictorySound = True
            else:
                HP-= 1;
                if (HP == 0):
                    menu = 0
                    HP = 3
                    currentMap = 0;
                
    print(HP)
    

#=========================
# While
#=========================

#BOUCLE INFINIE
continuer = 1
while continuer:
    #print(mapsPos[currentMap])
    
    for event in pygame.event.get():
        if event.type==QUIT:
            continuer=0
            pygame.quit()
        if event.type == MOUSEBUTTONDOWN:
            
            if (menu == 0 and resetMouse):
                if (150<event.pos[0])&(event.pos[0]<460)&(280<event.pos[1])&(event.pos[1]<380):
                    if (difficulty == -1):
                        menu = 1
                    else:
                        menu = 2
                    son_trappe.play()
                if (150<event.pos[0])&(event.pos[0]<475)&(460<event.pos[1])&(event.pos[1]<570):
                    son_trappe.play()
                    continuer=0
                    pygame.quit()
                resetMouse = False
                    
            if (menu == 1 and resetMouse):
                if (150<event.pos[0])&(event.pos[0]<460)&(280<event.pos[1])&(event.pos[1]<380):
                    son_trappe.play()
                    difficulty = 0
                    menu = -1
                    pygame.mixer.music.play(-1)
                if (150<event.pos[0])&(event.pos[0]<475)&(460<event.pos[1])&(event.pos[1]<570):
                    son_trappe.play()
                    difficulty = 1
                    menu = -1
                    pygame.mixer.music.play(-1)
                resetMouse = False
        
        if event.type == MOUSEBUTTONUP:
            resetMouse = True
        
        if event.type == KEYDOWN:
            k = event.key
            print(event.key);
            
            if (k == 13):
                speed = -20
            if (k == 8):
                speed = -2
            
            if (k==27 and menu != -1):
                menu = 0
            
            # zqsd : 97 119 100 115
            if (k == 97):
                direction[0] = 1;
                choice = 1
            elif (k == 119):
                direction[1] = 1;
                if (menu == 3 and resetH):
                    positiondict = (max(0,positiondict-1))
                    resetH = False
                choice = 0
            elif (k == 100):
                direction[2] = 1;
                choice = 3
            elif (k == 115):
                direction[3] = 1;
                if (menu == 3 and resetB):
                    positiondict=min(n-1,positiondict+1)
                    resetB = False
                choice = 2
            
            if (k == 101 and nearBot != -1 and resetE):
                if (isInteracting):
                    whichDiag += 3
                if (botsPos[nearBot][3] != "door"):
                    son_dial.play()
                resetE = False
                isInteracting = True
                choice = -1
            if (k == 113 and resetA and dicodecFound):
                if menu == 2:
                    menu = 3
                elif menu ==3:
                    menu = 2
                son_dico.play()
                resetA = False
                choice = -1

        if event.type == KEYUP:
            k = event.key

            if (k == 97):
                direction[0] = 0;
                resetChoice = True;
            elif (k == 119):
                direction[1] = 0;
                resetH = True
                resetChoice = True;
            elif (k == 100):
                direction[2] = 0;
                resetChoice = True;
            elif (k == 115):
                direction[3] = 0;
                resetB = True
                resetChoice = True;
            if (k == 101):
                resetE = True
            if (k == 113):
                resetA = True

    #print(resetSpace)
    if (menu == -1 and continuer!=0):
        if (counter<79):
            frame.blit(intro[counter], (0,0))
            counter += 1
            pygame.time.delay(90)
        elif (counter>=79):
            menu = 2
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.load("musique/fluffy_work_principal.wav")
            pygame.mixer.music.play(-1)
    elif (menu == 0 and continuer!=0):
        frame.blit(menu0, (0,0))
    elif (menu == 1 and continuer!=0):
        frame.blit(menu1, (0,0))
    elif (menu == 2 and continuer!=0):
        
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
        elif(currentMap == 2):
            for i in range(5,7):
                if (botsPos[i][3] == "statue"):
                    frame.blit(bots[i],(botsPos[i][1]+mapsPos[currentMap][0],botsPos[i][2]+mapsPos[currentMap][1]-150))
                else:
                    frame.blit(bots[i],(botsPos[i][1]+mapsPos[currentMap][0],botsPos[i][2]+mapsPos[currentMap][1]))
        elif(currentMap == 3):
            for i in range(7,9):
                frame.blit(bots[i],(botsPos[i][1]+mapsPos[currentMap][0],botsPos[i][2]+mapsPos[currentMap][1]))
        elif(currentMap == 4):
            for i in range(9,10):
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
        
        for i in range(HP):
            frame.blit(heart,(i*70,0))
        
        if (isInteracting):
            print(nearBot)
            if (botsPos[nearBot][3] != "door"):
                frame.blit(box,(40,H-250-20))
                if (whichDiag <= len(botsDiag[nearBot])-1):
                    text1 = constantiaFont.render(botsDiag[nearBot][whichDiag],1,White)
                    text2 = constantiaFont.render(botsDiag[nearBot][whichDiag+1],1,White)
                    text3 = constantiaFont.render(botsDiag[nearBot][whichDiag+2],1,White)
                    frame.blit(text1,(110,H-250+20))
                    frame.blit(text2,(110,H-250+80))
                    frame.blit(text3,(110,H-250+140))
                    if (botsPos[nearBot][3] != "statue" and whichDiag == len(botsDiag[nearBot])-1):
                        whichDiag+=3;
                else:
                    if (botsPos[nearBot][3] == "statue" and not answering):
                        answering = True
                        
                    if (answering):
                        frame.blit(text1,(110,H-250+20))
                        frame.blit(text2,(110,H-250+80))
                        frame.blit(text3,(110,H-250+140))
                        if (resetChoice):
                            resetChoice = False
                            evaluateAnwser()
                    else:
                        isInteracting = False;
                        whichDiag = 0
                        
                    if (nearBot == 1):
                       dicodecFound = True
                       
                sprite = 0
            else:
                evaluateDoor()
    
    elif (menu == 3 and continuer!=0):
        
        #aframe.blit(fond, (0,0))
        frame.blit(fond_dico,(0,0))
        n = len(dico)
        noms = dico[positiondict:min(n,positiondict+9)]
        lonfinal = len(noms)
        i=0
        str_dicodex = gabriolaFontB.render("My DICODEX", 1, Black)
            
        frame.blit(str_dicodex, (W/2-gabriolaFontB.size("My DICODEX")[0]/2, 80))
        for i in range(0,lonfinal):
            mot = gabriolaFont.render(noms[i][0], 1, Black)
            frame.blit(mot, (100, 110+i*60))
        
        trad = dico[positiondict][1]
        #print(trad)
        #trad = dictionnaire.cherche_fr_ang(trad,dictionnaire.dict)
        #print(trad)
        affiche_trad = gabriolaFont.render(trad, 1, Black)
        frame.blit(affiche_trad, (500, 210))
        
    # UPDATE
    
    if (continuer!=0):
        pygame.display.flip()
        pygame.time.delay(10)
