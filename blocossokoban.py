import time
from strips import *
from mapa import *


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

class MoveRight(Operator):
    # garantir q a posição atual é o keeper e a posição a seguir é floor
    initialPos = mapa.keeper
    finalPos = (initialPos[0]+1, initialPos[1])
    pc = [Floor(finalPos) or Goal(finalPos)] # saber se a pos final é floor
    neg = [Floor(finalPos) or Goal(finalPos), Man(initialPos)]
    pos = [Floor(initialPos) or Goal(initialPos), Man(finalPos)]



class MoveLeft(Operator):
    # garantir q a posição atual é o keeper e a posição a seguir é floor
    initialPos = mapa.keeper
    finalPos = (initialPos[0]-1, initialPos[1])
    pc = [Floor(finalPos) or Goal(finalPos)] # saber se a pos final é floor
    neg = [Floor(finalPos) or Goal(finalPos), Man(initialPos)]
    pos = [Floor(initialPos) or Goal(initialPos), Man(finalPos)]


class MoveUp(Operator):
    # garantir q a posição atual é o keeper e a posição a seguir é floor
    initialPos = mapa.keeper
    finalPos = (initialPos[0], initialPos[1]-1)
    pc = [Floor(finalPos) or Goal(finalPos)] # saber se a pos final é floor
    neg = [Floor(finalPos) or Goal(finalPos), Man(initialPos)]
    pos = [Floor(initialPos) or Goal(initialPos), Man(finalPos)]

class MoveDown(Operator):
    # garantir q a posição atual é o keeper e a posição a seguir é floor
    initialPos = mapa.keeper
    finalPos = (initialPos[0], initialPos[1]+1)
    pc = [Floor(finalPos) or Goal(finalPos)] # saber se a pos final é floor
    neg = [Floor(finalPos) or Goal(finalPos), Man(initialPos)]
    pos = [Floor(initialPos) or Goal(initialPos), Man(finalPos)]


class PushRight(Operator):
    initialPos = mapa.keeper
    finalPos = (initialPos[0]+1, initialPos[1])
    pc = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0]+1, finalPos[1]) or Goal(finalPos[0]+1, finalPos[1])] 
    neg = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0]+1, finalPos[1]) or Goal(finalPos[0]+1, finalPos[1]), Man(initialPos)]
    pos = [Box(finalPos[0]+1, finalPos[1]) or Box_On_Goal(finalPos[0]+1, finalPos[1]), Man(finalPos)]


class PushLeft(Operator):
    initialPos = mapa.keeper
    finalPos = (initialPos[0]-1, initialPos[1])
    pc = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0]-1, finalPos[1]) or Goal(finalPos[0]-1, finalPos[1])] 
    neg = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0]-1, finalPos[1]) or Goal(finalPos[0]-1, finalPos[1]), Man(initialPos)]
    pos = [Box(finalPos[0]-1, finalPos[1]) or Box_On_Goal(finalPos[0]-1, finalPos[1]), Man(finalPos)]


class PushUp(Operator):
    initialPos = mapa.keeper
    finalPos = (initialPos[0], initialPos[1]-1)
    pc = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0], finalPos[1]-1) or Goal(finalPos[0], finalPos[1]-1)] 
    neg = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0], finalPos[1]-1) or Goal(finalPos[0], finalPos[1]-1), Man(initialPos)]
    pos = [Box(finalPos[0], finalPos[1]-1) or Box_On_Goal(finalPos[0], finalPos[1]-1), Man(finalPos)]


class PushDown(Operator):
    initialPos = mapa.keeper
    finalPos = (initialPos[0], initialPos[1]+1)
    pc = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0], finalPos[1]+1) or Goal(finalPos[0], finalPos[1]+1)] 
    neg = [Box(finalPos) or Box_On_Goal(finalPos), Floor(finalPos[0], finalPos[1]+1) or Goal(finalPos[0], finalPos[1]+1), Man(initialPos)]
    pos = [Box(finalPos[0], finalPos[1]+1) or Box_On_Goal(finalPos[0], finalPos[1]+1), Man(finalPos)]


def getInitialState():
    










