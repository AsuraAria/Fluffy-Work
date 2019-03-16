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

#=========================
# Init Window
#=========================
import varglobal

pygame.init()

frame = pygame.display.set_mode((1280, 720))

#Chargement et collage du fond
#fond = pygame.image.load("background.jpg").convert()
#frame.blit(fond, (0,0))

#Chargement et collage du personnage
#perso = pygame.image.load("perso.png").convert_alpha()
#frame.blit(perso, (200,300))

#=========================
#
#=========================
pygame.display.flip()

#BOUCLE INFINIE
continuer = 1
while continuer:
    for event in pygame.event.get():
        if event.type==QUIT:
            loop=0
            pygame.quit()
        if event.type == KEYDOWN:
            print(event.key);
