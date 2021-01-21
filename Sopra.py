import sys
import math
import numpy as np 
# Send your busters out into the fog to trap ghosts and bring them home!

busters_per_player = int(input())  # the amount of busters you control
ghost_count = int(input())  # the amount of ghosts on the map
my_team_id = int(input())  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right

print(("Mon id",my_team_id), file=sys.stderr, flush=True)

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






    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(np.array(equipeFantome), file=sys.stderr, flush=True)

    #Séparer notre équipe, de l'autre, et des fantomes




    # First the HUNTER : MOVE x y | BUST id
    # Second the GHOST CATCHER: MOVE x y | TRAP id | RELEASE
    # Third the SUPPORT: MOVE x y | STUN id | RADAR
    print("MOVE 8000 4500")
    print("MOVE 8000 4500")
    print("MOVE 8000 4500")
