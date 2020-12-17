from audioop import add
from functools import reduce
import copy
import asyncio
import math
import bisect
#-------------------------------------------------------MYMAP------------------------------------------------------------
from game import logger


class MyMap:
    """Representation of a Map."""

    def __init__(self, mapa):
        self.mapa = mapa
        self._keeper = None

        self.hor_tiles, self.ver_tiles = (
            max([len(line) for line in self.mapa]),
            len(self.mapa),
        )  # X, Y

    @property
    def completed(self):
        """Map is completed when there are no empty_goals!"""
        return self.empty_goals == []

    @property
    def on_goal(self):
        """Number of boxes on goal.

           Counts per line and counts all lines using reduce
        """
        return reduce(
            add,
            [
                reduce(lambda a, b: a + int(b == 5), l, 0)
                for l in self.mapa
            ],
        )

    def filter_tiles(self, list_to_filter):
        """Util to retrieve list of coordinates of given tiles."""
        return [
            (x, y)
            for y, l in enumerate(self.mapa)
            for x, tile in enumerate(l)
            if tile in list_to_filter
        ]

    @property
    def keeper(self):
        """Coordinates of the Keeper."""
        if self._keeper is None:
            self._keeper = self.filter_tiles([2,3])[0]

        return self._keeper

    @property
    def boxes(self):
        """List of coordinates of the boxes."""
        return self.filter_tiles([4,5])

    @property
    def empty_goals(self):
        """List of coordinates of the empty goals locations."""
        return self.filter_tiles([1,3])

    def get_tile(self, pos):
        """Retrieve tile at position pos."""
        x, y = pos
        return self.mapa[y][x]

    def set_tile(self, pos, tile):
        """Set the tile at position pos to tile."""
        x, y = pos
        self.mapa[y][x] = (
            tile & 0b1110 | self.mapa[y][x]
        )  # the 0b1110 mask avoid carring ON_GOAL to new tiles

        if (
            tile & 2 == 2
        ):  # hack to avoid continuous searching for keeper
            self._keeper = pos

    def clear_tile(self, pos):
        """Remove mobile entity from pos."""
        x, y = pos
        self.mapa[y][x] = self.mapa[y][x] & 0b1  # lesser bit carries ON_GOAL

    def is_blocked(self, pos):
        """Determine if mobile entity can be placed at pos."""
        x, y = pos
        if x not in range(self.hor_tiles) or y not in range(self.ver_tiles):
            logger.error("Position out of map")
            return True
        if self.mapa[y][x] == 8:
            logger.debug("Position is a wall")
            return True
        return False
#-----------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------MYDOMAIN----------------------------------------------------------
class MyDomain:
    def __init__(self, initial):
        self.initial = initial

    def cornerCheck(self,state_map, pos): # pos will be the final position of a box
        x,y = pos

        em_baixo = state_map[y+1][x]
        a_direita = state_map[y][x+1]

        if em_baixo == 8 and a_direita == 8: # down and right are walls
            return True
        else:
            a_esquerda = state_map[y][x-1]
        if em_baixo == 8 and a_esquerda == 8: # down and left are walls
            return True
        else:
            em_cima =  state_map[y-1][x]
        if em_cima == 8 and a_direita == 8: # up and right are walls
            return True
        if em_cima == 8 and a_esquerda == 8: # up and left are walls
            return True
        return False

    def BoxesNextToWall(self, state_map, pos_init, pos): # pos will be the final position of a box
        x, y = pos

        mapa = state_map.mapa

        state = 4 if mapa[y][x] == 4 else 5

        state_map.clear_tile(pos_init)

        a_direita = mapa[y][x+1]
        em_baixo = mapa[y+1][x]
        direita_baixo = mapa[y+1][x+1]
        
        if a_direita in [4,5] and (em_baixo == 8 and direita_baixo == 8):
            print("ha uma caixa a direita e wall em baixo" + " " + str(pos)) 
            state_map.set_tile(pos_init, state)
            return True
        else:
            a_esquerda = mapa[y][x-1]
            esquerda_baixo = mapa[y+1][x-1]
        if a_esquerda in [4,5] and (em_baixo == 8 and esquerda_baixo == 8):
            print("ha uma caixa a esquerda e wall em baixo" + " " + str(pos)) 
            state_map.set_tile(pos_init, state)
            return True
        else:
            em_cima =  mapa[y-1][x]
            direita_cima = mapa[y-1][x+1]
        if a_direita in [4,5] and (em_cima == 8 and direita_cima == 8):
            print("ha uma caixa a direita e wall em cima" + " " + str(pos)) 
            state_map.set_tile(pos_init, state)
            return True
        else:
            esquerda_cima = mapa[y-1][x-1]
        if a_esquerda in [4,5] and (em_cima == 8 and esquerda_cima == 8):
            print("ha uma caixa a esquerda e wall em cima" + " " + str(pos)) 
            state_map.set_tile(pos_init, state)
            return True
        if em_baixo in [4,5] and (a_esquerda == 8 and esquerda_baixo == 8):
            print("ha uma caixa em baixo e wall à esquerda" + " " + str(pos))
            state_map.set_tile(pos_init, state)
            return True
        if em_cima in [4,5] and (a_esquerda == 8 and esquerda_cima == 8):
            print("ha uma caixa em cima e wall à esquerda" + " " + str(pos))
            state_map.set_tile(pos_init, state)
            return True
        if em_baixo in [4,5] and (a_direita == 8 and direita_baixo == 8):
            print("ha uma caixa em baixo e wall à direita" + " " + str(pos))
            state_map.set_tile(pos_init, state)
            return True
        if em_cima in [4,5] and (a_direita == 8 and direita_cima == 8):
            print("ha uma caixa em cima e wall à direita" + " " + str(pos))
            state_map.set_tile(pos_init, state)
            return True
        state_map.set_tile(pos_init, state)
        return False

    def BoxNextWallNotGoal(self, state_map, pos_init, pos):
        # this method will check if a given position of a box (after the push) will stop or not to move in a specific orientation:
        # if a goal exists and the box is near a wall, check if the box can achieve that goal
        x, y = pos

        mapa = state_map.mapa

        state = 4 if mapa[y][x] == 4 else 5

        state_map.clear_tile(pos_init)

        if state_map.mapa[y][x+1] == 8: # right-wall
            lastWall = y
            firstWall = y
            for line in range(y, len(state_map.mapa)):  #from our line to the end, check if there's a hole in the right wall below our position
                if state_map.mapa[line][x+1] == 8:
                    lastWall = line
                    our_col = state_map.mapa[line][x]
                    if our_col == 1:    #unless we find a goal in the way
                        state_map.set_tile(pos_init, state)
                        return False
                    if our_col == 8:        # now let's check our way up
                        for line in range(y, -1, -1):       #from our line to the top, check if there's a hole in the right wall before our position
                            if state_map.mapa[line][x+1] == 8: 
                                firstWall = line
                                our_col = state_map.mapa[line][x]
                                if our_col == 1:
                                    state_map.set_tile(pos_init, state)
                                    return False 
                                if our_col == 8:
                                    state_map.set_tile(pos_init, state)
                                    print("right-wall " + str(pos))
                                    print(rightWall, leftWall)
                                    print("blocked by " + str((col,y)))
                                    return True
                                else:                           #when we find a hole, we know in which line the wall starts (firstwall)
                                    break
                                
                else:                                   #when we find a hole, we know in which line the wall ends (lastwall)
                    break
                        
        
        if state_map.mapa[y][x-1] == 8: # left-wall
            lastWall = y
            firstWall = y
            for line in range(y, len(state_map.mapa)):  #from our line to the end, check if there's a hole in the left wall below our position
                if state_map.mapa[line][x-1] == 8:
                    lastWall = line
                    our_col = state_map.mapa[line][x]
                    if our_col == 1:
                        state_map.set_tile(pos_init, state)
                        return False 
                    if our_col == 8:        # now let's check our way up
                        for line in range(y, -1, -1):       #from our line to the top, check if there's a hole in the right wall before our position
                            if state_map.mapa[line][x-1] == 8: 
                                firstWall = line
                                our_col = state_map.mapa[line][x]
                                if our_col == 1:
                                    state_map.set_tile(pos_init, state)
                                    return False
                                if our_col == 8:
                                    state_map.set_tile(pos_init, state)
                                    print("left-wall " + str(pos))
                                    print(rightWall, leftWall)
                                    print("blocked by " + str((col,y)))
                                    return True
                                else:                           #when we find a hole, we know in which line the wall starts (firstwall)
                                    break
                else:                                   #when we find a hole, we know in which line the wall ends (lastwall)
                    break
                        

        if state_map.mapa[y+1][x] == 8: # down-wall
            rightWall = x
            leftWall = x
            for col in range(x, state_map.hor_tiles):  #from our column to the end, check if there's a hole in the down-wall on the right of our position
                if state_map.mapa[y+1][col] == 8:
                    rightWall = col
                    our_col = state_map.mapa[y][col]
                    if our_col == 1:
                        state_map.set_tile(pos_init, state)
                        return False
                    if our_col == 8:        # now let's check on our left
                        for col in range(x, -1, -1):       #from our column to the left, check if there's a hole in the down-wall on the left of our position
                            if state_map.mapa[y+1][col] == 8: 
                                leftWall = col
                                our_col = state_map.mapa[y][col]
                                if our_col == 1:
                                    state_map.set_tile(pos_init, state)
                                    return False 
                                if our_col == 8:
                                    state_map.set_tile(pos_init, state)
                                    print("down-wall " + str(pos))
                                    print(rightWall, leftWall)
                                    print("blocked by " + str((col,y)))
                                    return True
                            else:                           #when we find a hole, we know in which column the wall starts (firstwall)
                                break
                        

                else:                                   #when we find a hole, we know in which column the wall ends (rightWall)
                    break
            
            
        if state_map.mapa[y-1][x] == 8: # up-wall
            rightWall = x
            leftWall = x
            for col in range(x, state_map.hor_tiles):  #from our column to the end, check if there's a hole in the up-wall on the right of our position
                if state_map.mapa[y-1][col] == 8:
                    rightWall = col
                    our_col = state_map.mapa[y][col]
                    if our_col == 1:
                        state_map.set_tile(pos_init, state)
                        return False 
                    if our_col == 8:        # now let's check on our left
                        for col in range(x, -1, -1):       #from our column to the left, check if there's a hole in the up-wall on the left of our position
                            if state_map.mapa[y-1][col] == 8: 
                                leftWall = col
                                our_col = state_map.mapa[y][col]
                                if our_col == 1:
                                    state_map.set_tile(pos_init, state)
                                    return False 
                                if our_col == 8:
                                    state_map.set_tile(pos_init, state)
                                    print("up-wall " + str(pos))
                                    print(rightWall, leftWall)
                                    print("blocked by " + str((col,y)))
                                    return True
                            else:                           #when we find a hole, we know in which column the wall starts (firstwall)
                                break

                else:                                   #when we find a hole, we know in which column the wall ends (rightWall)
                    break
        state_map.set_tile(pos_init, state)
        return False

    def deadlocks(self, state_map, pos_init, pos):
        deadlock = self.cornerCheck(state_map.mapa, pos)
        if not deadlock:
            deadlock = self.BoxesNextToWall(state_map, pos_init, pos)
        if not deadlock:
            deadlock = self.BoxNextWallNotGoal(state_map, pos_init, pos)
        return deadlock

    def actions(self, state_map): # valid actions for a given state
        actList = []

        keeper_x, keeper_y = state_map.keeper

        # for each direction, if the next tile is "empty", the action is valid
        # if the next tile has a box, then the action is only valid if the other next tile is "empty" and not a corner
        # TODO: add cornercheck and blockedcheck
        if state_map.mapa[keeper_y][keeper_x + 1] == 0 or state_map.mapa[keeper_y][keeper_x + 1] == 1: # next position is a floor or goal - move
            actList.append('d')
        elif state_map.mapa[keeper_y][keeper_x + 1] == 4 or state_map.mapa[keeper_y][keeper_x + 1] == 5: # next position is a box or box on goal
            if (state_map.mapa[keeper_y][keeper_x + 2] == 0 and not self.deadlocks(state_map, (keeper_x + 1, keeper_y), (keeper_x + 2, keeper_y))) or state_map.mapa[keeper_y][keeper_x + 2] == 1:
                actList.append('d') 
            
        if state_map.mapa[keeper_y][keeper_x - 1] == 0 or state_map.mapa[keeper_y][keeper_x - 1] == 1:
            actList.append('a')
        elif state_map.mapa[keeper_y][keeper_x - 1] == 4 or state_map.mapa[keeper_y][keeper_x - 1] == 5:
            if (state_map.mapa[keeper_y][keeper_x - 2] == 0 and not self.deadlocks(state_map, (keeper_x - 1, keeper_y), (keeper_x - 2, keeper_y))) or state_map.mapa[keeper_y][keeper_x - 2] == 1:
                actList.append('a')
            
        
        if state_map.mapa[keeper_y + 1][keeper_x] == 0 or state_map.mapa[keeper_y + 1][keeper_x] == 1:
            actList.append('s')
        elif state_map.mapa[keeper_y + 1][keeper_x] == 4 or state_map.mapa[keeper_y + 1][keeper_x] == 5:
            if (state_map.mapa[keeper_y + 2][keeper_x] == 0 and not self.deadlocks(state_map, (keeper_x, keeper_y + 1), (keeper_x, keeper_y + 2))) or state_map.mapa[keeper_y + 2][keeper_x] == 1:
                actList.append('s')
            

        if state_map.mapa[keeper_y - 1][keeper_x] == 0 or state_map.mapa[keeper_y - 1][keeper_x] == 1:
            actList.append('w')
        elif state_map.mapa[keeper_y - 1][keeper_x] == 4 or state_map.mapa[keeper_y - 1][keeper_x] == 5:
            if (state_map.mapa[keeper_y - 2][keeper_x] == 0 and not self.deadlocks(state_map, (keeper_x, keeper_y - 1),(keeper_x, keeper_y - 2))) or state_map.mapa[keeper_y - 2][keeper_x] == 1:
                actList.append('w')
            
        
        return actList 
    
    def result(self,state_map,action): # result of an action in a given state (aka next state given an action)
        new_map = MyMap(copy.deepcopy(state_map.mapa))
        x, y = new_map.keeper

        if action == 'd':
            if new_map.mapa[y][x+1] == 4 or new_map.mapa[y][x+1] == 5:
                new_map.clear_tile((x+1, y))
                new_map.set_tile((x+2, y), 4)

            new_map.clear_tile((x,y))
            new_map.set_tile((x+1, y), 2)


        if action == 'a':
            if new_map.mapa[y][x-1] in [4,5]:
                new_map.clear_tile((x-1, y))
                if new_map.mapa[y][x-2] == 0:
                    new_map.set_tile((x-2, y), 4)
                elif new_map.mapa[y][x-2] == 1:
                    new_map.set_tile((x - 2, y), 5)

            new_map.clear_tile((x,y))
            new_map.set_tile((x-1, y), 2)
        
        if action == 's':
            if new_map.mapa[y + 1][x] in [4,5]:
                new_map.clear_tile((x, y + 1))
                if new_map.mapa[y + 2][x] == 0:
                    new_map.set_tile((x, y + 2), 4)
                elif new_map.mapa[y+2][x] == 1:
                    new_map.set_tile((x, y + 2), 5)


            new_map.clear_tile((x,y))
            new_map.set_tile((x, y+1), 2)

        if action == 'w':
            if new_map.mapa[y-1][x] in [4,5]:
                new_map.clear_tile((x, y-1))
                if new_map.mapa[y-2][x] == 0:
                    new_map.set_tile((x, y-2), 4)
                elif new_map.mapa[y-2][x] == 1:
                    new_map.set_tile((x, y - 2), 5)
                
            new_map.clear_tile((x,y))
            new_map.set_tile((x, y-1), 2)

        return new_map

    def satisfies(self, state_map): # test if the given "goal" is satisfied in "state"
        return state_map.empty_goals == []

    def heuristic(self, state_map):
        x,y = state_map.keeper
        boxes = state_map.boxes
        min_dist = 1000
        for box in boxes:
            bx, by = box
            dist = abs(x - bx) + abs(y-by) + len(state_map.empty_goals)
            min_dist = dist if dist < min_dist else min_dist

        return min_dist
    

#------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------MYPROBLEM------------------------------------------------------------
class MyProblem:
    def __init__(self, domain):
        self.domain = domain
        self.initial = domain.initial
    def goal_test(self, state): # tests if we found our goal state using map.empty_goals == []
        return self.domain.satisfies(state)

#------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------MYNODE--------------------------------------------------------------

# Nos de uma arvore de pesquisa
class MyNode:
    def __init__(self,state_map,parent,depth, heuristic, action): 
        self.state_map = state_map
        self.parent = parent
        self.depth = depth
        self.heuristic = heuristic
        self.action = action
    
    def __str__(self):
        return str(self.state_map)
    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.heuristic < other.heuristic

#------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------MYTREE------------------------------------------------------------

# Arvores de pesquisa
class MyTree:
    def __init__(self,problem): 
        self.problem = problem
        root = MyNode(MyMap(problem.initial), None, 0, 0, None)
        self.open_nodes = [root]
        self.visited_states = {}
        self.solution = None

    # get state maps from root to a given node
    def get_path(self,node):
        if node.parent == None:
            return [node.state_map.mapa]
        path = self.get_path(node.parent)
        path += [node.state_map.mapa]
        return path

    def get_plan(self, node):
        if node.parent == None:
            return []
        plan = self.get_plan(node.parent) # recursively from the root until this node
        plan += [node.action] # getting the list of keys used
        return plan

    def isRepeatedState(self, node):
        if node.state_map.keeper not in self.visited_states:
            return False
        for box_list in self.visited_states[node.state_map.keeper]:
            if box_list == node.state_map.boxes:
                return True
        return False
        
    # search for solution TODO: put the async here
    async def search(self, limit=None):
        while self.open_nodes != []:
            await asyncio.sleep(0)
            node = self.open_nodes.pop(0)
            print("--")
            if node.parent != None:
                print("p " + str(node.parent.state_map.keeper) + ", node " +  str(node.action) + " keeper " + str(node.state_map.keeper) + " depth " + str(node.depth))
            if self.problem.goal_test(node.state_map):
                self.solution = node
                return self.get_plan(node)
            lnewnodes = []
            if node.state_map.keeper not in self.visited_states.keys():
                self.visited_states[node.state_map.keeper] =  [node.state_map.boxes]
            else:
                 self.visited_states[node.state_map.keeper].append(node.state_map.boxes)
            for key in self.problem.domain.actions(node.state_map): # for each avaliable action on this state
                newstate = self.problem.domain.result(node.state_map,key)
                newnode = MyNode(newstate, node, node.depth+1, self.problem.domain.heuristic(newstate), key) # creating child node
                if not self.isRepeatedState(newnode):
                    lnewnodes.append(newnode)
            for element in lnewnodes:
                bisect.insort(self.open_nodes, element)
        return None
