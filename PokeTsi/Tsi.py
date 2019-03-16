#################################### Intro ####################################


#################################### Import ####################################

import pygame
from pygame.locals import *

import math
import operator
from random import *

################################## Definitions #################################

#Initialisation Pygame et Création fenêtre 
pygame.init()
frame = pygame.display.set_mode((640, 480))

frameSize = pygame.display.get_surface().get_size()

############
#### IMAGES
############

#Chargement Images
fond = pygame.image.load("Ressources/Map/fond.png").convert()
#fond = pygame.image.load("Map 640-480 x3 Quadrillage.png").convert()

###### Map

mapLoaded = []
mapValue = []
listObject = []
position_map = []
pxarray = []
for i in range(0,1):
     mapLoaded.append(pygame.image.load("Ressources/Map/map"+str(i)+".png").convert())
     mapValue.append(pygame.image.load("Ressources/Map/map"+str(i)+"_value.png").convert())
     listObject.append([])
     with open("Ressources/Map/map"+str(i)+"_object.csv", "r") as objectFile:
        for line in objectFile:
             buffer = "".join(line.split('\n')).split(";")
             listObject[i].append(buffer)   
     position_map.append(mapLoaded[i].get_rect())
     #Def array of image
     pxarray.append(pygame.PixelArray(mapValue[i].copy()))

print(listObject)

###### End Map

mainBack = []
mainLeft = []
mainRight = []
mainFront = []

#Chargement sprite perso
for i in range(1,5):
     mainBack.append(pygame.image.load("Ressources/Sprit Perso/back"+str(i)+".png").convert_alpha())
     mainLeft.append(pygame.image.load("Ressources/Sprit Perso/left"+str(i)+".png").convert_alpha()) #.image.set_colorkey((160,152,168))
     mainRight.append(pygame.transform.flip(pygame.image.load("Ressources/Sprit Perso/left"+str(i)+".png").convert_alpha(),True,False))
     mainFront.append(pygame.image.load("Ressources/Sprit Perso/front"+str(i)+".png").convert_alpha())

##     mainBack[i-1].image.set_colorkey((160,152,168))
##     mainLeft[i-1].image.set_colorkey((160,152,168))
##     mainRight[i-1].image.set_colorkey((160,152,168))
##     MainFront[i-1].image.set_colorkey((160,152,168))

#Chargement hitbox Perso
hitbox = pygame.image.load("Ressources/Sprit Perso/Hitbox v2.png").convert_alpha()

#Chargement In Game Menu pic
inGameMenu = pygame.image.load("Ressources/Menu/inGameMenu.png").convert_alpha()

#Chargement image roll for fight
roll_fight = pygame.image.load("Ressources/Menu/roll_fight.png").convert_alpha()

#Chargement image fight
fondFight = pygame.image.load("Ressources/Menu/fondFight.png").convert_alpha()
fight_gui = pygame.image.load("Ressources/Menu/fightMenu.png").convert_alpha()
healthBar = pygame.image.load("Ressources/Menu/healthBar.png").convert_alpha()
place = pygame.image.load("Ressources/Menu/placement.png").convert_alpha()

#Pixel Art pokémon
imageTsi = [0]
rectImageTsi = []
for i in range(len(listTsi)-1):
     imageTsi.append(pygame.image.load("Ressources/Perso/p"+str(i+1)+".png").convert_alpha())
     rectImageTsi.append(imageTsi[i+1].get_rect())

############
#### FIN IMAGES
############
#### DEF VARIABLES
############

#Direction main Perso : trigo rotation 0,1,2,3
direct = 1
sprite = 0

#Def positions map
position_perso = mainBack[0].get_rect()

#Def positions roll_fight
position_roll = roll_fight.get_rect()
print(position_roll)

#Def pygame var and fct
pygame.key.set_repeat(1, 30)
liste_key = pygame.key.get_pressed()

#Def coord main Perso

#x=int(math.floor(position_map[2]/2-position_perso[2]/2))   #296
#y=int(math.floor(position_map[3]/2-position_perso[3]/2))   #215
x=296
y=215
print(x,y)

#Def Hitbox placement in Hitbox Image (+11, +25) dimension(+41,+51)
xHitbox = 11
yHitbox = 26

#Def inGame Menu is displayed
affMenu = False
r_menu = True

#Hautes Herbes
countForFight = 0
positionBefore = position_map

#Variable d'environnement : on map:0, on roll for fight:1,on fight:2
env = 0

#Reset position Image Perso
r_posImage = 1

#Variable d'arret des deplacement
stopMove = False

#Font family (50, 30) et (330, 265)
myfont = pygame.font.SysFont("monospace", 20)

#currentMap
currentMap = 0

#Tsi alea par map
wildTsi = 0

#Tsi of player [(id,lvl),]
deckTsi = [(19,7)]

#Tsi choisi par le joueur
tsiChoosen1 = 1
tsiChoosen2 = 0

curVie1 = 0
curVie2 = 0

################################### Fonctions ##################################

def add(a,b):
     return tuple(map(operator.add,a,b))

#Verif Collisions
def Collision(side):
     isWall = False
     
     #Calcul position absolue à par rapport au coin haut gauche de la map
     #Hitbox image
     coP = [x-position_map[currentMap][0],y-position_map[currentMap][1]]
     #Hibox Réel 2,5D (Pieds du perso)
     coP_hB = add(coP,(11,25))
     #print(coP_hB)
     
     upL = (coP[0]+11,coP[1]+25)
     upR = (coP[0]+41,coP[1]+25)

     doL = (coP[0]+11,coP[1]+51)
     doR = (coP[0]+41,coP[1]+51)
     #print(pygame.Color(pxarray[currentMap][coP[0]+11,coP[1]+51+4]),pygame.Color(pxarray[currentMap][coP[0]+41,coP[1]+51+4]))
          
     for i in [(0,140,70,15),(0,48,96,160)]:
          
          if side == "up":
               if coP_hB[1]-4 > 0:
                    if pygame.Color(pxarray[currentMap][add(upR,(0,-3))])==i or pygame.Color(pxarray[currentMap][add(upL,(0,-3))])==i:
                         isWall = True
               else:
                    isWall = True
               
          if side == "down":
               if coP_hB[1]+26+4 < position_map[currentMap][3]:
                    if pygame.Color(pxarray[currentMap][add(doR,(0,3))])==i or pygame.Color(pxarray[currentMap][add(doL,(0,3))])==i:
                         isWall = True
               else:
                    isWall = True
                    
          if side == "left":
               if coP_hB[0]-4 > 0:
                    if pygame.Color(pxarray[currentMap][add(upL,(-3,0))])==i or pygame.Color(pxarray[currentMap][add(doL,(-3,0))])==i:
                         isWall = True
               else:
                    isWall = True
                    
          if side == "right":
               if coP_hB[0]+30+4 < position_map[currentMap][2]:
                    if pygame.Color(pxarray[currentMap][add(upR,(3,0))])==i or pygame.Color(pxarray[currentMap][add(doR,(3,0))])==i:
                         isWall = True
               else:
                    isWall = True
          
     return isWall


#Affichages Surfaces
def Display():
     global position_map
     global affMenu

     #Aff Fond Vert
     frame.blit(fond, (0,0))

     #Aff Map
     frame.blit(mapLoaded[currentMap], position_map[currentMap])

     #Aff Perso (Sprite and direction)
     if direct == 0:
          frame.blit(mainRight[math.floor(sprite)], (x,y))
     if direct == 1:
          frame.blit(mainBack[math.floor(sprite)], (x,y))
     if direct == 2:
          frame.blit(mainLeft[math.floor(sprite)], (x,y))
     if direct == 3:
          frame.blit(mainFront[math.floor(sprite)], (x,y))

     #Aff hitbox Perso
     frame.blit(hitbox, (x,y))

     #Aff Menu
     if affMenu:
          frame.blit(inGameMenu,(0,0))

     return 7

def ProbForFight():
     global position_map
     global positionBefore
     global countForFight
     global stopMove
     global env
     global r_posImage
     global currentMap
     
     #Haute herbes proba (50,100,40)

     #Calcul position absolue à par rapport au coin haut gauche de la map
     #Hitbox image
     coP = [x-position_map[currentMap][0],y-position_map[currentMap][1]]
     upL = (coP[0]+11,coP[1]+25)
     
     if pygame.Color(pxarray[currentMap][add(upL,(15,13))])==(0,50,100,40) and positionBefore != position_map[currentMap]:
          #Is fight time ?
          countForFight+=1
          #print(countForFight)
          #random for fight
          rand = randint(0,30)
          if countForFight >= 50 and rand == 7:
               stopMove = True
               env = 1
               countForFight = 0
               r_posImage = 1
     
     positionBefore = position_map[currentMap]

     return 7

def DispRoll_Fight():
     global position_roll
     global env
     global direct
     global position_perso
     global r_posImage
     global listObject
     global wildTsi
     global wildLvl
     global currentMap

     ## DEDI MAIN TAMO

     #Direction mouvement bande
     DirBande = [(64,0),(0,48),(-64,0),(0,-48)]
     #Emplacement affichage
     coordAff = [0,0]
     #Nombre d'affichage par coté
     NombreAff = [9,9,9,8,8,7,7,6,6,5,5,4,4,3,3,2,2,1,1,1]
     
     for i in range(20):
          for k in range(NombreAff[i]):
               #Affichage BlackPick en [x,y]
               frame.blit(roll_fight, coordAff)
               
               #Aff Perso (Sprite and direction)
               if direct == 0:
                    frame.blit(mainRight[math.floor(sprite)], (x,y))
               if direct == 1:
                    frame.blit(mainBack[math.floor(sprite)], (x,y))
               if direct == 2:
                    frame.blit(mainLeft[math.floor(sprite)], (x,y))
               if direct == 3:
                    frame.blit(mainFront[math.floor(sprite)], (x,y))
                    
               #Refresg Affichage
               pygame.display.flip()

               #Deplacement pour prochain affichage
               coordAff = add(coordAff, DirBande[i%4])
               #Attente
               pygame.time.delay(10)

     #Lancement du fight
     env = 2
           
     #print(listObject[currentMap])
     randTsi = randint(0,len(listObject[currentMap][0])-1)
     wildTsi = int(listObject[currentMap][0][randTsi])

     randLvl = randint(0,len(listObject[currentMap][1])-1)
     print(randLvl)
     print(listObject[currentMap][1])
     wildLvl = int(listObject[currentMap][1][randLvl])
     
     pygame.time.delay(1000)

     return 7

def Disp_WildFight():
    #### Persos : Enemy et Ally
    #Nom Persos : (50, 30) et (330, 265)
    #Affichage Persos : ((349,17);(618,216)) et ((20,96);(289,295))
    #Taille pixel art 270x200
    global imageTsi
    global xImage1
    global xImage2
    global r_posImage
    global env
    global stopMove
    global wildTsi
    global wildLvl
    global listTsi
    global deckTsi
    global curVie1
    global curVie2
    global tsiChoosen1
    global tsiChoosen2

    ############
    #### AFF TSI FIGHT
    ############
    
    #Affichage Fond et GUI
    frame.blit(fondFight, (0,0))
    frame.blit(fight_gui, (0,0))
    frame.blit(healthBar, (0,0))
    #frame.blit(place,(0,0))
     
    #Definition images a afficher
    imagePerso1 = imageTsi[wildTsi]
    imagePerso2 = imageTsi[deckTsi[tsiChoosen2][0]]

    #Definitions des Surfaces a afficher
    rectImagePerso1 = imagePerso1.get_rect()
    rectImagePerso2 = imagePerso2.get_rect()

    if r_posImage == 1:
        #Def position image
        xImage1 = 349+math.floor(270/2-rectImagePerso1[2]/2)+500
        xImage2 = 20+math.floor(270/2-rectImagePerso2[2]/2)-500
        curVie1 = int(listTsi[wildTsi][4])+int(listTsi[wildTsi][5])*int(wildLvl-1)
        print(listTsi[wildTsi][4])
        print(listTsi[wildTsi][5])
        print(wildLvl)
        curVie2 = int(listTsi[deckTsi[tsiChoosen2][0]][4])+int(listTsi[deckTsi[tsiChoosen2][0]][5])*int(deckTsi[tsiChoosen2][1]-1)
        r_posImage = 0
     
    #print(listTsi[wildTsi][1][1:][:len(listTsi[wildTsi][1])-2].split(",")[0])
    #Definition des noms des persos
    nom1 = listTsi[wildTsi][1]
    nom2 = listTsi[deckTsi[tsiChoosen2][0]][1]

    #Definition vie
    vie1 = str(int(listTsi[wildTsi][4])+int(listTsi[wildTsi][5])*int(wildLvl-1))
    vie2 = str(int(listTsi[deckTsi[tsiChoosen2][0]][4])+int(listTsi[deckTsi[tsiChoosen2][0]][5])*int(deckTsi[tsiChoosen2][1]-1))

    #Definition Lvl
    lvl1 = wildLvl
    lvl2 = deckTsi[tsiChoosen2][1]
    
    #Creation Texte : Noms
    perso1 = myfont.render(nom1, 1, (0,0,0))
    perso2 = myfont.render(nom2, 1, (0,0,0))

    #Creation Texte : Vie
    textVie1 = myfont.render(str(curVie1)+"/"+vie1, 1, (0,0,0))
    textVie2 = myfont.render(str(curVie2)+"/"+vie2, 1, (0,0,0))

    #Creation Texte : Level
    textLvl1 = myfont.render("Lvl "+str(lvl1), 1, (0,0,0))
    textLvl2 = myfont.render("Lvl "+str(lvl2), 1, (0,0,0))
    
    #Affichage Noms
    frame.blit(perso1, (50, 49))
    frame.blit(perso2, (330, 265))

    #Affichage Vies : (30,9) et (310,225)
    frame.blit(textVie1, (30,9))
    frame.blit(textVie2, (310,225))

    #Affichage Lvl : (251,3) et (531,229)
    frame.blit(textLvl1, (251,9))
    frame.blit(textLvl2, (531,225))

    #add((349,17),(math.floor(270/2-rectImagePerso1[2]/2),0)))
    #add((20,96),(math.floor(270/2-rectImagePerso2[2]/2),0)))
    if xImage1>349+math.floor(270/2-rectImagePerso1[2]/2):
        xImage1 -= 20
        xImage2 += 20
     
    #Affichage PixelArt
    frame.blit(imagePerso1, (xImage1,17))
    frame.blit(imagePerso2, (xImage2,96))

    ############
    #### FIN AFF TSI FIGHT
    ############
    #### AFFICHAGE MENU
    ############
    # 606,151 : 303,75
        
    #Afficahge Menu : Compétence, Tsi, Objets, RageQuit
    
    
    ############
    #### AFFICHAGE MENU
    ############

    #Refresh affichage
    pygame.display.flip()
     
    return 7

################################### Programme ##################################

#Affichage Fond et main Perso
frame.blit(roll_fight, position_roll)
frame.blit(fond, (0,0))
frame.blit(fond, position_map[currentMap])
frame.blit(mainBack[sprite], (x,y))
frame.blit(hitbox, (x,y))

#Refresh Frame
pygame.display.flip()

loop = True
while loop:
     #Boucle Infinie

     #Event Control
     for event in pygame.event.get():
          if event.type==QUIT:
               loop=0
               pygame.quit()

          #Vitesse du sprite : 0<vit<1
          vit = 0.5

          if event.type == KEYDOWN:

               #Déplacement perso si le menu est fermé
               if stopMove == False and env == 0:
                    if  event.key == K_UP and not Collision("up"):# and position_map[1]<=-4:
                         position_map[currentMap] = position_map[currentMap].move(0,3)
                         direct = 1
                         sprite = (sprite+vit)%4
                    elif  event.key == K_DOWN and not Collision("down"):# and position_map[1]>-position_map[2]+frameSize[1]:
                         position_map[currentMap] = position_map[currentMap].move(0,-3)
                         direct = 3
                         sprite = (sprite+vit)%4
                    elif  event.key == K_LEFT and not Collision("left"):# and position_map[0]<=-4:
                         position_map[currentMap] = position_map[currentMap].move(3,0)
                         direct = 2
                         sprite = (sprite+vit)%4
                    elif  event.key == K_RIGHT and not Collision("right"):# and position_map[0]>-position_map[3]+frameSize[0]:
                         position_map[currentMap] = position_map[currentMap].move(-3,0)
                         direct = 0
                         sprite = (sprite+vit)%4

               #Utilisation Clavier Interface en Combat
               if env == 2:
                    if  event.key == K_UP:
                         print("Key_up")
                    
               ####Debug Key
               if event.key == K_KP8:
                    position_map[currentMap] = position_map[currentMap].move(0,64)
               elif event.key == K_KP2:
                    position_map[currentMap] = position_map[currentMap].move(0,-64)
               elif event.key == K_KP4:
                    position_map[currentMap] = position_map[currentMap].move(64,0)
               elif event.key == K_KP6:
                    position_map[currentMap] = position_map[currentMap].move(-64,0)

               if event.key == K_p:
                    stopMove = (stopMove+1)%2
                    env = (env+1)%3
                    r_posImage = 1
               ####
               
               #Aff menu
               if event.key == K_KP1 and r_menu:
                    r_menu = False
                    stopMove = (stopMove+1)%2
                    affMenu = (affMenu+1)%2
                    #print(affMenu)
                    pygame.time.delay(100)
          else:
               r_menu = True
               sprite = 0

               
          pygame.time.wait(8)
     ###Fin Event Control

     #Fin Haute herbes
     ProbForFight()
     
     #Calculs

     #....................
     #print(env)
     #print(countForFight)
     
     #Afficahge   
     if env == 0:
          Display()
     elif env == 1:
          DispRoll_Fight()
     elif env == 2:
          Disp_WildFight()
          
     pygame.display.flip()

     pygame.time.delay(25)
     
     #Fin Boucle Infinie


