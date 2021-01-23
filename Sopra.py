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
OTHERTEAM = (my_team_id+1)%2 #l'identifiant de l'autre équipe

coorBase = [0,0]
coorOther  =[16000,9000]

if(my_team_id!=0): #Si on est dans l'équipe 1
    coorBase[0]=16000
    coorBase[1]=9000
    coorOther[0] = 0
    coorOther[1] = 0


#print(("Mon id",my_team_id), file=sys.stderr, flush=True)


def catching(equipe):
    for buster in equipe:
        if(buster[5]==1): 
            return True
    return False

def getSymetric(center,extern):
    xsym = 2*center[0]-extern[0]
    ysym = 2*center[1]-extern[1]
    return [xsym,ysym]


def barycentreMoi(X,Y): #renvoie le barycentre de notre equipe
    xMoy = sum(X)/len(X) 
    yMoy = sum(Y)/len(Y)
    return [xMoy,yMoy]

def distance(a,b):
    return np.sqrt(  (a[0]-b[0])**2 + (a[1]-b[1])**2 )

def distMoy(coordonees,goal):
    M=0 #la moyenne des distances au goal 
    for myBuster in coordonees:
        M += distance(myBuster,goal)
    M / len(coordonees)
    return M

def fantomeLePlusProche(listeFantomes,LEbuster):
    
    indice = 0
    minDist = 30000 # plus grand que la map
    n=len(listeFantomes)
    for k in range(n):
        #indice+=1
        LK = listeFantomes[k]

        #print(("LK",LK), file=sys.stderr, flush=True)
        #print(("LEbuster",LEbuster), file=sys.stderr, flush=True)

        dist = distance([   LK[1] , LK[2] ],LEbuster) #distance entre 1 fantome et le buster concerné, pour le moment le hunter
        if(dist<minDist):
           minDist = dist
           indice = k
    return indice





# game loop
while True:
    entities = int(input())  # the number of busters and ghosts visible to you
    
    equipeMoi = []
    equipeAdverse  = []
    equipeFantome = []


    """
    coorHunterX  = 8000 
    coorHunterY = 4500
    coorGhostCatcherX  = 8000
    coorGhostCatcherY = 4500
    coorSupportX  =8000
    coorSupportY =4500
    """

    coorHunterX = random.randint(0,16000)
    coorHunterY = random.randint(0,9000)
    coorGhostCatcherX = random.randint(0,16000)
    coorGhostCatcherY = random.randint(0,9000)
    coorSupportX = random.randint(0,16000)
    coorSupportY = random.randint(0,9000)


    coorFantomeProche = [0,0]
    idFantome  = 0
    idFantomeToCatch = 0 #il faut bien initialiser à qqch
    idFantomeToStun =0 #idem
    #les actions de chacun
    huntDoBust = False
    supDoRadar = False
    supportDoStun = False
    AttrapeurDoTrap = False
    AttrapeurDoRelease  = False

    #les etats
    #catching = False #on est en train d'attraper quelqu'un ?

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
        elif(entity_type==OTHERTEAM): #l'autre équipe
            equipeAdverse.append([entity_id,x,y,entity_type,entity_role,state,value])
        else: #les fantomes
            equipeFantome.append([entity_id,x,y,entity_type,entity_role,state,value])


    
    currentCoorHunter = []
    currentCoorAttrapeur = []
    currentCoorSupport = []
    for buster in equipeMoi:
        if(buster[4]==HUNTER):
            currentCoorHunter.append(buster[1])
            currentCoorHunter.append(buster[2])
        if(buster[4]==ATTRAPEUR):
            currentCoorAttrapeur.append(buster[1])
            currentCoorAttrapeur.append(buster[2])
            #print(("Attributioncoor",currentCoorAttrapeur), file=sys.stderr, flush=True)

        if(buster[4]==SUPPORT):
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
    
        #sinon on attaque
    else: #si on voit un ou des fantomes

            ##Comportement de HUNTER
            indiceF = fantomeLePlusProche(equipeFantome,currentCoorHunter)
            coorFantomeProche = [equipeFantome[indiceF][1],equipeFantome[indiceF][2] ]
            idFantome  = equipeFantome[indiceF][0] #l'ID du fantome le plus proche pour savoir sur qui tirer
            #si la distance du plus proche fantome est trop élevée
            if(distance(coorFantomeProche,currentCoorHunter)>1760):
                #on se rapproche du fantome
                coorHunterX = coorFantomeProche[0]
                coorHunterY = coorFantomeProche[1]
            elif(distance(coorFantomeProche,currentCoorHunter)<900):#si la distance est trop faible
                #on s'écarte
                symet = getSymetric(currentCoorHunter,coorFantomeProche)
                coorHunterX = symet[0]
                coorHunterY = symet[1]
            else: #on tape
                huntDoBust = True
            

            ##Comportement de ATTRAPEUR
            # on commence par voir si on porte déjà un fantome

            if(catching(equipeMoi)): #alors on se dirige vers la base
                if( distance(currentCoorAttrapeur,coorBase) < 1600  ): #si on est suffisamment proche, on relache
                    AttrapeurDoRelease  = True
                else:
                    coorGhostCatcherX = coorBase[0]
                    coorGhostCatcherY = coorBase[1]
            
            else:
                
                fantomesToCatch = []
                for fantome in equipeFantome:
                    if (fantome[5]==0): #le fantome n'a plus d'endurance
                        fantomesToCatch.append(fantome)

                if( len(fantomesToCatch)!=0 ): #  s'il y a des fantomes visibles et attrapables (0HP)
                    # ensuite on cherche le plus proche
                    indiceFToCatch = fantomeLePlusProche(fantomesToCatch,currentCoorAttrapeur)
                    coorFantomeProcheToCatch = [fantomesToCatch[indiceFToCatch][1],fantomesToCatch[indiceFToCatch][2] ]
                    idFantomeToCatch  = fantomesToCatch[indiceFToCatch][0] #l'ID du fantome à catch

                    # Si l'attrapeur est bien placé
                    
                    if(distance(coorFantomeProcheToCatch,currentCoorAttrapeur)>1760): #on est trop loin
                        #on se rapproche du fantome
                        coorGhostCatcherX = coorFantomeProcheToCatch[0]
                        coorGhostCatcherY = coorFantomeProcheToCatch[1]
                    elif(distance(coorFantomeProcheToCatch,currentCoorAttrapeur)<900):#si la distance est trop faible
                        #on s'écarte
                        symet = getSymetric(currentCoorAttrapeur,coorFantomeProcheToCatch)
                        coorGhostCatcherX = symet[0]
                        coorGhostCatcherY = symet[1]
                    else: #on capture
                        AttrapeurDoTrap = True

            ##Comportement de SUPPORT
            
            #y a t il des ennemis à stun ?
            #ennemisToStun = []
                for enemi in equipeAdverse:
                    if(enemi[4]==1): #par default le support marque l'attrapeur adverse
                        coorSupportX = enemi[1]
                        coorSupportY = enemi[2]

                    if (enemi[5]==1 or enemi[5]==3): #lennemi porte un fantome ou tente de le trap , feu !!
                        #il faut voir s'il est suffisamment proche
                        if(  distance(currentCoorSupport, [enemi[1], enemi[2]] )   ): #on peut effectivement tirer
                            idFantomeToStun  = enemi[0] #l'ID de l'ennemi à stun
                            supportDoStun = True
                        else: #on doit se rapprocher
                            #potentielle amélioration pour plus tard. On pourra lui couper la route car on sait qu'il va à sa base
                            if(enemi[5]==1): #il transporte un fantome
                                coorSupportX = coorOther[0]
                                coorSupportY = coorOther[1]
                            elif(enemi[5]==3): #il tente de trap un fantome
                                coorSupportX = enemi[1]
                                coorSupportY = enemi[2]
                            
                        

            
            



        # le hunter et l'attrapeur vont se rapprocher du fantome le plus proche du hunter

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    #Séparer notre équipe, de l'autre, et des fantomes




    # First the HUNTER : MOVE x y | BUST id
    # Second the GHOST CATCHER: MOVE x y | TRAP id | RELEASE
    # Third the SUPPORT: MOVE x y | STUN id | RADAR

    """
    print("MOVE 8000 4500")
    print("MOVE 8000 4500")
    print("MOVE 8000 4500")
    """

    if(huntDoBust):
        #print("MOVE 8000 4500")
        print("BUST {}".format(idFantome))
        #print("je suis la", file=sys.stderr, flush=True)
        huntDoBust = False
    else:
        print("MOVE {} {}".format(coorHunterX,coorHunterY))
        #print("MOVE {} {}".format(8000,4500))



    if(AttrapeurDoTrap):
        print("TRAP {}".format(idFantomeToCatch))
    elif(AttrapeurDoRelease):
        print("RELEASE")
    else:
        print("MOVE {} {}".format(coorGhostCatcherX,coorGhostCatcherY))




    if(supDoRadar):
        print("RADAR")
        supDoRadar = False
    elif(supportDoStun):
        print("STUN {}".format(idFantomeToStun))
    else:    
        print("MOVE {} {}".format(coorSupportX,coorSupportY))


