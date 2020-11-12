import mapa

class Tree:
    def __init__(self, state_map):
        root = Node(self.dict, state_map)
        self.dict = {root: []}

class Node:
    def __init__(self, tree, parent=None, key=None, state_map):
        self.parent = parent
        self.key = key
        self.state_map = state_map
        create_childs()

    def create_childs(self):
        visited = {'w': False, 'a': False, 's': False, 'd': False}
        queue = ['w']

        while queue:
            s = queue.pop(0)
            Node(tree, self, s, state_map.copy())

            for key in tree[s]:
                    if visited[key] == False: 
                        queue.append(key) 
                        visited[key] = True


            mapa = mapa.move(key)

            if mapa != self.state_map:
                child_node = Node(self, key, mapa)
                tree[self].append(child_node)




{root: [w,d,a,s], nw : [w,d,s,a],  ..... }

