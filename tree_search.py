from audioop import add
from functools import reduce
import copy
import asyncio
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
        if state_map[y+1][x] == 8 and state_map[y][x+1] == 8: # down and right are walls 
            return True
        elif state_map[y+1][x] == 8 and state_map[y][x-1] == 8: # down and left are walls
            return True
        elif state_map[y-1][x] == 8 and state_map[y][x+1] == 8: # up and rigtht are walls
            return True
        elif state_map[y-1][x] == 8 and state_map[y][x-1] == 8: # up and left are walls
            return True
        return False

    def BoxesNextToWall(self, state_map, pos): # pos will be the final position of a box
        x, y = pos
        if state_map[y][x+1] == 4 and (state_map[y+1][x] == 8 and state_map[y+1][x+1] == 8):
            return True
        elif state_map[y][x-1] == 4 and (state_map[y+1][x] == 8 and state_map[y+1][x-1] == 8):
            return True
        elif state_map[y][x+1] == 4 and (state_map[y-1][x] == 8 and state_map[y-1][x+1] == 8):
            return True
        elif state_map[y][x-1] == 4 and (state_map[y-1][x] == 8 and state_map[y-1][x-1] == 8):
            return True
        elif state_map[y+1][x] == 4 and (state_map[y][x-1] == 8 and state_map[y+1][x-1] == 8):
            return True
        elif state_map[y-1][x] == 4 and (state_map[y][x-1] == 8 and state_map[y-1][x-1] == 8):
            return True
        elif state_map[y+1][x] == 4 and (state_map[y][x+1] == 8 and state_map[y+1][x+1] == 8):
            return True
        elif state_map[y-1][x] == 4 and (state_map[y][x+1] == 8 and state_map[y-1][x+1] == 8):
            return True
        return False

    def BoxNextWallNotGoal(self, state_map, pos):
        # this method will check if a given position of a box (after the push) will stop or not to move in a specific orientation:
        # if a goal exists and the box is near a wall, check if the box can achieve that goal
        x, y = pos
        goals = state_map.empty_goals
    
        if state_map.mapa[y][x+1] == 8: # right-wall, can only move vertically -> same x
            exists = [l for l in goals if l[0] == x] 
            if len(exists) == 0:
                return True
        
        elif state_map.mapa[y][x-1] == 8: # left-wall, can only move vertically -> same x
            exists = [l for l in goals if l[0] == x] 
            if len(exists) == 0:
                return True

        elif state_map.mapa[y+1][x] == 8: # down-wall, can only move horizontally -> same y
            exists = [l for l in goals if l[1] == y] 
            if len(exists) == 0:
                return True
        
        elif state_map.mapa[y-1][x] == 8: # up-wall, can only move horizontally -> same y
            exists = [l for l in goals if l[1] == y] 
            if len(exists) == 0:
                return True 

        return False

    def deadlocks(self, state_map, mapa, pos):
        deadlock1 = self.cornerCheck(state_map, pos)
        #deadlock2 = self.BoxesNextToWall(state_map, pos)
        deadlock3 = self.BoxNextWallNotGoal(mapa, pos)
        if deadlock1 or deadlock3:
            return True
        return False

    def actions(self, state_map): # valid actions for a given state
        actList = []

        keeper_x, keeper_y = state_map.keeper

        # for each direction, if the next tile is "empty", the action is valid
        # if the next tile has a box, then the action is only valid if the other next tile is "empty" and not a corner
        # TODO: add cornercheck and blockedcheck

        if state_map.mapa[keeper_y][keeper_x + 1] == 0 or state_map.mapa[keeper_y][keeper_x + 1] == 1: # next position is a floor or goal - move
            actList.append('d')
        elif state_map.mapa[keeper_y][keeper_x + 1] == 4 or state_map.mapa[keeper_y][keeper_x + 1] == 5: # next position is a box or box on goal
            if (state_map.mapa[keeper_y][keeper_x + 2] == 0 and not self.deadlocks(state_map.mapa, state_map, (keeper_x + 2, keeper_y))) or state_map.mapa[keeper_y][keeper_x + 2] == 1:
                actList.append('d') 
            
        if state_map.mapa[keeper_y][keeper_x - 1] == 0 or state_map.mapa[keeper_y][keeper_x - 1] == 1:
            actList.append('a')
        elif state_map.mapa[keeper_y][keeper_x - 1] == 4 or state_map.mapa[keeper_y][keeper_x - 1] == 5:
            if (state_map.mapa[keeper_y][keeper_x - 2] == 0 and not self.deadlocks(state_map.mapa, state_map, (keeper_x - 2, keeper_y))) or state_map.mapa[keeper_y][keeper_x - 2] == 1:
                actList.append('a')
            
        
        if state_map.mapa[keeper_y + 1][keeper_x] == 0 or state_map.mapa[keeper_y + 1][keeper_x] == 1:
            actList.append('s')
        elif state_map.mapa[keeper_y + 1][keeper_x] == 4 or state_map.mapa[keeper_y + 1][keeper_x] == 5:
            if (state_map.mapa[keeper_y + 2][keeper_x] == 0 and not self.deadlocks(state_map.mapa, state_map, (keeper_x, keeper_y + 2))) or state_map.mapa[keeper_y + 2][keeper_x] == 1:
                actList.append('s')
            

        if state_map.mapa[keeper_y - 1][keeper_x] == 0 or state_map.mapa[keeper_y - 1][keeper_x] == 1:
            actList.append('w')
        elif state_map.mapa[keeper_y - 1][keeper_x] == 4 or state_map.mapa[keeper_y - 1][keeper_x] == 5:
            if (state_map.mapa[keeper_y - 2][keeper_x] == 0 and not self.deadlocks(state_map.mapa, state_map, (keeper_x, keeper_y - 2))) or state_map.mapa[keeper_y - 2][keeper_x] == 1:
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

    def cost(self, state, action):
        return 1
    

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
    def __init__(self,state_map,parent,depth,action): 
        self.state_map = state_map
        self.parent = parent
        self.depth = depth
        self.action = action
            
    # preventing cycles
    def in_parent(self, newstate):
        if self.parent == None:
            return False
        if self.parent.state_map.mapa == newstate.mapa:
            return True
        
        return self.parent.in_parent(newstate) 
        
    def __str__(self):
        return str(self.state_map)
    def __repr__(self):
        return str(self)

#------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------MYTREE------------------------------------------------------------

# Arvores de pesquisa
class MyTree:
    def __init__(self,problem): 
        self.problem = problem
        root = MyNode(MyMap(problem.initial), None, 0, None)
        self.open_nodes = [root]
        self.solution = None
        self.terminals = 1  #root starts as terminal
        self.non_terminals = 0

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

    @property
    def plan(self):
        return self.get_plan(self.solution) # this is what we want to pass to the server!!
        
    @property
    def length(self):
            return self.solution.depth # number of steps it takes from root to solution
               
    @property # average of expansions ? 
    def avg_branching(self):
        return round((self.terminals + self.non_terminals - 1) / self.non_terminals, 2) # 2 decimal figures
        
    # search for solution TODO: put the async here
    async def search(self, limit=None):
        while self.open_nodes != []:
            await asyncio.sleep(0)
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state_map):
                self.solution = node
                self.terminals = len(self.open_nodes) + 1
                print(self.get_plan(node))
                return self.get_plan(node)
            self.non_terminals += 1 # the open node we just popped now has children
            lnewnodes = []
            for key in self.problem.domain.actions(node.state_map): # for each avaliable action on this state
                newstate = self.problem.domain.result(node.state_map,key)
                newnode = MyNode(newstate, node, node.depth+1, key) # creating child node
                if not node.in_parent(newstate) and (limit == None or newnode.depth <= limit):
                    lnewnodes.append(newnode)
            self.open_nodes.extend(lnewnodes)
        return None
