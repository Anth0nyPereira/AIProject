from mapa import Map

#Há muita coisa comentada que são partes das implementações antigas que não me pareceram apropriadas / uteis mas deixei caso venham a ser necessárias
#Retirei o dominio porque aquilo que o dominio fazia é o que estamos a fazer com o mapa, logo acho que o mapa é o nosso dominio.
#A forma como isto funciona é, criamos uma arvore, que tem um problema, o problema é o estado inicial do mapa simplesmente.
#O problema vai dar origem ao root node que vai automaticamente gerar todos os outros nodes da arvore sobre 2 condições:
#A jogada é possivel
#A jogada não leva caixas para cantos
#Depois o search da arvore vai percorrer todos os nodes até encontrar um que passe no problem.goal_test, ou seja que tenha todos os diamantes preenchidos por caixas
#Quando encontrar vai dar-nos as jogadas que temos que fazer em forma de um array através do get_play

class SearchProblem:
    def __init__(self, initial):   #Initial é o estado do mapa quando o nivel começa
        self.initial = initial
    def goal_test(self, state):
        if(state.empty_goals() == 0):  #Se os goals tem todos caixas em cima então está ganho
            return True

        else:
            return False

class Node:
    def __init__(self, tree, parent=None, key=None, state_map):
        self.tree = tree
        self.parent = parent
        self.key = key
        self.state_map = state_map
        self.children = []
        create_childs()                 #Cria os filhos
        tree.open_nodes.append(self)    #E junta-se ao grupo de nós a explorar

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
        self.open_nodes = [self.root]           #nodes a explorar
        self.solution = None                    #node da jogada final, não me parece importante mas pode vir a ser
        self.visitedStates = []                 #estados em que já tivemos, para ele não andar de um lado para o outro sem fazer nada

        def search(self):
            while self.open_nodes != []:
                node = self.open_nodes.pop(0)
                if(node.state_map in self.visitedStates):                   #Evitar que ele volte a estados em que já esteve (não sei se isto não vai causar problemas mais tarde)
                    continue                                                #Se ele não conseguir encontrar soluções retirem esta linha, pode estar a causar problemas
                if self.problem.goal_test(node.state_map):                  #Verificar se é solução
                    #self.terminal = len(self.open_nodes) + 1               #Não me parece necessário mas posso estar errado
                    self.solution = node
                    return self.get_play(node)
                else:
                    self.visitedStates.append(node.state_map)
                                                                            # Tudo isto era geração de nós que já estamos a fazer com o create_childs no Node
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

        def get_play(self, node):                        #Basicamente o mesmo que o get_path era nas cidades mas já nos dá o array com as teclas a primir para resolver o nivel
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

