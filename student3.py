from mapa import Map

class Tree:
    def __init__(self, state_map):
        root = Node(self.dict, state_map)
        self.dict = {root: []}

class Node:
    def __init__(self, tree, parent=None, key=None, state_map):
        self.tree = tree
        self.parent = parent
        self.key = key
        self.state_map = state_map
        create_childs()

    def create_childs(self):

        visitDirs = ['w', 'a', 's', 'd']        #Array de direções
        mapCopy = self.state_map.copy()         #Copia do mapa

        for dir in visitDirs:                           #Para cada direção
            valid = mapCopy.move(dir)                      #Ver se é possivel, se sim valid será true e a copia do mapa alterada
            nonCornerBlock = mapCopy.checkCorner()         #Se o anterior foi true vamos verificar se a jogada bloqueou uma caixa num canto (se a jogada não for valida já vai falhar a condição abaixo logo esta linha não é importante) / este metodo será implementado em mapa.py
            if(valid and nonCornerBlock):               #Se a jogada for válida e não bloquear caixas vamos gerar o node
                Node(self.tree, self, dir, mapCopy)


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

