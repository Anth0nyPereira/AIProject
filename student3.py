from mapa import Map


class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

class Node:
    def __init__(self, tree, parent=None, key=None, state_map):
        self.tree = tree
        self.parent = parent
        self.key = key
        self.state_map = state_map
        self.children = []
        create_childs()

    def create_childs(self):

        visitDirs = ['w', 'a', 's', 'd']        #Array de direções
        mapCopy = self.state_map.copy()         #Copia do mapa

        for dir in visitDirs:                           #Para cada direção
            valid = mapCopy.move(dir)                      #Ver se é possivel, se sim valid será true e a copia do mapa alterada
            nonCornerBlock = mapCopy.checkCorner()         #Se o anterior foi true vamos verificar se a jogada bloqueou uma caixa num canto (se a jogada não for valida já vai falhar a condição abaixo logo esta linha não é importante) / este metodo será implementado em mapa.py
            if(valid and nonCornerBlock):               #Se a jogada for válida e não bloquear caixas vamos gerar o node
                Node(self.tree, self, dir, mapCopy)

class Tree:
    def __init__(self, problem):
        self.problem = problem
        self.root = Node(self, problem.initial) #problem initial é o estado inicial do nivel
        self.open_nodes = [self.root]
        self.solution = None

        def search(self):
            while self.open_nodes != []:
                node = self.open_nodes.pop(0)
                if self.problem.goal_test(node.state_map):
                    self.terminal = len(self.open_nodes) + 1
                    self.solution = node
                    return self.get_play(node)
                #self.non_terminal += 1
                #node.children = []
                #self.nodeList.append(node)
                #offset = 0
                #for tryNode in self.nodeList:
                    #if (tryNode.depth == tryNode.depth + 1):
                        #offset = offset + 1
                #for a in self.problem.domain.actions(node.state):
                    #newstate = self.problem.domain.result(node.state, a)
                    #if newstate not in self.get_path(node):
                        #newnode = MyNode(newstate, node.depth + 1, offset, node)
                        #node.children.append(newnode)
                #self.add_to_open(node.children)
            #return None

        def get_play(self, node):
            if node.parent == None:
                return []
            play = self.get_play(node.parent)
            play += [node.key]
            return (play)





   # def create_childs(self):
   #     visited = {'w': False, 'a': False, 's': False, 'd': False}
   #     queue = ['w']

    #    while queue:
     #       s = queue.pop(0)
     #       Node(tree, self, s, state_map.copy())

      #      for key in tree[s]:
     #               if visited[key] == False:
     #                   queue.append(key)
    #                    visited[key] = True


     #       mapa = mapa.move(key)

     #       if mapa != self.state_map:
     #           child_node = Node(self, key, mapa)
     #           tree[self].append(child_node)




{root: [w,d,a,s], nw : [w,d,s,a],  ..... }

