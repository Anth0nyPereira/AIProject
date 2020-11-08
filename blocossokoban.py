import time
from strips import *
from mapa import *
from game import Game

# Predicados
class Floor(Predicate):
    def _init_(self, pos):
        self.args = [pos]

class Goal(Predicate):
    def _init_(self, pos):
        self.args = [pos]

class Man(Predicate):
    def _init_(self, pos):
        self.args = [pos]

class Man_On_Goal(Predicate):
    def _init_(self, pos):
        self.args = [pos]

class Box(Predicate):
    def _init_(self, pos):
        self.args = [pos]

class Box_On_Goal(Predicate):
    def _init_(self, pos):
        self.args = [pos]

class Wall(Predicate):
    def _init_(self, pos):
        self.args = [pos]


w = "w"
a = "a"
s = "s"
d = "d"

g = Game()
game_state = g.state
print(game_state)
game_level = game_state["level"]
game_map = Map(f"levels/{level}.xsb")
print(game_map) 

class MoveRight(Operator):
    # garantir q a posição atual é o keeper e a posição a seguir é floor
    initialPos = game_map.keeper
    finalPos = (initialPos[0]+1, initialPos[1])
    pc = [Floor(finalPos) or Goal(finalPos)] # saber se a pos final é floor
    neg = [Floor(finalPos) or Goal(finalPos), Man(initialPos)]
    pos = [Floor(initialPos) or Goal(initialPos), Man(finalPos)]



class MoveLeft(Operator):
    # garantir q a posição atual é o keeper e a posição a seguir é floor
    initialPos = game_map.keeper
    finalPos = (initialPos[0]-1, initialPos[1])
    pc = [Floor(finalPos) or Goal(finalPos)] # saber se a pos final é floor
    neg = [Floor(finalPos) or Goal(finalPos), Man(initialPos)]
    pos = [Floor(initialPos) or Goal(initialPos), Man(finalPos)]


class MoveUp(Operator):
    # garantir q a posição atual é o keeper e a posição a seguir é floor
    initialPos = game_map.keeper
    finalPos = (initialPos[0], initialPos[1]-1)
    pc = [Floor(finalPos) or Goal(finalPos)] # saber se a pos final é floor
    neg = [Floor(finalPos) or Goal(finalPos), Man(initialPos)]
    pos = [Floor(initialPos) or Goal(initialPos), Man(finalPos)]

class MoveDown(Operator):
    # garantir q a posição atual é o keeper e a posição a seguir é floor
    initialPos = game_map.keeper
    finalPos = (initialPos[0], initialPos[1]+1)
    pc = [Floor(finalPos) or Goal(finalPos)] # saber se a pos final é floor
    neg = [Floor(finalPos) or Goal(finalPos), Man(initialPos)]
    pos = [Floor(initialPos) or Goal(initialPos), Man(finalPos)]


class PushRight(Operator):
    initialPos = game_map.keeper
    finalPos = (initialPos[0]+1, initialPos[1])
    pc = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0]+1, finalPos[1]) or Goal(finalPos[0]+1, finalPos[1])] 
    neg = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0]+1, finalPos[1]) or Goal(finalPos[0]+1, finalPos[1]), Man(initialPos)]
    pos = [Box(finalPos[0]+1, finalPos[1]) or Box_On_Goal(finalPos[0]+1, finalPos[1]), Man(finalPos)]


class PushLeft(Operator):
    initialPos = game_map.keeper
    finalPos = (initialPos[0]-1, initialPos[1])
    pc = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0]-1, finalPos[1]) or Goal(finalPos[0]-1, finalPos[1])] 
    neg = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0]-1, finalPos[1]) or Goal(finalPos[0]-1, finalPos[1]), Man(initialPos)]
    pos = [Box(finalPos[0]-1, finalPos[1]) or Box_On_Goal(finalPos[0]-1, finalPos[1]), Man(finalPos)]


class PushUp(Operator):
    initialPos = game_map.keeper
    finalPos = (initialPos[0], initialPos[1]-1)
    pc = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0], finalPos[1]-1) or Goal(finalPos[0], finalPos[1]-1)] 
    neg = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0], finalPos[1]-1) or Goal(finalPos[0], finalPos[1]-1), Man(initialPos)]
    pos = [Box(finalPos[0], finalPos[1]-1) or Box_On_Goal(finalPos[0], finalPos[1]-1), Man(finalPos)]


class PushDown(Operator):
    initialPos = game_map.keeper
    finalPos = (initialPos[0], initialPos[1]+1)
    pc = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0], finalPos[1]+1) or Goal(finalPos[0], finalPos[1]+1)] 
    neg = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0], finalPos[1]+1) or Goal(finalPos[0], finalPos[1]+1), Man(initialPos)]
    pos = [Box(finalPos[0], finalPos[1]+1) or Box_On_Goal(finalPos[0], finalPos[1]+1), Man(finalPos)]


def getInitialState():
    map_list = game_map 
    initial_state = []
    for row in range(len(map_list)):
        for col in range(len(row)):
            if map_list[row][col] == 0:
                initial_state += Floor((row,col))
            if map_list[row][col] == 1:
                initial_state += Goal((row,col))
            if map_list[row][col] == 2:
                initial_state += Man((row,col))
            if map_list[row][col] == 3:
                initial_state += Man_On_Goal((row,col))
            if map_list[row][col] == 4:
                initial_state += Box((row,col))
            if map_list[row][col] == 5:
                initial_state += Box_On_Goal((row,col))
            if map_list[row][col] == 8:
                initial_state += Wall((row,col))
    return initial_state

initial_state = getInitialState()

goal_state = [Box_On_Goal(pos) for pos in game_map.empty_goals]

sokobandomain = STRIPS()

print(initial_state)
print('Actions:',sokobandomain.actions(initial_state))
print(goal_state)

inittime = time.time()

p = SearchProblem(sokobandomain,initial_state,goal_state)
t = SearchTree(p, 'depth')
t.search()

print(t.plan)
print('time=',time.time()-inittime)
print(len(t.open_nodes),' nodes')