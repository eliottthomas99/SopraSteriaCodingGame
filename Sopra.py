import sys
import math
import numpy as np 
import random #pour la dispertion
# Send your busters out into the fog to trap ghosts and bring them home!

busters_per_player = int(input())  # the amount of busters you control
ghost_count = int(input())  # the amount of ghosts on the map
my_team_id = int(input())  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right
radarDone = False # savoir si on a utilisé le radar

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


# game loop
while True:
    entities = int(input())  # the number of busters and ghosts visible to you
    
    equipeMoi = []
    equipeAdverse  = []
    equipeFantome = []



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


    

    XMoi = [entity[1] for entity in equipeMoi]
    YMoi = [entity[2] for entity in equipeMoi]
    coordonnees = [  [XMoi[k],YMoi[k]] for k in range(len(XMoi))   ] #les coordonnées de mes bros

    numFantomes = len(equipeFantome)
    if(numFantomes==0): # Si on ne voit aucun fantome, il faut plus de visibilité 
        barycentre = barycentreMoi(XMoi,YMoi)
        #print(barycentre, file=sys.stderr, flush=True)
        dist = distMoy(coordonnees,barycentre)
        #print(dist, file=sys.stderr, flush=True)
        if(dist<2200): #S'ils sont trop proches les uns des autres
            #les 3 vont dans des spots aléatoires pour se disperser


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    #Séparer notre équipe, de l'autre, et des fantomes




    # First the HUNTER : MOVE x y | BUST id
    # Second the GHOST CATCHER: MOVE x y | TRAP id | RELEASE
    # Third the SUPPORT: MOVE x y | STUN id | RADAR
    print("MOVE 8000 4500")
    print("MOVE 8000 4500")
    print("MOVE 8000 4500")

