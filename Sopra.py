import sys
import math
import numpy as np 
import random #pour la dispertion
# Send your busters out into the fog to trap ghosts and bring them home!

busters_per_player = int(input())  # the amount of busters you control
ghost_count = int(input())  # the amount of ghosts on the map
my_team_id = int(input())  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right
radarDone = False # savoir si on a utilisé le radar

HUNTER = 0
ATTRAPEUR = 1
SUPPORT = 2
FANTOME = -1 

print(("Mon id",my_team_id), file=sys.stderr, flush=True)



def barycentreMoi(X,Y): #renvoie le barycentre de notre equipe
    xMoy = sum(X)/len(X) 
    yMoy = sum(Y)/len(Y)
    return [xMoy,yMoy]

def distance(a,b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 )

def distMoy(coordonees,goal):
    M=0 #la moyenne des distances au goal 
    for myBuster in coordonees:
        M += distance(myBuster,goal)
    M / len(coordonees)
    return M

def fantomeLePlusProche(listeFantomes,buster):
    indice = 0
    minDist = 30000 # plus grand que la map
    for k in range len(listeFantomes):
        distance = distance([listeFantomes[k][1],[listeFantomes[k][2]],buster) #distance entre 1 fantome et le buster concerné, pour le moment le hunter
        if(dist<minDist):
            minDist = dist
            indice = k
    return k


# game loop
while True:
    entities = int(input())  # the number of busters and ghosts visible to you
    
    equipeMoi = []
    equipeAdverse  = []
    equipeFantome = []

    coorHunterX  = 8000 
    coorHunterY = 4500
    coorGhostCatcherX  = 8000
    coorGhostCatcherY = 4500
    coorSupportX  =8000
    coorSupportY =4500

    #les actions de chacun
    supDoRadar = False


    for i in range(entities):
        # entity_id: buster id or ghost id
        # y: position of this buster / ghost
        # entity_type: the team id if it is a buster, -1 if it is a ghost.
        # entity_role: -1 for ghosts, 0 for the HUNTER, 1 for the GHOST CATCHER and 2 for the SUPPORT
        # state: For busters: 0=idle, 1=carrying a ghost. For ghosts: remaining stamina points.
        # value: For busters: Ghost id being carried/busted or number of turns left when stunned. For ghosts: number of busters attempting to trap this ghost.
        entity_id, x, y, entity_type, entity_role, state, value = [int(j) for j in input().split()]
        
        if(entity_type==my_team_id):
            equipeMoi.append([entity_id,x,y,entity_type,entity_role,state,value])
        elif(entity_type==(my_team_id+1)%2): #l'autre équipe
            equipeAdverse.append([entity_id,x,y,entity_type,entity_role,state,value])
        else: #les fantomes
            equipeFantome.append([entity_id,x,y,entity_type,entity_role,state,value])


    
    currentCoorHunter = []
    currentCoorAttrapeur = []
    currentCoorSupport = []
    for buster in equipeMoi:
        if(buster[3]==HUNTER):
            currentCoorHunter.append(buster[1])
            currentCoorHunter.append(buster[2])
        if(buster[3]==ATTRAPEUR):
            currentCoorAttrapeur.append(buster[1])
            currentCoorAttrapeur.append(buster[2])
        if(buster[3]==SUPPORT):
            currentCoorSupport.append(buster[1])
            currentCoorSupport.append(buster[2])

    XMoi = [entity[1] for entity in equipeMoi]
    YMoi = [entity[2] for entity in equipeMoi]
    coordonnees = [  [XMoi[k],YMoi[k]] for k in range(len(XMoi))   ] #les coordonnées de mes bros

    numFantomes = len(equipeFantome) #le nombre de fantomes visibles
    barycentre = barycentreMoi(XMoi,YMoi)


    if(numFantomes==0): # Si on ne voit aucun fantome, il faut plus de visibilité 
        
        #print(barycentre, file=sys.stderr, flush=True)
        dist = distMoy(coordonnees,barycentre)
        #print(dist, file=sys.stderr, flush=True)
        if(dist<2200): #S'ils sont trop proches les uns des autres
            #les 3 vont dans des spots aléatoires pour se disperser
            coorHunterX = random.randint(0,16000)
            coorHunterY = random.randint(0,9000)
            coorGhostCatcherX = random.randint(0,16000)
            coorGhostCatcherY = random.randint(0,9000)
            coorSupportX = random.randint(0,16000)
            coorSupportY = random.randint(0,9000)
            coorHunter =[coorHunterX,coorHunterY] #coordonnee du hunter
            coorGhostCatcher = [coorGhostCatcherX,coorGhostCatcherY] #coor du ghost catcher
            coorSupport = [coorSupportX,coorSupportY] #coor du support
        else: #ils sont déjà loin donc il faut employer les grands moyen
            if(not radarDone):
                supDoRadar = True
                radarDone  = True

    else: #si on voit un ou des fantomes
        # le hunter et l'attrapeur vont se rapprocher du fantome le plus proche du hunter
        indiceF = fantomeLePlusProche(equipeFantome,currentCoorHunter)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    #Séparer notre équipe, de l'autre, et des fantomes




    # First the HUNTER : MOVE x y | BUST id
    # Second the GHOST CATCHER: MOVE x y | TRAP id | RELEASE
    # Third the SUPPORT: MOVE x y | STUN id | RADAR
    print("MOVE {} {}".format(coorHunterX,coorHunterY))
    print("MOVE {} {}".format(coorGhostCatcherX,coorGhostCatcherY))
    if(supDoRadar):
        print("RADAR")
        supDoRadar = False
    else:    
        print("MOVE {} {}".format(coorSupportX,coorSupportY))


